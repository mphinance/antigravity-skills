#!/usr/bin/env python3
"""
Urithiru Runner — Multi-lane AI verification system
Fires queries to multiple OpenRouter models in parallel and returns structured results.

Usage:
    python3 runner.py --query "your question here" --lanes 5 --category code
    python3 runner.py --query-file /tmp/query.txt --lanes 7 --category trading
    python3 runner.py --query "..." --lanes 5 --dry-run   # show config, don't call APIs
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiohttp

# v2 adaptive routing — imported lazily so runner still works without them
try:
    from router import get_routing_decision, format_routing_header
    from tracker import select_lanes, record_run, cache_lookup
    from outlier_detector import detect_outliers, format_outlier_report
    V2_AVAILABLE = True
except ImportError:
    V2_AVAILABLE = False

# ── Paths ─────────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent
MODELS_FILE = SKILL_DIR / "models.json"
PROMPTS_DIR = SKILL_DIR / "prompts"
LOGS_DIR = SKILL_DIR / "logs"

# ── API Config ─────────────────────────────────────────────────────────────────
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT_SECONDS = 120  # DeepSeek V4 Pro (Pattern) can take 60-90s on complex queries

# Per-model timeout overrides (seconds) — set higher for known slow models
# DeepSeek V4 Pro: chain-of-thought on complex queries can take 3-4 min on OpenRouter shared queue
# Qwen3-235B: large model, can be slow under load
MODEL_TIMEOUTS = {
    "deepseek/deepseek-v4-pro": 240,
    "qwen/qwen3-235b-a22b": 180,
}

# ── Category system prompts ────────────────────────────────────────────────────
CATEGORY_PREAMBLES = {
    "code": (
        "You are reviewing code or answering a coding question. "
        "Evaluate correctness, performance, maintainability, edge cases, and security. "
        "Show your reasoning. Be specific — point to exact lines or patterns."
    ),
    "trading": (
        "You are analyzing a trading strategy, signal, or market setup. "
        "Evaluate risk/reward, statistical edge, market regime applicability, "
        "execution feasibility, and failure modes. Quantify where possible."
    ),
    "writing": (
        "You are reviewing written content for publication. "
        "Evaluate clarity, narrative flow, factual accuracy, audience engagement, "
        "and logical structure. Suggest specific improvements."
    ),
    "general": (
        "You are solving a problem or answering a question. "
        "Be thorough, precise, and honest about uncertainty. "
        "Show your reasoning chain."
    ),
}


def load_api_key() -> str:
    """Load OpenRouter API key from env var or .env file."""
    # 1. Check environment variable first
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key:
        return key

    # 2. Check skill-level .env
    skill_env = SKILL_DIR / ".env"
    if skill_env.exists():
        content = skill_env.read_text().strip()
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
            # Handle bare key (legacy format from Urithiru/.env)
            if line.startswith("sk-or-"):
                return line

    # 3. Check workspace .env (legacy location)
    workspace_env = Path("/home/mph/Antigravity/Urithiru/.env")
    if workspace_env.exists():
        content = workspace_env.read_text().strip()
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip()
            if line.startswith("sk-or-"):
                return line

    raise ValueError(
        "OpenRouter API key not found. Set OPENROUTER_API_KEY env var "
        "or add it to ~/.gemini/antigravity/skills/urithiru/.env"
    )


def load_models() -> dict:
    """Load models config from models.json."""
    with open(MODELS_FILE) as f:
        return json.load(f)


def build_lane_list(models: dict, lane_count: int) -> list[dict]:
    """Build the list of lanes to run."""
    lanes = list(models["core_lanes"])
    if lane_count == 7:
        lanes += list(models["expansion_lanes"])
    return lanes[:lane_count]


def build_system_prompt(lane: dict, category: str) -> str:
    """Build the full system prompt for a lane."""
    codename = lane["codename"]
    prompt_file = PROMPTS_DIR / f"{codename.lower()}.md"

    if prompt_file.exists():
        model_prompt = prompt_file.read_text().strip()
    else:
        model_prompt = f"You are {codename}. {lane['role']}"

    preamble = CATEGORY_PREAMBLES.get(category, CATEGORY_PREAMBLES["general"])
    return f"{preamble}\n\n{model_prompt}"


async def call_lane(
    session: aiohttp.ClientSession,
    api_key: str,
    lane: dict,
    query: str,
    category: str,
    lane_number: int,
) -> dict:
    """Call a single lane and return structured result."""
    start = time.time()
    system_prompt = build_system_prompt(lane, category)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://antigravity.urithiru",
        "X-Title": "Urithiru",
    }

    payload = {
        "model": lane["id"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }

    result = {
        "lane": lane_number,
        "codename": lane["codename"],
        "model_id": lane["id"],
        "role": lane["role"],
        "status": "pending",
        "response": None,
        "error": None,
        "elapsed_seconds": None,
        "prompt_tokens": None,
        "completion_tokens": None,
        "cost_usd": None,
        "system_prompt": system_prompt,
    }

    try:
        model_timeout = MODEL_TIMEOUTS.get(lane["id"], TIMEOUT_SECONDS)
        async with session.post(
            OPENROUTER_BASE,
            headers=headers,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=model_timeout),
        ) as resp:
            elapsed = time.time() - start
            result["elapsed_seconds"] = round(elapsed, 2)

            if resp.status != 200:
                error_text = await resp.text()
                result["status"] = "error"
                result["error"] = f"HTTP {resp.status}: {error_text[:500]}"
                return result

            data = await resp.json()

            # Extract response content
            choice = data.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content", "") or ""
            finish_reason = choice.get("finish_reason", "")

            # Extract usage FIRST — need it even for empty responses
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            result["prompt_tokens"] = prompt_tokens
            result["completion_tokens"] = completion_tokens

            # Detect silent empty responses (HTTP 200, no content, no tokens billed).
            # Causes: content filter/refusal at OpenRouter layer, rate limit disguised as 200,
            # or model returned null content. These are NOT successes — log and flag them.
            if not content.strip() and completion_tokens == 0:
                result["status"] = "empty"
                result["error"] = (
                    f"Empty response (HTTP 200, 0 completion tokens, finish_reason={finish_reason!r}). "
                    f"Likely: content filter, silent rate limit, or model refusal. "
                    f"Raw keys: {list(data.keys())}"
                )
                result["response"] = None
                result["cost_usd"] = 0.0
                return result

            result["response"] = content
            result["status"] = "success"

            # Calculate cost
            cost = (
                (prompt_tokens / 1_000_000) * lane["prompt_cost_per_m"]
                + (completion_tokens / 1_000_000) * lane["completion_cost_per_m"]
            )
            result["cost_usd"] = round(cost, 6)

    except asyncio.TimeoutError:
        model_timeout = MODEL_TIMEOUTS.get(lane["id"], TIMEOUT_SECONDS)
        result["status"] = "timeout"
        result["error"] = f"Lane timed out after {model_timeout}s"
        result["elapsed_seconds"] = round(time.time() - start, 2)
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        result["elapsed_seconds"] = round(time.time() - start, 2)

    return result


async def run_urithiru(
    query: str,
    lane_count: int,
    category: str,
    session_id: Optional[str] = None,
    dry_run: bool = False,
    auto_route: bool = False,
    stakes_hint: Optional[str] = None,
) -> dict:
    """Main orchestration function — fires all lanes in parallel."""
    api_key = load_api_key()
    models_data = load_models()
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    routing_reason = f"{lane_count} lanes (manual)"
    stakes_level = stakes_hint or "medium"
    cache_status = "miss"

    # ── v2 Auto-routing ────────────────────────────────────────────────────────
    if auto_route and V2_AVAILABLE:
        decision = get_routing_decision(
            query, category_hint=category,
            lane_hint=None, stakes_hint=stakes_hint
        )
        category = decision["category"]
        lane_count = decision["lane_count"]
        routing_reason = decision["routing_reason"]
        stakes_level = decision["stakes"]

        # Check semantic cache before firing lanes
        cache_status, cache_hits = cache_lookup(query, category)
        if cache_status == "hit" and not dry_run:
            hit = cache_hits[0]
            print(f"\n⚡ CACHE HIT (similarity={hit['similarity']:.4f}) — serving cached answer")
            print(f"   Cached at: {hit['timestamp'][:19]} | Skipping API calls")
            print(f"   Answer:\n{hit['answer'][:400]}...\n")
            # Still return a minimal trace so logs are consistent
            return {
                "run_id": f"urithiru_{run_timestamp}",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "category": category,
                "lane_count": 0,
                "query": query,
                "lane_results": [],
                "total_cost_usd": 0.0,
                "total_elapsed_seconds": 0.0,
                "status": "cache_hit",
                "cache_answer": hit["answer"],
                "routing_reason": routing_reason,
                "stakes_level": stakes_level,
            }

        # Select optimal lanes via Thompson Sampling
        all_model_ids = [l["id"] for l in models_data["core_lanes"] + models_data["expansion_lanes"]]
        selected_ids, debug_info = select_lanes(
            category=category,
            lane_count=lane_count,
            available_model_ids=all_model_ids,
            speed_biased=decision["speed_biased"],
        )
        # Build lane list from selected model IDs (preserving metadata from models.json)
        id_to_lane = {l["id"]: l for l in models_data["core_lanes"] + models_data["expansion_lanes"]}
        lanes = [id_to_lane[mid] for mid in selected_ids if mid in id_to_lane]

        # Attach debug info to lane list for routing header
        codename_to_debug = {d.get("model_id", ""): d for d in debug_info}
        for lane in lanes:
            dbg = codename_to_debug.get(lane["id"], {})
            lane["_sample_score"] = dbg.get("sample_score", 0.0)

        # Print routing header (always — even dry-run so you can see what would fire)
        print(format_routing_header(decision, [
            {"codename": l["codename"], "sample_score": l.get("_sample_score", 0),
             "speed_bonus": decision["speed_biased"] and l["id"] in ("x-ai/grok-4-fast",),
             "diversity_override": codename_to_debug.get(l["id"], {}).get("diversity_override", False)}
            for l in lanes
        ]))
        # Inject RAG context if cache returned context hits
        if cache_status == "context" and cache_hits:
            ctx_block = "\n\n---\nRELATED PAST ANALYSES (use as context, not as answers):\n"
            for h in cache_hits:
                ctx_block += f"\n[sim={h['similarity']:.3f}, {h['timestamp'][:10]}]\n{h['answer'][:300]}\n"
            query = query + ctx_block
            print(f"  📚 RAG context: injected {len(cache_hits)} similar past runs")
    else:
        lanes = build_lane_list(models_data, lane_count)

    trace = {
        "run_id": f"urithiru_{run_timestamp}",
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "lane_count": lane_count,
        "query": query,
        "lane_results": [],
        "total_cost_usd": None,
        "total_elapsed_seconds": None,
        "status": "pending",
        "routing_reason": routing_reason,
        "stakes_level": stakes_level,
        "cache_status": cache_status,
    }

    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN — Urithiru | {lane_count} Lanes | Category: {category} | Stakes: {stakes_level}")
        print(f"{'='*60}")
        for i, lane in enumerate(lanes, 1):
            print(f"  Lane {i}: [{lane['codename']}] {lane['id']}")
            print(f"           ${lane['prompt_cost_per_m']:.2f}/${lane['completion_cost_per_m']:.2f} per M tokens")
            print(f"           Role: {lane['role']}")
        print(f"\nQuery ({len(query)} chars):")
        print(f"  {query[:200]}{'...' if len(query) > 200 else ''}")
        print(f"\nRouting: {routing_reason}")
        print(f"No API calls made (dry run mode)\n")
        return trace

    print(f"\n🗼 Urithiru — {lane_count} Lanes | {category.upper()} | {run_timestamp}")
    print(f"   Firing {lane_count} lanes in parallel...")

    wall_start = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [
            call_lane(session, api_key, lane, query, category, i + 1)
            for i, lane in enumerate(lanes)
        ]
        results = await asyncio.gather(*tasks)

    total_elapsed = round(time.time() - wall_start, 2)
    trace["lane_results"] = results
    trace["total_elapsed_seconds"] = total_elapsed

    # Aggregate costs
    total_cost = sum(r["cost_usd"] or 0 for r in results)
    trace["total_cost_usd"] = round(total_cost, 6)
    trace["status"] = "complete"

    # ── v2: Outlier detection before synthesis ─────────────────────────────────
    if V2_AVAILABLE:
        outlier_result = detect_outliers(results)
        trace["outlier_detection"] = outlier_result
        # Mark outlier lanes so tracker knows to discount them
        for r in results:
            if any(o["codename"] == r["codename"] for o in outlier_result.get("outliers", [])):
                r["is_outlier"] = 1
        print(format_outlier_report(outlier_result))

    # ── v2: Record run in tracker DB for Bayesian learning ────────────────────
    if V2_AVAILABLE:
        try:
            record_run(
                run_id=trace["run_id"],
                category=category,
                lane_count=lane_count,
                query=query,
                total_cost_usd=total_cost,
                wall_time_seconds=total_elapsed,
                routing_reason=routing_reason,
                stakes_level=stakes_level,
                lane_results=results,
            )
        except Exception as e:
            print(f"  ⚠️  Tracker record failed (non-fatal): {e}")

    # Print lane summaries
    print(f"\n{'─'*60}")
    STATUS_ICONS = {"success": "✅", "timeout": "⏱️ ", "empty": "🔇", "error": "❌"}
    for r in results:
        status_icon = STATUS_ICONS.get(r["status"], "❓")
        cost_str = f"${r['cost_usd']:.5f}" if r["cost_usd"] else "  N/A  "
        tokens = f"{(r['prompt_tokens'] or 0) + (r['completion_tokens'] or 0)} tok"
        print(f"  {status_icon} Lane {r['lane']} [{r['codename']:12s}] {r['elapsed_seconds']}s | {tokens} | {cost_str}")
        if r["status"] == "success" and r["response"]:
            preview = r["response"][:120].replace("\n", " ")
            print(f"     └─ {preview}...")
        elif r["status"] == "empty":
            print(f"     └─ 🔇 SILENT EMPTY: {r['error'][:120]}")
        elif r["error"]:
            print(f"     └─ {r['error'][:120]}")
    print(f"{'─'*60}")
    print(f"  🕐 Wall time: {total_elapsed}s | 💰 Total cost: ${total_cost:.5f}")

    return trace


def save_trace(trace: dict, category: str) -> Path:
    """Save trace to JSONL log file."""
    LOGS_DIR.mkdir(exist_ok=True)
    log_filename = f"{trace['run_id']}_{category}.jsonl"
    log_path = LOGS_DIR / log_filename

    with open(log_path, "w") as f:
        json.dump(trace, f, indent=2)

    return log_path


def try_send_to_langfuse(trace: dict) -> bool:
    """
    Optionally send trace to Langfuse if credentials are configured.
    Returns True if sent, False if Langfuse not configured.

    To enable: set LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST in env.
    Self-hosted: LANGFUSE_HOST=http://localhost:3000
    """
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not (secret_key and public_key):
        return False

    try:
        from langfuse import Langfuse  # type: ignore

        lf = Langfuse(
            secret_key=secret_key,
            public_key=public_key,
            host=host,
        )

        t = lf.trace(
            id=trace["run_id"],
            name="urithiru-run",
            input={"query": trace["query"]},
            metadata={
                "category": trace["category"],
                "lane_count": trace["lane_count"],
                "session_id": trace["session_id"],
            },
        )

        for r in trace.get("lane_results", []):
            t.span(
                name=f"lane-{r['lane']}-{r['codename']}",
                input={"system": r.get("system_prompt", ""), "user": trace["query"]},
                output=r.get("response", r.get("error", "")),
                metadata={
                    "model": r["model_id"],
                    "status": r["status"],
                    "elapsed_seconds": r.get("elapsed_seconds"),
                    "prompt_tokens": r.get("prompt_tokens"),
                    "completion_tokens": r.get("completion_tokens"),
                    "cost_usd": r.get("cost_usd"),
                },
            )

        lf.flush()
        return True

    except ImportError:
        print("  ℹ️  Langfuse not installed (pip install langfuse). Using local logs only.")
        return False
    except Exception as e:
        print(f"  ⚠️  Langfuse send failed: {e}. Local log still saved.")
        return False


def print_full_responses(trace: dict) -> None:
    """Print full lane responses for synthesis."""
    print(f"\n{'='*60}")
    print("LANE RESPONSES — FULL OUTPUT")
    print(f"{'='*60}\n")

    for r in trace["lane_results"]:
        if r["status"] == "success":
            print(f"── Lane {r['lane']}: {r['codename']} ({r['model_id']}) ──────")
            print(r["response"])
            print()
        else:
            print(f"── Lane {r['lane']}: {r['codename']} [FAILED: {r['status']}] ──")
            print(f"Error: {r['error']}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Urithiru — Multi-lane AI verification runner"
    )
    query_group = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument("--query", "-q", type=str, help="Query string")
    query_group.add_argument("--query-file", "-f", type=str, help="File containing query")

    parser.add_argument(
        "--lanes", "-l", type=int, choices=[3, 5, 7], default=None,
        help="Number of lanes (3/5/7). Omit to use --auto routing."
    )
    parser.add_argument(
        "--auto", action="store_true",
        help="Auto-route: let router.py pick lane count and tracker.py pick models"
    )
    parser.add_argument(
        "--stakes", type=str, choices=["low", "medium", "high", "critical"], default=None,
        help="Override auto-detected stakes level (used with --auto)"
    )
    parser.add_argument(
        "--category", "-c",
        choices=["code", "trading", "writing", "general"],
        default=None,
        help="Query category hint. Auto-detected if omitted with --auto."
    )
    parser.add_argument(
        "--session-id", "-s", type=str, default=None,
        help="Optional session label for grouping runs in logs"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show lane config without making API calls"
    )
    parser.add_argument(
        "--full-output", action="store_true",
        help="Print full lane responses (for synthesis step)"
    )
    parser.add_argument(
        "--json-out", type=str, default=None,
        help="Write trace JSON to this file path"
    )

    args = parser.parse_args()

    # Load query
    if args.query_file:
        query = Path(args.query_file).read_text().strip()
    else:
        query = args.query.strip()

    if not query:
        print("Error: Query is empty.", file=sys.stderr)
        sys.exit(1)

    # Resolve defaults for non-auto mode
    lane_count = args.lanes if args.lanes is not None else 5
    category = args.category if args.category else "general"

    # Run
    trace = asyncio.run(
        run_urithiru(
            query=query,
            lane_count=lane_count,
            category=category,
            session_id=args.session_id,
            dry_run=args.dry_run,
            auto_route=args.auto,
            stakes_hint=args.stakes,
        )
    )

    if args.dry_run:
        return

    # Print full responses if requested
    if args.full_output:
        print_full_responses(trace)

    # Save trace locally
    resolved_category = trace.get("category", category)
    log_path = save_trace(trace, resolved_category)
    print(f"\n  📝 Trace saved: {log_path}")

    # Try Langfuse
    if try_send_to_langfuse(trace):
        print("  📡 Trace sent to Langfuse")

    # Optional JSON output
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(trace, f, indent=2)
        print(f"  💾 JSON written: {args.json_out}")

    print(f"\n🗼 Urithiru complete. Now synthesize.\n")


if __name__ == "__main__":
    main()

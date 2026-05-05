#!/usr/bin/env python3
"""
stats.py — Urithiru run analytics
Reads JSONL logs and surfaces cost, latency, quality, and model performance.
Think of this as your local Langfuse dashboard.

Usage:
    python3 stats.py                    # Summary of all runs
    python3 stats.py --last 10          # Last 10 runs
    python3 stats.py --category trading # Filter by category
    python3 stats.py --lane Stormfather # Lane-specific stats
    python3 stats.py --run <run_id>     # Single run detail
    python3 stats.py --compare          # Compare lanes head-to-head
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Optional

from tracker import get_leaderboard, get_routing_log, get_daily_spend, init_db, get_conn

LOGS_DIR = Path(__file__).parent / "logs"
MODELS_FILE = Path(__file__).parent / "models.json"


def load_traces(
    category: Optional[str] = None,
    last_n: Optional[int] = None,
    run_id: Optional[str] = None,
) -> list[dict]:
    """Load and filter trace files from logs directory."""
    if not LOGS_DIR.exists():
        return []

    files = sorted(LOGS_DIR.glob("*.jsonl"), reverse=True)
    traces = []

    for f in files:
        try:
            trace = json.loads(f.read_text())
            if run_id and trace.get("run_id") != run_id:
                continue
            if category and trace.get("category") != category:
                continue
            if trace.get("status") == "complete":
                traces.append(trace)
        except Exception:
            continue

    if last_n:
        traces = traces[:last_n]

    return traces


def fmt_cost(usd: Optional[float]) -> str:
    if usd is None:
        return "  N/A  "
    return f"${usd:.5f}"


def fmt_ms(seconds: Optional[float]) -> str:
    if seconds is None:
        return "  N/A"
    return f"{seconds*1000:6.0f}ms"


def fmt_tokens(n: Optional[int]) -> str:
    if n is None:
        return "  N/A"
    return f"{n:5d}"


# ── Single Run Detail ──────────────────────────────────────────────────────────

def show_run_detail(trace: dict) -> None:
    run_id = trace.get("run_id", "unknown")
    timestamp = trace.get("timestamp", "")
    category = trace.get("category", "general")
    lane_count = trace.get("lane_count", 0)
    total_cost = trace.get("total_cost_usd", 0)
    total_elapsed = trace.get("total_elapsed_seconds", 0)
    query = trace.get("query", "")

    print(f"\n{'='*70}")
    print(f"  Run: {run_id}")
    print(f"  Time: {timestamp[:19]}")
    print(f"  Category: {category} | Lanes: {lane_count}")
    print(f"  Total Cost: ${total_cost:.5f} | Wall Time: {total_elapsed}s")
    print(f"  Query: {query[:100]}{'...' if len(query) > 100 else ''}")
    print(f"{'='*70}")

    results = trace.get("lane_results", [])
    if not results:
        print("  No lane results found.")
        return

    print(f"\n  {'Lane':<5} {'Codename':<14} {'Status':<10} {'Latency':>9} {'In tok':>7} {'Out tok':>7} {'Cost':>10}")
    print(f"  {'─'*5} {'─'*14} {'─'*10} {'─'*9} {'─'*7} {'─'*7} {'─'*10}")

    for r in results:
        status = r.get("status", "unknown")
        status_icon = {"success": "✅", "empty": "🔇", "timeout": "⏱️", "error": "❌"}.get(status, "❓")
        in_tok = r.get("prompt_tokens")
        out_tok = r.get("completion_tokens")
        cost = r.get("cost_usd")
        elapsed = r.get("elapsed_seconds")

        print(f"  {r.get('lane', '?'):<5} {r.get('codename', '?'):<14} "
              f"{status_icon} {status:<8} "
              f"{fmt_ms(elapsed):>9} "
              f"{fmt_tokens(in_tok):>7} "
              f"{fmt_tokens(out_tok):>7} "
              f"{fmt_cost(cost):>10}")

        if status == "success" and r.get("response"):
            preview = r["response"][:120].replace("\n", " ")
            print(f"         └─ {preview}...")
        elif r.get("error"):
            print(f"         └─ ERROR: {r['error'][:80]}")

    print()


# ── Summary Table ──────────────────────────────────────────────────────────────

def show_summary(traces: list[dict]) -> None:
    if not traces:
        print("\nNo completed runs found in logs/")
        return

    total_cost = sum(t.get("total_cost_usd") or 0 for t in traces)
    total_queries = len(traces)
    avg_cost = total_cost / total_queries if total_queries else 0
    avg_latency = sum(t.get("total_elapsed_seconds") or 0 for t in traces) / total_queries if total_queries else 0

    category_counts = defaultdict(int)
    lane_counts = defaultdict(int)
    for t in traces:
        category_counts[t.get("category", "general")] += 1
        lane_counts[t.get("lane_count", 5)] += 1

    print(f"\n{'='*70}")
    print(f"  🗼 URITHIRU STATS — {total_queries} runs")
    print(f"{'='*70}")
    print(f"  Total spend:    ${total_cost:.4f}")
    print(f"  Avg per query:  ${avg_cost:.5f}")
    print(f"  Avg latency:    {avg_latency:.1f}s")
    print(f"  Runs by category: {dict(category_counts)}")
    print(f"  Runs by lanes:    {dict(lane_counts)}")

    print(f"\n  {'#':<4} {'Run ID':<32} {'Cat':<9} {'Lanes':<6} {'Cost':>10} {'Time':>8}")
    print(f"  {'─'*4} {'─'*32} {'─'*9} {'─'*6} {'─'*10} {'─'*8}")

    for t in traces:
        run_id = t.get("run_id", "")[:30]
        cat = t.get("category", "?")[:8]
        lanes = t.get("lane_count", "?")
        cost = t.get("total_cost_usd")
        elapsed = t.get("total_elapsed_seconds")
        print(f"  {traces.index(t)+1:<4} {run_id:<32} {cat:<9} {str(lanes):<6} "
              f"{fmt_cost(cost):>10} {elapsed or '?':>6}s")

    print()


# ── Lane Comparison ────────────────────────────────────────────────────────────

def show_lane_comparison(traces: list[dict]) -> None:
    """Show per-lane performance stats across all runs."""
    lane_stats = defaultdict(lambda: {
        "runs": 0, "successes": 0, "timeouts": 0, "errors": 0,
        "total_latency": 0.0, "total_cost": 0.0,
        "total_in_tokens": 0, "total_out_tokens": 0,
    })

    for trace in traces:
        for r in trace.get("lane_results", []):
            name = r.get("codename", "Unknown")
            s = lane_stats[name]
            s["runs"] += 1
            status = r.get("status", "error")
            if status == "success":
                s["successes"] += 1
            elif status == "timeout":
                s["timeouts"] += 1
            elif status == "empty":
                s["empties"] = s.get("empties", 0) + 1
            else:
                s["errors"] += 1
            s["total_latency"] += r.get("elapsed_seconds") or 0
            s["total_cost"] += r.get("cost_usd") or 0
            s["total_in_tokens"] += r.get("prompt_tokens") or 0
            s["total_out_tokens"] += r.get("completion_tokens") or 0

    if not lane_stats:
        print("\nNo lane data found.")
        return

    print(f"\n{'='*80}")
    print(f"  🏟  LANE PERFORMANCE COMPARISON — across {len(traces)} runs")
    print(f"{'='*80}")
    print(f"  {'Lane':<14} {'Runs':>5} {'Success%':>9} {'Avg Lat':>9} "
          f"{'Avg Cost':>10} {'Avg Out':>8} {'Total Cost':>11}")
    print(f"  {'─'*14} {'─'*5} {'─'*9} {'─'*9} {'─'*10} {'─'*8} {'─'*11}")

    for name, s in sorted(lane_stats.items(), key=lambda x: x[1]["total_cost"], reverse=True):
        runs = s["runs"]
        if runs == 0:
            continue
        success_pct = (s["successes"] / runs) * 100
        avg_lat = s["total_latency"] / runs
        avg_cost = s["total_cost"] / runs
        avg_out = s["total_out_tokens"] / runs
        total_cost = s["total_cost"]

        timeout_note = f" ({s['timeouts']} timeouts)" if s["timeouts"] else ""
        empty_note = f" ({s.get('empties', 0)} silent empty)" if s.get("empties") else ""
        print(f"  {name:<14} {runs:>5} {success_pct:>8.1f}% {avg_lat:>8.1f}s "
              f"${avg_cost:>9.5f} {avg_out:>7.0f}  ${total_cost:>9.4f}{timeout_note}{empty_note}")

    print()


# ── Single Lane Detail ─────────────────────────────────────────────────────────

def show_lane_detail(traces: list[dict], lane_name: str) -> None:
    """Show all responses from a specific lane."""
    print(f"\n{'='*70}")
    print(f"  Lane Detail: {lane_name}")
    print(f"{'='*70}")

    found = 0
    for trace in traces:
        for r in trace.get("lane_results", []):
            if r.get("codename", "").lower() == lane_name.lower():
                found += 1
                ts = trace.get("timestamp", "")[:19]
                cat = trace.get("category", "?")
                query_preview = trace.get("query", "")[:60]
                status = r.get("status", "?")
                cost = fmt_cost(r.get("cost_usd"))
                elapsed = r.get("elapsed_seconds", "?")

                print(f"\n  [{found}] {ts} | {cat} | {elapsed}s | {cost}")
                print(f"  Query: {query_preview}...")
                print(f"  Status: {status}")
                if r.get("response"):
                    print(f"  Response preview:")
                    print(f"  {r['response'][:300].replace(chr(10), ' ')[:300]}...")

    if not found:
        print(f"\n  No runs found for lane: {lane_name}")
    print()


# ── Cost Trend ─────────────────────────────────────────────────────────────────

def show_cost_trend(traces: list[dict]) -> None:
    """Show cost over time — spot if you're spending more."""
    if not traces:
        return

    # Group by day
    by_day = defaultdict(list)
    for t in traces:
        day = t.get("timestamp", "")[:10]
        cost = t.get("total_cost_usd") or 0
        by_day[day].append(cost)

    print(f"\n{'='*50}")
    print(f"  💰 COST BY DAY")
    print(f"{'='*50}")

    for day in sorted(by_day.keys()):
        costs = by_day[day]
        day_total = sum(costs)
        count = len(costs)
        bar = "█" * min(int(day_total * 100), 40)
        print(f"  {day}  ${day_total:.4f}  ({count} runs)  {bar}")

    print()


# ── V2 DB Stats ────────────────────────────────────────────────────────────────

def show_v2_leaderboard(category: str) -> None:
    rows = get_leaderboard(category)
    if not rows:
        print(f"\nNo data for category: {category}")
        return
        
    init_db()
    with get_conn() as conn:
        total_runs_row = conn.execute("SELECT COUNT(*) FROM runs WHERE category=?", (category,)).fetchone()
        total_runs = total_runs_row[0] if total_runs_row else 0
        
    print(f"\n🏆 LANE LEADERBOARD — {category} | {total_runs} runs\n")
    print(f"  {'Rank':<4} {'Lane':<14} {'Win Rate':<10} {'Runs':<6} {'Uncertainty':<13} {'Avg Cost/run':<12}")
    print(f"  {'─'*4} {'─'*14} {'─'*10} {'─'*6} {'─'*13} {'─'*12}")
    
    warnings = []
    for i, r in enumerate(rows, 1):
        win_rate = f"{r['win_rate']*100:.1f}%"
        unc = f"± {r['uncertainty']:.2f}"
        
        # Get avg cost per run for this model/category
        with get_conn() as conn:
            cost_row = conn.execute(
                "SELECT AVG(cost_usd) as avg_cost FROM lane_results lr JOIN runs r ON r.run_id = lr.run_id WHERE r.category=? AND lr.model_id=? AND lr.status='success'", 
                (category, r['model_id'])
            ).fetchone()
        avg_cost = cost_row["avg_cost"] if cost_row and cost_row["avg_cost"] is not None else 0.0
        cost_str = f"${avg_cost:.4f}"
        
        flag = ""
        if r['runs'] < 30:
            flag = "⚠️"
            warnings.append(f"⚠️  {r['model_id'].split('/')[-1]}: HIGH UNCERTAINTY — only {r['runs']} {category} runs. Needs more data.")
            
        print(f"  {i:<4} {r['model_id'].split('/')[-1]:<14} {win_rate:<10} {r['runs']:<6} {unc:<11} {flag:<1} {cost_str:<12}")
        
    if warnings:
        print("\n" + "\n".join(warnings))
    print()

def show_v2_routing_log() -> None:
    rows = get_routing_log(20)
    if not rows:
        print("\nNo routing data.")
        return
        
    print(f"\n📋 ROUTING DECISIONS — last {len(rows)} runs\n")
    print(f"  {'#':<4} {'Run ID':<22} {'Cat':<9} {'Stakes':<10} {'Lanes':<6} {'Routing Reason'}")
    print(f"  {'─'*4} {'─'*22} {'─'*9} {'─'*10} {'─'*6} {'─'*30}")
    
    for i, r in enumerate(rows, 1):
        run_id = r['run_id'][:20]
        cat = r['category'][:8]
        stakes = r['stakes_level'] or 'unknown'
        lanes = str(r['lane_count'])
        reason = (r['routing_reason'] or '')[:40]
        
        print(f"  {i:<4} {run_id:<22} {cat:<9} {stakes:<10} {lanes:<6} {reason}")
    print()

def show_v2_spend_today() -> None:
    rows = get_daily_spend(7)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_spend = 0.0
    today_runs = 0
    week_spend = 0.0
    
    for r in rows:
        if r['date'] == today:
            today_spend = r['total_usd']
            today_runs = r['run_count']
        week_spend += r['total_usd']
        
    print(f"\n💰 Today's spend: ${today_spend:.2f} ({today_runs} runs) | This week: ${week_spend:.2f}\n")

def show_v2_outliers() -> None:
    init_db()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT r.timestamp, r.category, lr.codename, r.query_preview "
            "FROM lane_results lr JOIN runs r ON r.run_id = lr.run_id "
            "WHERE lr.is_outlier = 1 ORDER BY r.timestamp DESC LIMIT 20"
        ).fetchall()
        
    if not rows:
        print("\n🔍 No outliers flagged yet. The board is in consensus.")
        return
        
    print(f"\n🚨 RECENT OUTLIERS (Flagged before synthesis)\n")
    print(f"  {'Time':<16} {'Cat':<9} {'Lane':<14} {'Query Preview'}")
    print(f"  {'─'*16} {'─'*9} {'─'*14} {'─'*40}")
    
    for r in rows:
        ts = r['timestamp'][5:16].replace('T', ' ')
        cat = r['category'][:8]
        lane = r['codename'][:13]
        query = r['query_preview'][:45] + "..." if len(r['query_preview']) > 45 else r['query_preview']
        print(f"  {ts:<16} {cat:<9} {lane:<14} {query}")
    print()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Urithiru run analytics")
    parser.add_argument("--last", "-n", type=int, default=None, help="Last N runs")
    parser.add_argument("--category", "-c", type=str, default=None, help="Filter by category")
    parser.add_argument("--lane", "-l", type=str, default=None, help="Show detail for a specific lane")
    parser.add_argument("--run", "-r", type=str, default=None, help="Show detail for a specific run ID")
    parser.add_argument("--compare", action="store_true", help="Lane comparison table")
    parser.add_argument("--trend", action="store_true", help="Cost trend by day")
    parser.add_argument("--all", action="store_true", help="Show everything")
    
    # V2 Flags
    parser.add_argument("--leaderboard", type=str, metavar="CATEGORY", help="Who's winning in a given category?")
    parser.add_argument("--routing-log", action="store_true", help="Why did each run choose the lane count it did?")
    parser.add_argument("--spend-today", action="store_true", help="Today's API spend")
    parser.add_argument("--outliers", action="store_true", help="Which lanes were flagged as outliers?")
    
    args = parser.parse_args()

    # Handle V2 arguments first
    if args.leaderboard:
        show_v2_leaderboard(args.leaderboard)
        return
    if args.routing_log:
        show_v2_routing_log()
        return
    if args.spend_today:
        show_v2_spend_today()
        return
    if args.outliers:
        show_v2_outliers()
        return

    traces = load_traces(
        category=args.category,
        last_n=args.last,
        run_id=args.run if args.run else None,
    )

    if args.run:
        if traces:
            show_run_detail(traces[0])
        else:
            print(f"Run ID not found: {args.run}")
        return

    if args.lane:
        all_traces = load_traces()  # need all for lane detail
        show_lane_detail(all_traces, args.lane)
        return

    if args.compare or args.all:
        all_traces = load_traces(category=args.category)
        show_lane_comparison(all_traces)

    if args.trend or args.all:
        all_traces = load_traces()
        show_cost_trend(all_traces)

    show_summary(traces)

    if not traces:
        print("  Run a query first: python3 runner.py --query 'test' --lanes 5")
        print(f"  Looking in: {LOGS_DIR}")


if __name__ == "__main__":
    main()

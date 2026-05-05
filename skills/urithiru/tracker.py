#!/usr/bin/env python3
"""
tracker.py — Urithiru v2 Bayesian Model Tracker
Tracks per-model per-category performance via Beta distributions (Thompson Sampling).
Backed by SQLite for ratings + ChromaDB for semantic query caching.

Usage:
    python3 tracker.py --init
    python3 tracker.py --leaderboard trading
    python3 tracker.py --spend
    python3 tracker.py --routing-log
"""

import argparse
import hashlib
import json
import math
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

SKILL_DIR = Path(__file__).parent
DB_PATH = SKILL_DIR / "tracker.db"
CHROMA_PATH = SKILL_DIR / "chroma_db"
MODELS_FILE = SKILL_DIR / "models.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Per-category similarity thresholds (cosine similarity 0–1)
# Trading stricter: "buy AAPL at 185" != "buy AAPL at 210" even at 0.95 sim
CACHE_HIT_THRESHOLD = {"trading": 0.97, "code": 0.93, "writing": 0.90, "general": 0.92}
CONTEXT_THRESHOLD   = {"trading": 0.88, "code": 0.84, "writing": 0.82, "general": 0.84}

# Per-category cache TTL in seconds
CACHE_TTL = {"trading": 3_600, "code": 2_592_000, "writing": 604_800, "general": 604_800}

# Speed bonus applied during Thompson Sampling when category=trading
# Positive = faster model preferred, negative = slower model penalized
SPEED_BONUS = {
    "x-ai/grok-4-fast":          +0.05,   # Wit — fast and cheap
    "deepseek/deepseek-v4-pro":  -0.03,   # Pattern — slow chain-of-thought
}

# ── SQLite Schema ──────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS models (
    model_id TEXT PRIMARY KEY,
    codename TEXT,
    family TEXT,
    prompt_cost_per_m REAL,
    completion_cost_per_m REAL,
    enabled INTEGER DEFAULT 1
);

-- Beta distribution per (model, category): alpha=wins+prior, beta=losses+prior
CREATE TABLE IF NOT EXISTS model_ratings (
    model_id    TEXT NOT NULL,
    category    TEXT NOT NULL,
    alpha       REAL NOT NULL DEFAULT 2.0,
    beta        REAL NOT NULL DEFAULT 2.0,
    runs        INTEGER NOT NULL DEFAULT 0,
    last_run_at TEXT,
    PRIMARY KEY (model_id, category)
);

CREATE TABLE IF NOT EXISTS runs (
    run_id            TEXT PRIMARY KEY,
    timestamp         TEXT NOT NULL,
    category          TEXT NOT NULL,
    lane_count        INTEGER NOT NULL,
    query_hash        TEXT,
    query_preview     TEXT,
    total_cost_usd    REAL,
    wall_time_seconds REAL,
    routing_reason    TEXT,
    stakes_level      TEXT
);

CREATE TABLE IF NOT EXISTS lane_results (
    run_id            TEXT NOT NULL,
    model_id          TEXT NOT NULL,
    codename          TEXT,
    status            TEXT NOT NULL,
    elapsed_seconds   REAL,
    prompt_tokens     INTEGER,
    completion_tokens INTEGER,
    cost_usd          REAL,
    heuristic_score   REAL,
    is_outlier        INTEGER DEFAULT 0,
    score_breakdown   TEXT,
    PRIMARY KEY (run_id, model_id)
);

CREATE TABLE IF NOT EXISTS daily_spend (
    date       TEXT PRIMARY KEY,
    total_usd  REAL DEFAULT 0,
    run_count  INTEGER DEFAULT 0
);
"""


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create schema and seed model registry from models.json."""
    with get_conn() as conn:
        conn.executescript(SCHEMA)

    if not MODELS_FILE.exists():
        return
    data = json.loads(MODELS_FILE.read_text())
    all_lanes = data.get("core_lanes", []) + data.get("expansion_lanes", [])
    with get_conn() as conn:
        existing = {r["model_id"] for r in conn.execute("SELECT model_id FROM models")}
        for lane in all_lanes:
            if lane["id"] not in existing:
                conn.execute(
                    "INSERT OR IGNORE INTO models VALUES (?,?,?,?,?,?)",
                    (lane["id"], lane["codename"], lane["id"].split("/")[0],
                     lane["prompt_cost_per_m"], lane["completion_cost_per_m"],
                     1 if lane.get("enabled", True) else 0)
                )


# ── Thompson Sampling ──────────────────────────────────────────────────────────

def _sample(model_id: str, category: str, conn: sqlite3.Connection) -> float:
    """Draw one sample from Beta(alpha, beta) posterior for this model+category."""
    row = conn.execute(
        "SELECT alpha, beta FROM model_ratings WHERE model_id=? AND category=?",
        (model_id, category)
    ).fetchone()
    a = row["alpha"] if row else 2.0
    b = row["beta"]  if row else 2.0
    g1 = random.gammavariate(a, 1.0)
    g2 = random.gammavariate(b, 1.0)
    return g1 / (g1 + g2)


def select_lanes(
    category: str,
    lane_count: int,
    available_model_ids: list[str],
    speed_biased: bool = False,
) -> tuple[list[str], list[dict]]:
    """
    Thompson Sampling lane selection.
    Returns (ordered_model_ids, debug_info_list).
    speed_biased=True applies SPEED_BONUS adjustments (used for trading).
    Family diversity: at most 1 model per provider unless forced.
    """
    init_db()
    with get_conn() as conn:
        scores = {}
        for mid in available_model_ids:
            score = _sample(mid, category, conn)
            if speed_biased and mid in SPEED_BONUS:
                score = max(0.0, min(1.0, score + SPEED_BONUS[mid]))
            scores[mid] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    selected: list[str] = []
    family_counts: dict[str, int] = {}
    debug: list[dict] = []

    for mid, score in ranked:
        family = mid.split("/")[0]
        if len(selected) < lane_count:
            if family_counts.get(family, 0) < 1 or len(ranked) <= lane_count:
                selected.append(mid)
                family_counts[family] = family_counts.get(family, 0) + 1
                debug.append({"model_id": mid, "sample_score": round(score, 4)})

    # Fill any remaining slots (diversity constraint left gaps)
    for mid, score in ranked:
        if len(selected) >= lane_count:
            break
        if mid not in selected:
            selected.append(mid)
            debug.append({"model_id": mid, "sample_score": round(score, 4), "diversity_override": True})

    return selected[:lane_count], debug


# ── Scoring & Rating Update ────────────────────────────────────────────────────

def score_lane(response: Optional[str], all_responses: list[Optional[str]], query: str) -> tuple[float, dict]:
    """
    Heuristic quality score [0–1].
    50% consensus word-overlap, 30% consistency, 20% query coverage.
    Explicit non-signals: length, latency.
    """
    if not response:
        return 0.0, {"consensus": 0.0, "consistency": 0.0, "coverage": 0.0, "note": "no_response"}

    # Consensus: Jaccard overlap against other successful responses
    others = [r for r in all_responses if r and r != response]
    if others:
        my_words = set(response.lower().split())
        overlaps = []
        for o in others:
            ow = set(o.lower().split())
            union = my_words | ow
            overlaps.append(len(my_words & ow) / len(union) if union else 0)
        consensus = sum(overlaps) / len(overlaps)
    else:
        consensus = 0.5

    # Consistency: penalize obvious self-contradictions
    rl = response.lower()
    contradictions = sum(1 for a, b in [
        ("always", "never"), ("buy", "sell"), ("increase", "decrease"), ("do ", "don't ")
    ] if a in rl and b in rl)
    consistency = max(0.4, 1.0 - contradictions * 0.2)

    # Coverage: words per query sub-question (≥150 = full)
    parts = max(1, query.count("?") + query.count("\n-") + query.count("\nA.") + query.count("\nB."))
    coverage = min(1.0, (len(response.split()) / parts) / 150)

    final = 0.50 * consensus + 0.30 * consistency + 0.20 * coverage
    breakdown = {
        "consensus": round(consensus, 3),
        "consistency": round(consistency, 3),
        "coverage": round(coverage, 3),
        "final": round(final, 3),
    }
    return round(final, 4), breakdown


def _update_pair(mid_a: str, mid_b: str, category: str, outcome: float, conn: sqlite3.Connection) -> None:
    """Update Beta distributions for one pairwise comparison. outcome: 1=A wins, 0=B wins, 0.5=tie."""
    def get(mid):
        r = conn.execute(
            "SELECT alpha, beta FROM model_ratings WHERE model_id=? AND category=?",
            (mid, category)
        ).fetchone()
        return (r["alpha"], r["beta"]) if r else (2.0, 2.0)

    def put(mid, a, b):
        conn.execute(
            """INSERT INTO model_ratings (model_id, category, alpha, beta, runs, last_run_at)
               VALUES (?,?,?,?,1,?) ON CONFLICT(model_id,category) DO UPDATE SET
               alpha=excluded.alpha, beta=excluded.beta, runs=runs+1, last_run_at=excluded.last_run_at""",
            (mid, category, a, b, datetime.utcnow().isoformat())
        )

    aa, ab = get(mid_a)
    ba, bb = get(mid_b)
    if outcome == 1.0:
        put(mid_a, aa + 1, ab);  put(mid_b, ba, bb + 1)
    elif outcome == 0.0:
        put(mid_a, aa, ab + 1);  put(mid_b, ba + 1, bb)
    else:
        put(mid_a, aa + 0.5, ab + 0.5);  put(mid_b, ba + 0.5, bb + 0.5)


def record_run(
    run_id: str, category: str, lane_count: int, query: str,
    total_cost_usd: float, wall_time_seconds: float,
    routing_reason: str, stakes_level: str, lane_results: list[dict],
) -> None:
    """Record a run and update Bayesian ratings. Called by runner.py after all lanes complete."""
    init_db()
    qhash = hashlib.sha256(query.lower().strip().encode()).hexdigest()[:16]
    today = datetime.utcnow().strftime("%Y-%m-%d")

    with get_conn() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO runs VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (run_id, datetime.utcnow().isoformat(), category, lane_count, qhash,
             query[:120].replace("\n", " "), total_cost_usd, wall_time_seconds,
             routing_reason, stakes_level)
        )
        conn.execute(
            """INSERT INTO daily_spend VALUES (?,?,1) ON CONFLICT(date) DO UPDATE SET
               total_usd=total_usd+excluded.total_usd, run_count=run_count+1""",
            (today, total_cost_usd)
        )

        all_responses = [r.get("response") for r in lane_results if r.get("status") == "success"]
        scored = []
        for r in lane_results:
            s, breakdown = score_lane(r.get("response"), all_responses, query)
            conn.execute(
                """INSERT OR IGNORE INTO lane_results VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (run_id, r["model_id"], r["codename"], r["status"],
                 r.get("elapsed_seconds"), r.get("prompt_tokens"),
                 r.get("completion_tokens"), r.get("cost_usd"),
                 s, r.get("is_outlier", 0), json.dumps(breakdown))
            )
            if r.get("status") == "success":
                scored.append((r["model_id"], s))

        # All pairwise comparisons to update Beta ratings
        for i in range(len(scored)):
            for j in range(i + 1, len(scored)):
                mid_a, sa = scored[i]
                mid_b, sb = scored[j]
                diff = sa - sb
                outcome = 1.0 if diff > 0.15 else (0.0 if diff < -0.15 else 0.5)
                _update_pair(mid_a, mid_b, category, outcome, conn)


# ── ChromaDB Semantic Cache ────────────────────────────────────────────────────

def _get_collection():
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        return client.get_or_create_collection(
            "urithiru_cache", embedding_function=ef, metadata={"hnsw:space": "cosine"}
        )
    except Exception:
        return None


def cache_lookup(query: str, category: str) -> tuple[str, list[dict]]:
    """
    Returns ("hit"|"context"|"miss", list_of_matches).
    hit     → serve cached answer directly, skip API calls
    context → inject top-3 as RAG context into lane prompts
    miss    → run fresh
    """
    col = _get_collection()
    if col is None or col.count() == 0:
        return "miss", []

    try:
        res = col.query(query_texts=[query], n_results=min(5, col.count()),
                        include=["documents", "metadatas", "distances"])
    except Exception:
        return "miss", []

    hit_thresh = CACHE_HIT_THRESHOLD.get(category, 0.92)
    ctx_thresh = CONTEXT_THRESHOLD.get(category, 0.84)
    ttl = CACHE_TTL.get(category, 604_800)
    now = datetime.utcnow()

    hits, ctx = [], []
    for dist, meta, doc in zip(
        res["distances"][0], res["metadatas"][0], res["documents"][0]
    ):
        sim = 1.0 - dist
        try:
            age = (now - datetime.fromisoformat(meta.get("timestamp", "2000-01-01"))).total_seconds()
            if age > ttl:
                continue
        except Exception:
            continue

        entry = {"answer": doc, "similarity": round(sim, 4), "timestamp": meta.get("timestamp", "")}
        if sim >= hit_thresh:
            hits.append(entry)
        elif sim >= ctx_thresh:
            ctx.append(entry)

    if hits:
        return "hit", hits[:1]
    if ctx:
        return "context", ctx[:3]
    return "miss", []


def cache_store(query: str, category: str, run_id: str, synthesis: str) -> bool:
    """Store a synthesis in ChromaDB for future cache lookups."""
    col = _get_collection()
    if col is None:
        return False
    try:
        doc_id = hashlib.sha256(f"{run_id}_{query[:80]}".encode()).hexdigest()[:20]
        col.upsert(
            ids=[doc_id],
            documents=[synthesis],
            metadatas=[{"query_preview": query[:200], "category": category,
                        "run_id": run_id, "timestamp": datetime.utcnow().isoformat()}]
        )
        return True
    except Exception as e:
        print(f"  ⚠️  Cache store failed: {e}")
        return False


# ── Stats Helpers ──────────────────────────────────────────────────────────────

def get_leaderboard(category: Optional[str] = None) -> list[dict]:
    init_db()
    with get_conn() as conn:
        q = "SELECT * FROM model_ratings" + (" WHERE category=?" if category else "") + \
            " ORDER BY category, (alpha/(alpha+beta)) DESC"
        rows = conn.execute(q, (category,) if category else ()).fetchall()
    result = []
    for r in rows:
        a, b = r["alpha"], r["beta"]
        mean = a / (a + b)
        unc = 2.0 * math.sqrt(mean * (1 - mean) / (a + b))
        result.append({"model_id": r["model_id"], "category": r["category"],
                       "win_rate": round(mean, 4), "uncertainty": round(unc, 4), "runs": r["runs"]})
    return result


def get_daily_spend(days: int = 7) -> list[dict]:
    init_db()
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM daily_spend WHERE date>=? ORDER BY date DESC", (cutoff,)
        )]


def get_routing_log(n: int = 20) -> list[dict]:
    init_db()
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM runs ORDER BY timestamp DESC LIMIT ?", (n,)
        )]


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Urithiru v2 tracker")
    p.add_argument("--init", action="store_true")
    p.add_argument("--stats", action="store_true")
    p.add_argument("--leaderboard", type=str, metavar="CATEGORY")
    p.add_argument("--spend", action="store_true")
    p.add_argument("--routing-log", action="store_true")
    args = p.parse_args()

    if args.init:
        init_db(); print(f"✅ {DB_PATH} initialized"); return

    if args.leaderboard:
        rows = get_leaderboard(args.leaderboard)
        print(f"\n🏆 LEADERBOARD — {args.leaderboard}\n")
        print(f"  {'#':<4} {'Model':<32} {'Win%':>7} {'±':>7} {'Runs':>6}")
        print(f"  {'─'*4} {'─'*32} {'─'*7} {'─'*7} {'─'*6}")
        for i, r in enumerate(rows, 1):
            flag = " ⚠️ low data" if r["runs"] < 10 else ""
            print(f"  {i:<4} {r['model_id']:<32} {r['win_rate']:>6.1%} {r['uncertainty']:>6.1%} {r['runs']:>6}{flag}")
        return

    if args.spend:
        rows = get_daily_spend(14)
        print(f"\n💰 DAILY SPEND\n")
        for r in rows:
            bar = "█" * min(int(r["total_usd"] * 50), 40)
            print(f"  {r['date']}  ${r['total_usd']:.4f}  ({r['run_count']} runs)  {bar}")
        return

    if args.routing_log:
        rows = get_routing_log(20)
        print(f"\n📋 ROUTING LOG\n")
        print(f"  {'#':<4} {'Run ID':<28} {'Cat':<9} {'Stakes':<10} {'Lanes':>5}  Reason")
        print(f"  {'─'*4} {'─'*28} {'─'*9} {'─'*10} {'─'*5}  {'─'*35}")
        for i, r in enumerate(rows, 1):
            print(f"  {i:<4} {r['run_id'][:26]:<28} {r['category']:<9} "
                  f"{(r['stakes_level'] or '?'):<10} {r['lane_count']:>5}  {(r['routing_reason'] or '')[:50]}")
        return

    if args.stats:
        init_db()
        with get_conn() as conn:
            runs = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
            spend = conn.execute("SELECT SUM(total_usd) FROM daily_spend").fetchone()[0] or 0
        print(f"\n🗼 TRACKER  DB={DB_PATH}  Runs={runs}  Spend=${spend:.4f}")
        return

    p.print_help()


if __name__ == "__main__":
    main()

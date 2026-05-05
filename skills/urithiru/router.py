#!/usr/bin/env python3
"""
router.py — Urithiru v2 Adaptive Lane Router
Classifies query stakes and determines optimal lane count.

The routing decision is:
  1. Detect category (auto or hint)
  2. Classify stakes level (critical/high/medium/low)
  3. Look up routing policy → min/max lanes
  4. Ask tracker.py for the best models via Thompson Sampling
"""

import re
from typing import Optional

# ── Stakes keyword maps (trading category) ───────────────────────────────────
# Checked in order — first match wins
TRADING_STAKES = [
    ("critical", [
        "execute", "buy to open", "sell to open", "buy to close", "sell to close",
        "enter position", "exit position", "place order", "submit order",
        "fill", "stop loss", "take profit", "position size", "how many contracts",
        "live trade", "real money", "going in",
    ]),
    ("high", [
        "setup", "entry point", "signal", "breakout", "conviction", "thesis",
        "risk/reward", "r/r", "should i buy", "should i sell", "would you take",
        "trade this", "what's the trade", "whats the trade",
    ]),
    ("medium", [
        "analysis", "looking at", "watching", "sector", "watchlist", "research",
        "what do you think", "thoughts on", "review this", "screen for",
    ]),
]

CODE_STAKES = [
    ("high", [
        "production", "deploy", "refactor", "architecture", "security",
        "race condition", "data loss", "migration", "live system",
    ]),
    ("medium", [
        "review", "debug", "fix", "optimize", "implement", "build",
    ]),
]

# ── Routing policy: (category, stakes) → (min_lanes, max_lanes, reason) ──────
# Trading defaults to 5-lane minimum at high stakes (fast lanes OK).
# Code gets 5 lanes on high-stakes production decisions.
ROUTING_TABLE: dict[tuple, tuple] = {
    ("trading",  "critical"): (7, 7, "Full tower — real money execution"),
    ("trading",  "high"):     (5, 5, "5 lanes — active trade decision (speed-biased)"),
    ("trading",  "medium"):   (3, 5, "3 lanes — analysis/setup review"),
    ("trading",  "low"):      (3, 3, "3 lanes — general market question"),
    ("code",     "high"):     (5, 7, "5 lanes — production/architecture decision"),
    ("code",     "medium"):   (3, 5, "3 lanes — code review/debug"),
    ("code",     "low"):      (3, 3, "3 lanes — quick code question"),
    ("writing",  "high"):     (5, 5, "5 lanes — content for publication"),
    ("writing",  "medium"):   (3, 3, "3 lanes — writing review"),
    ("writing",  "low"):      (3, 3, "3 lanes — quick writing question"),
    ("general",  "critical"): (5, 7, "5 lanes — high-stakes general decision"),
    ("general",  "high"):     (3, 5, "3 lanes — important question"),
    ("general",  "medium"):   (3, 3, "3 lanes — default"),
    ("general",  "low"):      (3, 3, "3 lanes — default"),
}

# User-facing trigger overrides (checked before auto-detection)
OVERRIDE_TRIGGERS = {
    # Stakes overrides
    "real money":         ("trading", "critical"),
    "live trade":         ("trading", "critical"),
    "going live":         ("trading", "critical"),
    "trading check":      ("trading", "high"),
    "trade this":         ("trading", "high"),
    "quick trading":      ("trading", "medium"),
    # Lane count overrides
    "quick check":        (None, "low"),
    "fast lane":          (None, "low"),
    "full tower":         (None, "critical"),   # forces 7 lanes via routing table
}


def detect_stakes(query: str, category: str) -> tuple[str, str]:
    """
    Detect stakes level from query content.
    Returns (stakes_level, detection_reason).
    Stakes: critical > high > medium > low
    """
    q = query.lower()

    # Check override triggers first
    for phrase, (cat_override, stakes_override) in OVERRIDE_TRIGGERS.items():
        if phrase in q:
            return stakes_override, f"trigger phrase: '{phrase}'"

    # Dollar amounts → at least high stakes
    if re.search(r"\$[\d,]+", query) or re.search(r"\d+\s*contracts", q):
        if category == "trading":
            return "high", "dollar amount or contracts mentioned"

    # Category-specific keyword matching
    stakes_map = TRADING_STAKES if category == "trading" else (
        CODE_STAKES if category == "code" else []
    )
    for level, keywords in stakes_map:
        matched = [kw for kw in keywords if kw in q]
        if matched:
            return level, f"keywords: {matched[:3]}"

    return "low", "no high-stakes signals detected"


def detect_category(query: str, hint: Optional[str] = None) -> str:
    """Auto-detect category from query content, with optional user hint."""
    if hint and hint in ("code", "trading", "writing", "general"):
        return hint

    q = query.lower()
    trading_signals = [
        "stock", "option", "spy", "qqq", "iwm", "dia", "aapl", "tsla", "nvda", "msft",
        "call", "put", "strike", "expiry", "expiration",
        "delta", "theta", "gamma", "vega", "vix", "iv", "implied volatility",
        "market", "ticker", "trade", "position",
        "buy", "sell", "bull", "bear", "chart", "support", "resistance",
        "breakout", "breakdown", "entry", "exit", "profit", "loss", "portfolio",
        "setup", "signal", "alert", "scanner", "screener",
        "wheel", "covered call", "cash secured", "iron condor", "spread",
    ]
    code_signals = [
        "def ", "function", "class ", "import ", "```", "error:", "traceback",
        "python", "typescript", "javascript", "sql", "api", "docker", "git",
        "bug", "fix this", "code", "implement", "refactor", "debug",
    ]
    writing_signals = [
        "substack", "write", "draft", "post", "article", "blog", "email",
        "paragraph", "sentence", "edit", "rewrite", "tone", "voice",
    ]

    trading_score = sum(1 for s in trading_signals if s in q)
    code_score = sum(1 for s in code_signals if s in q)
    writing_score = sum(1 for s in writing_signals if s in q)

    if code_score >= 2 and code_score >= trading_score:
        return "code"
    if trading_score >= 1:   # single strong trading signal (ticker + context) is enough
        return "trading"
    if writing_score >= 2:
        return "writing"
    if code_score == 1:
        return "code"
    return "general"


def get_routing_decision(
    query: str,
    category_hint: Optional[str] = None,
    lane_hint: Optional[int] = None,
    stakes_hint: Optional[str] = None,
) -> dict:
    """
    Main routing function. Returns a routing decision dict:
    {
        "category": str,
        "stakes": str,
        "stakes_reason": str,
        "lane_count": int,
        "routing_reason": str,
        "speed_biased": bool,   # whether Thompson Sampling uses speed bonus
    }

    lane_hint overrides the routing table if provided (explicit --lanes flag).
    stakes_hint overrides auto-detection if provided.
    """
    category = detect_category(query, category_hint)
    stakes, stakes_reason = (stakes_hint, "user override") if stakes_hint else detect_stakes(query, category)

    # Look up routing policy
    policy_key = (category, stakes)
    min_lanes, max_lanes, policy_reason = ROUTING_TABLE.get(
        policy_key, (3, 3, "3 lanes — default fallback")
    )

    # lane_hint overrides policy (explicit user request)
    if lane_hint:
        lane_count = lane_hint
        routing_reason = f"user override ({lane_hint} lanes)"
    else:
        lane_count = min_lanes
        routing_reason = policy_reason

    # Speed bias: active for trading to prioritize Grok-4-fast
    speed_biased = (category == "trading")

    return {
        "category": category,
        "stakes": stakes,
        "stakes_reason": stakes_reason,
        "lane_count": lane_count,
        "routing_reason": routing_reason,
        "speed_biased": speed_biased,
        "policy_min": min_lanes,
        "policy_max": max_lanes,
    }


def format_routing_header(decision: dict, selected_models: list[dict]) -> str:
    """Format the pre-flight routing display printed before API calls."""
    lines = [
        f"\n🗼 Urithiru AUTO-ROUTE | {decision['category'].upper()} / {decision['stakes'].upper()} STAKES",
        f"   Stakes detected: {decision['stakes'].upper()} ({decision['stakes_reason']})",
        f"   Lane count: {decision['lane_count']} ({decision['routing_reason']})",
    ]
    if selected_models:
        lines.append("   Thompson Sampling selection:")
        for i, m in enumerate(selected_models, 1):
            speed_note = " ⚡ speed bonus" if m.get("speed_bonus") else ""
            div_note = " [diversity override]" if m.get("diversity_override") else ""
            lines.append(f"     Lane {i}: [{m['codename']:12s}] sample={m['sample_score']:.4f}{speed_note}{div_note}")
    if decision["speed_biased"]:
        lines.append("   ⚡ Speed-biased selection active (trading mode)")
    lines.append("")
    return "\n".join(lines)

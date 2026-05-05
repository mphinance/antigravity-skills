#!/usr/bin/env python3
"""
outlier_detector.py — Pre-synthesis outlier guard for Urithiru v2
Detects lane responses that diverge significantly from group consensus
before they can be averaged into the synthesis.

Uses sentence-transformers (all-MiniLM-L6-v2, same model as ChromaDB cache)
for fast local embedding comparison. No API calls.

Usage:
    from outlier_detector import detect_outliers
    result = detect_outliers(lane_results)
"""

from __future__ import annotations

import math
from typing import Optional


def _cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def detect_outliers(
    lane_results: list[dict],
    std_threshold: float = 2.0,
    min_sim_threshold: float = 0.55,
) -> dict:
    """
    Detect outlier lane responses before synthesis.

    A lane is flagged as an outlier if its cosine similarity to the group
    centroid is more than `std_threshold` standard deviations below the mean,
    OR below the hard floor `min_sim_threshold`.

    Args:
        lane_results: list of lane result dicts (from runner.py).
                      Must have 'response', 'codename', 'model_id', 'status'.
        std_threshold: how many std devs below mean = outlier (default 2.0)
        min_sim_threshold: hard floor — always flag if sim < this (default 0.55)

    Returns:
        {
            "outliers": [{"codename", "model_id", "similarity_to_centroid", "deviation"}],
            "consensus_score": float,     # mean pairwise similarity [0–1]
            "checked": int,               # number of responses checked
            "skipped": int,               # lanes with no response
            "available": bool,            # False if sentence-transformers not installed
        }
    """
    # Only check successful responses with content
    valid = [
        r for r in lane_results
        if r.get("status") == "success" and r.get("response")
    ]
    skipped = len(lane_results) - len(valid)

    if len(valid) < 2:
        return {
            "outliers": [],
            "consensus_score": 1.0 if len(valid) == 1 else 0.0,
            "checked": len(valid),
            "skipped": skipped,
            "available": True,
            "note": "< 2 valid responses — outlier detection skipped",
        }

    # Try to get embeddings — graceful fallback if not installed
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [r["response"][:2048] for r in valid]   # cap to keep it fast
        embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        embeddings = [list(map(float, e)) for e in embeddings]
        available = True
    except ImportError:
        return {
            "outliers": [],
            "consensus_score": None,
            "checked": len(valid),
            "skipped": skipped,
            "available": False,
            "note": "sentence-transformers not installed — run: pip install sentence-transformers",
        }
    except Exception as e:
        return {
            "outliers": [],
            "consensus_score": None,
            "checked": len(valid),
            "skipped": skipped,
            "available": False,
            "note": f"embedding failed: {e}",
        }

    # Compute centroid (mean of all embeddings)
    n = len(embeddings)
    dim = len(embeddings[0])
    centroid = [sum(embeddings[i][d] for i in range(n)) / n for d in range(dim)]
    # Normalize centroid
    mag = math.sqrt(sum(x * x for x in centroid))
    if mag > 0:
        centroid = [x / mag for x in centroid]

    # Similarity of each response to centroid
    sims = [_cosine(e, centroid) for e in embeddings]
    mean_sim = sum(sims) / len(sims)
    variance = sum((s - mean_sim) ** 2 for s in sims) / len(sims)
    std_sim = math.sqrt(variance) if variance > 0 else 0.0

    # Pairwise similarity for consensus score
    pair_sims = []
    for i in range(n):
        for j in range(i + 1, n):
            pair_sims.append(_cosine(embeddings[i], embeddings[j]))
    consensus_score = sum(pair_sims) / len(pair_sims) if pair_sims else 1.0

    # Flag outliers
    outliers = []
    for i, (r, sim) in enumerate(zip(valid, sims)):
        deviation = (mean_sim - sim) / std_sim if std_sim > 0 else 0.0
        is_outlier = (deviation > std_threshold) or (sim < min_sim_threshold)
        if is_outlier:
            outliers.append({
                "codename": r["codename"],
                "model_id": r["model_id"],
                "similarity_to_centroid": round(sim, 4),
                "deviation_std": round(deviation, 2),
                "response_preview": (r.get("response") or "")[:150],
            })

    return {
        "outliers": outliers,
        "consensus_score": round(consensus_score, 4),
        "mean_centroid_sim": round(mean_sim, 4),
        "std_centroid_sim": round(std_sim, 4),
        "per_lane_sims": {
            valid[i]["codename"]: round(sims[i], 4) for i in range(n)
        },
        "checked": len(valid),
        "skipped": skipped,
        "available": True,
    }


def format_outlier_report(result: dict) -> str:
    """Format outlier detection result for display before synthesis."""
    if not result.get("available"):
        return f"  🔍 Outlier check skipped: {result.get('note', 'unavailable')}"

    lines = ["\n🔍 Outlier Detection (pre-synthesis):"]

    if result.get("note"):
        lines.append(f"  ℹ️  {result['note']}")
        return "\n".join(lines)

    consensus = result.get("consensus_score")
    if consensus is not None:
        consensus_pct = f"{consensus:.0%}"
        if consensus >= 0.80:
            icon = "✅"
        elif consensus >= 0.65:
            icon = "⚠️"
        else:
            icon = "🚨"
        lines.append(f"  {icon} Board consensus: {consensus_pct}")

    sims = result.get("per_lane_sims", {})
    if sims:
        sim_parts = " | ".join(f"{k}: {v:.2f}" for k, v in sims.items())
        lines.append(f"  Centroid sims: {sim_parts}")

    if result["outliers"]:
        lines.append(f"\n  ⚠️  OUTLIERS FLAGGED ({len(result['outliers'])}):")
        for o in result["outliers"]:
            lines.append(
                f"    🚩 {o['codename']} — sim={o['similarity_to_centroid']:.3f}, "
                f"deviation={o['deviation_std']:.1f}σ"
            )
            lines.append(f"       Preview: \"{o['response_preview'][:100]}...\"")
            lines.append(f"       → Excluded from synthesis weights. Shown in Board Dissent.")
    else:
        checked = result.get("checked", 0)
        lines.append(f"  ✅ No outliers — {checked} lanes in consensus")

    return "\n".join(lines)

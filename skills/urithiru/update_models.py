#!/usr/bin/env python3
"""
update_models.py — Refresh models.json from live OpenRouter API.
Run this periodically to keep model IDs and pricing current.

Usage: python3 update_models.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

MODELS_FILE = Path(__file__).parent / "models.json"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# The models we care about — map from OR ID to our metadata
LANE_TARGETS = {
    # Core lanes
    "openai/gpt-5": {"codename": "Lola", "lane": 1},
    "anthropic/claude-sonnet-4.6": {"codename": "Stormfather", "lane": 2},
    "google/gemini-2.5-pro": {"codename": "Navani", "lane": 3},
    "x-ai/grok-4-fast": {"codename": "Wit", "lane": 4},
    "deepseek/deepseek-v4-pro": {"codename": "Pattern", "lane": 5},
    # Expansion lanes
    "qwen/qwen3-235b-a22b": {"codename": "Shallan", "lane": 6},
    "mistralai/mistral-large-2512": {"codename": "Adolin", "lane": 7},
}


def fetch_models() -> list[dict]:
    """Fetch model list from OpenRouter."""
    try:
        import urllib.request
        with urllib.request.urlopen(OPENROUTER_MODELS_URL, timeout=30) as resp:
            return json.load(resp).get("data", [])
    except Exception as e:
        print(f"Failed to fetch from OpenRouter: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    print(f"Fetching models from OpenRouter...")
    all_models = fetch_models()
    print(f"  Got {len(all_models)} models")

    # Index by ID
    model_index = {m["id"]: m for m in all_models}

    current = json.loads(MODELS_FILE.read_text())
    updated_core = []
    updated_expansion = []
    warnings = []

    for model_id, meta in LANE_TARGETS.items():
        if model_id not in model_index:
            warnings.append(f"⚠️  {model_id} [{meta['codename']}] NOT FOUND on OpenRouter — may be renamed or removed")
            continue

        m = model_index[model_id]
        pricing = m.get("pricing", {})
        prompt_cost = float(pricing.get("prompt", "0")) * 1_000_000
        completion_cost = float(pricing.get("completion", "0")) * 1_000_000
        ctx = m.get("context_length", 0)

        # Find existing lane data to preserve our custom fields
        lane_num = meta["lane"]
        all_existing = current.get("core_lanes", []) + current.get("expansion_lanes", [])
        existing = next((x for x in all_existing if x.get("lane") == lane_num), {})

        updated = {
            "lane": lane_num,
            "id": model_id,
            "codename": meta["codename"],
            "role": existing.get("role", m.get("description", "")),
            "strength": existing.get("strength", ""),
            "weakness": existing.get("weakness", ""),
            "prompt_cost_per_m": round(prompt_cost, 4),
            "completion_cost_per_m": round(completion_cost, 4),
            "context_length": ctx,
            "enabled": existing.get("enabled", True),
        }

        old_prompt = existing.get("prompt_cost_per_m")
        if old_prompt and abs(old_prompt - updated["prompt_cost_per_m"]) > 0.01:
            print(f"  💰 {meta['codename']} pricing changed: ${old_prompt:.2f} → ${updated['prompt_cost_per_m']:.2f}/M")

        if lane_num <= 5:
            updated_core.append(updated)
        else:
            updated_expansion.append(updated)

    updated_core.sort(key=lambda x: x["lane"])
    updated_expansion.sort(key=lambda x: x["lane"])

    current["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    current["core_lanes"] = updated_core
    current["expansion_lanes"] = updated_expansion

    MODELS_FILE.write_text(json.dumps(current, indent=2))
    print(f"\n✅ models.json updated — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"   Core lanes: {len(updated_core)}/5")
    print(f"   Expansion lanes: {len(updated_expansion)}/2")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  {w}")


if __name__ == "__main__":
    main()

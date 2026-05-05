# Urithiru v2

> *"The tower at the center of the world. All the Oathgates lead here."*

Multi-lane AI verification system. When you say **"run this through Urithiru"**, your query fans out to multiple AI models simultaneously via OpenRouter. Each model is a specialist. Antigravity reads all outputs and synthesizes the best answer.

---

## What's New in v2

v2 transitions Urithiru from a static fan-out script into an intelligent, adaptive orchestration engine optimized for trading and high-stakes synthesis:

1. **Adaptive Lane Router**: `--auto` detects query "stakes" (critical, high, medium, low) via keywords and dynamically assigns the right number of lanes (from 3 to 7).
2. **Bayesian Model Tracker**: Powered by Thompson Sampling (SQLite `tracker.db`), Urithiru tracks model performance per-category over time. Better performing models get selected more often, with a speed-bias applied specifically to trading queries.
3. **Semantic Cache**: Integrated ChromaDB embeds and caches queries. Semantically similar queries return cached results instantly, drastically reducing OpenRouter costs.
4. **Pre-Synthesis Outlier Guard**: Uses `sentence-transformers` to embed all lane responses before synthesis. Any response > 2σ away from the group consensus is flagged and excluded to prevent hallucination laundering.

---

## Quick Start

```bash
# Install v2 dependencies
pip install aiohttp chromadb sentence-transformers

export OPENROUTER_API_KEY=sk-or-v1-...

# Adaptive Auto-Routing (v2 Recommended)
python3 runner.py --query "AAPL 0DTE entry setup" --auto

# Hardcoded 5-lane run
python3 runner.py --query "your question" --category code

# Full tower (7 lanes)
python3 runner.py --query "your question" --lanes 7 --category trading

# Dry run — see routing config, stakes, and outlier logic without calling APIs
python3 runner.py --query "AAPL setup" --auto --dry-run
```

---

## The Lanes

### Core — always run (if not using --auto)

| # | Codename | Model | Role | $/M in/out |
|---|----------|-------|------|------------|
| 1 | **Lola** | `openai/gpt-5` | Clean, readable baseline | $1.25/$10.00 |
| 2 | **Stormfather** | `anthropic/claude-sonnet-4.6` | Edge cases, risk, error handling | $3.00/$15.00 |
| 3 | **Navani** | `google/gemini-2.5-pro` | Theory-first, 1M context | $1.25/$10.00 |
| 4 | **Wit** | `x-ai/grok-4-fast` | Fast, concise, type-safe, 2M ctx | $0.20/$0.50 |
| 5 | **Pattern** | `deepseek/deepseek-v4-pro` | Mathematical rigor, quant | $0.43/$0.87 |

### Expansion — "full tower" only (or via high stakes --auto)

| # | Codename | Model | Role | $/M in/out |
|---|----------|-------|------|------------|
| 6 | **Shallan** | `qwen/qwen3-235b-a22b` | Devil's advocate | $0.45/$1.82 |
| 7 | **Adolin** | `mistralai/mistral-large-2512` | Audit, security, direct | $0.50/$1.50 |

**Typical cost:** ~$0.09 (5 lanes) | ~$0.11 (7 lanes)

---

## Categories & Stakes

```
--category code      # Source code, functions, architecture
--category trading   # Strategies, signals, risk, backtests
--category writing   # Posts, docs, prose
--category general   # Everything else (default)
```

With `--auto`, the router detects stakes natively. You can also explicitly set them to override lane sizing:
```
--stakes critical    # Forces all 7 lanes (max confidence)
--stakes high        # 5 lanes
--stakes medium      # 3 lanes
--stakes low         # 1 lane (cache/fast fallback)
```

---

## File Structure

```
urithiru/
├── SKILL.md              # Antigravity's instructions
├── README.md             # This file
├── PROMPT_LIBRARY.md     # Study guide — read this
├── runner.py             # Parallel API caller + main entrypoint
├── router.py             # Adaptive stakes/routing engine
├── tracker.py            # Bayesian model tracker (Thompson Sampling) + Chroma cache
├── outlier_detector.py   # Pre-synthesis consensus guard (sentence-transformers)
├── tracker.db            # SQLite database for Bayesian model scores
├── update_models.py      # Refresh models.json
├── models.json           # Model catalog + pricing
├── .env                  # OPENROUTER_API_KEY
├── chroma_db/            # Semantic vector database
├── prompts/              # Per-model system prompts
└── logs/                 # JSONL trace per run
```

---

## Observability

### Local Logs (always on)
Every run writes `logs/urithiru_YYYY-MM-DD_HHMMSS_category.jsonl` with:
- Full query, routing decision, outlier analysis, lane responses, token counts, cost, and timings.

### Langfuse (optional, recommended)

Langfuse is open-source LLM observability. For Urithiru specifically it gives you:
- **Parallel trace visualization** — see all lanes fire simultaneously with exact timings
- **Cost tracking over time** — how much per category, per week?
- **Prompt versioning** — did changing Stormfather's prompt improve edge case detection?
- **Side-by-side lane comparison** — one UI, all responses

**Self-host with Docker Compose (~5 min):**
```bash
git clone https://github.com/langfuse/langfuse && cd langfuse
docker compose up -d
# UI: http://localhost:3000
```

**Enable in Urithiru:**
```bash
export LANGFUSE_PUBLIC_KEY=pk-lf-...
export LANGFUSE_SECRET_KEY=sk-lf-...
export LANGFUSE_HOST=http://localhost:3000
pip install langfuse
```

That's it — no code changes. Every run auto-sends traces. Without those env vars, falls back to local JSONL silently.

---

## Keep Models Current

OpenRouter reprices and adds models constantly. Refresh monthly:
```bash
python3 update_models.py
```

---

## The Names

Stormlight Archive characters — because Urithiru is the tower where all Oathgates converge and all answers come together.

**Lola** = clear-eyed and dependable | **Stormfather** = warns you about danger | **Navani** = the scholar | **Wit** = sharpest mind, fewest words | **Pattern** = finds the mathematical truth | **Shallan** = sees what nobody else does | **Adolin** = reliable, direct, gets it done

You don't need to have read the books. The metaphor is the point.

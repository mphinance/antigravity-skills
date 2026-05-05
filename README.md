<div align="center">
  <h1>The Alpha Skills Suite</h1>
  <p><strong>105 Elite AI Agent Skills for Quant Trading, Market Intelligence, and Creative Production</strong></p>
  <p>
    <a href="https://github.com/mphinance/antigravity-skills/stargazers"><img src="https://img.shields.io/github/stars/mphinance/antigravity-skills?style=for-the-badge&color=ffd700" alt="Stars" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Agent_Skills-105-blue?style=for-the-badge" alt="105 Skills" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Optimized_For-Claude_%7C_Gemini-8a2be2?style=for-the-badge" alt="Optimized for Claude/Gemini" /></a>
  </p>
</div>

---

## 🧠 The "Aha!" Moment

AI agents like Claude Code and Gemini are only as good as the context you provide them. Out of the box, they are brilliant generalists. 

**This repository gives them a PhD in algorithmic trading and a master's in design.**

By dropping these `skills/` into your agent's workspace, you inject decades of domain expertise, algorithmic rigor, and aesthetic taste directly into their runtime. You aren't just getting scripts—you are getting autonomous agents capable of identifying market regimes, rewriting PineScript to Python, running full design critiques, and generating Substack-ready financial reports.

*Note: I ran a "Full Tower" audit across all 105 directories looking for redundancies to prune. Every single skill is structurally unique. Even seemingly overlapping skills (like Breadth vs. Uptrend analyzers) are intentionally decoupled, serving as independent, uncorrelated inputs for the downstream Druckenmiller Strategy Synthesizer.*

---

## 🚀 Quick Start

1. Clone this repository to your local machine.
2. Copy the `skills/` folder into your agent's skill directory (e.g., `~/.gemini/antigravity/skills/` or your Claude Code equivalent).
3. Start your agent. It will automatically detect and index its new capabilities.

**API Keys Required (for some skills):**
- `FMP_API_KEY`: Financial Modeling Prep (Free tier covers 90% of the screeners)
- `TRADIER_API_KEY`: Tradier Brokerage (For live options chains and position sizing)
- `OPENROUTER_API_KEY`: OpenRouter (For the `urithiru` multi-lane verification agent)

---

## 🔥 The Quant Trading Engine

*Built for traders, by traders. These skills automate the tedious parts of algorithmic research and protect you from your own biases.*

### 1. Strategy Optimization & Backtesting
The hardest part of algo trading isn't writing the strategy—it's proving it won't blow up in out-of-sample data.

| Skill | What It Does |
|-------|-------------|
| **[pine-to-python](skills/pine-to-python/)** | **[NEW]** Translates brittle TradingView PineScript into vectorized Python. Extracts parameters automatically for Optuna hyperparameter optimization. |
| **[quant-feature-engineer](skills/quant-feature-engineer/)** | **[NEW]** Renaissance Tech-style feature engineering. Build unified scoring models instead of isolated strategies. |
| **[ghost-auto-trader](skills/ghost-auto-trader/)** | **[NEW]** Deploy the Ghost Auto-Trader framework: TV webhook -> AI Gate -> Broker Execution for 0DTE options. |
| **[backtest-expert](skills/backtest-expert/)** | The "beat ideas to death" methodology. Enforces slippage modeling, bias prevention, and overfitting detection. |
| **[edge-strategy-reviewer](skills/edge-strategy-reviewer/)** | An LLM "Pessimistic Strategist". Evaluates strategy drafts for edge plausibility and execution realism. Issues PASS/REVISE/REJECT verdicts. |
| **[strategy-pivot-designer](skills/strategy-pivot-designer/)** | Detects when your Optuna optimization hits a local optimum and proposes structurally different strategy pivots. |
| **[signal-postmortem](skills/signal-postmortem/)** | Autopsies post-trade outcomes. Tracks false positives, regime mismatches, and missed opportunities. |
| **[diagnose](skills/diagnose/)** | Disciplined diagnosis loop for hard bugs and performance regressions in your trading bots. |

### 2. Market Intelligence & Regime Detection
*Credits: Methodologies adapted from TraderMonty, William O'Neil, and Mark Minervini.*

Before you deploy capital, you need to know what environment you are in.

| Skill | What It Does |
|-------|-------------|
| **[stanley-druckenmiller-investment](skills/stanley-druckenmiller-investment/)** | **The Crown Jewel.** Synthesizes 8 upstream signals (Breadth, Macro, FTDs, VCP, etc.) into a single 0-100 conviction score and allocation map. |
| **[us-market-bubble-detector](skills/us-market-bubble-detector/)** | Implements the Minsky/Kindleberger framework. Mechanically scores Put/Call, VIX, margin debt, and IPO data to detect structural bubbles. |
| **[market-breadth-analyzer](skills/market-breadth-analyzer/)** | Generates a 0-100 composite breadth score using public CSV data. |
| **[macro-regime-detector](skills/macro-regime-detector/)** | Detects structural 1-2 year regime shifts (Concentration / Broadening / Inflationary). |
| **[market-top-detector](skills/market-top-detector/)** | Tactical 2-8 week defensive timing using Distribution Days and defensive sector rotation. |
| **[ftd-detector](skills/ftd-detector/)** | Follow-Through Day (FTD) detector for bottom confirmation. |
| **[ibd-distribution-day-monitor](skills/ibd-distribution-day-monitor/)** | IBD-style distribution day counting, clustering, and invalidation tracking. |

### 3. The Edge Research Pipeline
An automated, end-to-end factory for finding alpha.

`edge-hint-extractor` ➡️ `edge-concept-synthesizer` ➡️ `edge-strategy-designer` ➡️ `edge-strategy-reviewer` ➡️ `edge-candidate-agent` ➡️ `edge-pipeline-orchestrator`

### 4. Advanced Stock Screening
| Skill | What It Does |
|-------|-------------|
| **[vcp-screener](skills/vcp-screener/)** | Minervini Volatility Contraction Pattern (VCP) scanner. Finds tight bases and volatility contraction in Stage 2 uptrends. |
| **[canslim-screener](skills/canslim-screener/)** | William O'Neil's CANSLIM methodology scanner. |
| **[pead-screener](skills/pead-screener/)** | Post-Earnings Announcement Drift (PEAD) detector. Finds red-candle pullbacks post-gap-up. |
| **[pair-trade-screener](skills/pair-trade-screener/)** | Statistical arbitrage. Finds cointegrated pairs, z-scores, and mean-reversion entries. |
| **[dividend-growth-pullback-screener](skills/dividend-growth-pullback-screener/)** | Finds 12%+ dividend growers experiencing temporary RSI oversold pullbacks. |

### 5. Options, Portfolio & Risk Management
| Skill | What It Does |
|-------|-------------|
| **[position-sizer](skills/position-sizer/)** | Calculates risk-based sizing using Kelly Criterion, ATR scaling, and sector heat checks. |
| **[options-strategy-advisor](skills/options-strategy-advisor/)** | Black-Scholes pricing, Greeks calculation, and P/L simulation for complex options structures. |
| **[portfolio-manager](skills/portfolio-manager/)** | Connects to your broker to analyze asset allocation, risk metrics, and generate rebalancing logic. |
| **[trader-memory-core](skills/trader-memory-core/)** | A state machine that tracks investment theses from idea generation to closed-trade MAE/MFE postmortems. |

### 6. Dividend & Income (Kanchi Method)
*Credits: Workflows adapted from the Kanchi Japanese investing methodology.*
- `kanchi-dividend-sop`: Full SOP for screening, entry planning, and monitoring.
- `kanchi-dividend-review-monitor`: Automated T1-T5 triggers for 8-K governance and dividend safety checks.
- `kanchi-dividend-us-tax-accounting`: US tax location optimization (Qualified vs Ordinary, REIT/BDC treatment).

---

## 🎨 Creative Production & Prototyping

Why just build algorithms when you can build the SaaS companies to sell them?
*Credits: UI structures inspired by Replit Slides and HyperFrames.*

### Web, Dashboards & Presentations
| Skill | What It Does |
|-------|-------------|
| **[dashboard](skills/dashboard/)** | Generates a single-file HTML admin/analytics dashboard with KPI cards and charts. |
| **[saas-landing](skills/saas-landing/)** | Generates a complete marketing page with hero, features, pricing, and CTAs. |
| **[replit-deck](skills/replit-deck/)** | Generates beautiful, horizontal-swipe pitch decks in the style of Replit. |
| **[guizang-ppt](skills/guizang-ppt/)** | E-magazine style horizontal HTML presentations with WebGL fluid backgrounds. |
| **[mobile-app](skills/mobile-app/)** | Generates pixel-accurate iPhone 15 Pro framed mobile prototypes. |

### Media Generation
| Skill | What It Does |
|-------|-------------|
| **[hyperframes](skills/hyperframes/)** | Creates programmable video compositions, audio-reactive visuals, and kinetic typography in HTML. |
| **[image-poster](skills/image-poster/)** | Connects to Flux/Midjourney to generate editorial-style posters and key art. |
| **[audio-jingle](skills/audio-jingle/)** | Connects to ElevenLabs/Suno to generate voiceovers, jingles, and SFX. |
| **[social-carousel](skills/social-carousel/)** | Generates cinematic, 3-card 1080x1080 social media carousels. |

---

## ⚙️ Agent Infrastructure & Workflow

*Credits: Agent communication protocols inspired by OpenClaw.*

| Skill | What It Does |
|-------|-------------|
| **[urithiru](skills/urithiru/)** | **Multi-lane AI verification.** Fans out complex queries to 5-7 models simultaneously (via OpenRouter) and synthesizes the consensus to prevent hallucinations. |
| **[skill-designer](skills/skill-designer/)** | Prompts the agent to write its own new skills following repo conventions. |
| **[dual-axis-skill-reviewer](skills/dual-axis-skill-reviewer/)** | Deterministic + LLM deep review of your skills. Gates PRs with a 0-100 quality score. |
| **[grill-me](skills/grill-me/)** | The agent interviews you relentlessly about an idea until the decision tree is fully mapped. |
| **[caveman](skills/caveman/)** | Forces the agent into ultra-compressed communication mode. Cuts token usage by ~75%. |

---

## 💼 Enterprise Consulting & Custom Integrations

The days of manual trading and generic ChatGPT prompts are over. If you are a hedge fund, prop desk, or SaaS founder looking to implement autonomous workflows, custom LLM strategy evaluators, or high-frequency data pipelines:

**[Link to your Substack / Newsletter]**  
**[Link to Consulting / Contact Info]**

*Built by [@mphinance](https://github.com/mphinance).*

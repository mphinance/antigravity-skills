<div align="center">
  <img src="assets/hero.png" alt="Alpha Skills Hero Image" width="100%" />
  <h1>The Alpha Skills Suite</h1>
  <p><strong>105 Elite AI Agent Skills for Quant Trading, Market Intelligence, and Creative Production</strong></p>
  <p>
    <a href="https://github.com/mphinance/antigravity-skills/stargazers"><img src="https://img.shields.io/github/stars/mphinance/antigravity-skills?style=for-the-badge&color=ffd700" alt="Stars" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Agent_Skills-105-blue?style=for-the-badge" alt="105 Skills" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Optimized_For-Claude_%7C_Gemini-8a2be2?style=for-the-badge" alt="Optimized for Claude/Gemini" /></a>
  </p>
</div>

---

## 📑 Table of Contents
- [🧠 The "Aha!" Moment](#-the-aha-moment)
- [🚀 Quick Start](#-quick-start)
- [🔥 The Quant Trading Engine](#-the-quant-trading-engine)
  - [1. Strategy Optimization & Backtesting](#1-strategy-optimization--backtesting)
  - [2. Market Intelligence & Regime Detection](#2-market-intelligence--regime-detection)
  - [3. The Edge Research Pipeline](#3-the-edge-research-pipeline)
  - [4. Advanced Stock Screening](#4-advanced-stock-screening)
  - [5. Options, Portfolio & Risk Management](#5-options-portfolio--risk-management)
  - [6. Dividend & Income (Kanchi Method)](#6-dividend--income-kanchi-method)
- [🎨 Creative Production & Prototyping](#-creative-production--prototyping)
  - [Web, Dashboards & Presentations](#web-dashboards--presentations)
  - [Content & Voice](#content--voice)
  - [Media Generation](#media-generation)
- [⚙️ Agent Infrastructure & Workflow](#️-agent-infrastructure--workflow)
- [💼 Enterprise Consulting & Custom Integrations](#-enterprise-consulting--custom-integrations)

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

### Content & Voice
| Skill | What It Does |
|-------|-------------|
| **[mph-substack-writer](skills/mph-substack-writer/)** | **[NEW]** Captures Michael's exact Substack writing style. Enforces hard rules (no em dashes, PG-13, recovery wisdom, no markdown tables). |

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
| **[portable-memory-core](skills/portable-memory-core/)** | **[NEW]** Enforces the One Brain protocol. A portable `.agent/` folder that tracks your preferences, context, and identity across all IDEs and CLI tools. *(Inspired by codejunkie99/agentic-stack)* |
| **[skill-warden](skills/skill-warden/)** | **[NEW]** Automates health and security audits of your `skills/` tree to find dead skills, conflicting triggers, and risky shell executions. *(Inspired by Fangcun-AI/SkillWard & runesleo/claude-skill-audit)* |
| **[mental-model-evaluator](skills/mental-model-evaluator/)** | **[NEW]** Forces a pause before execution and runs your proposed plan through rigorous mental models (Inversion, First Principles, Second-Order). *(Inspired by will2025btc/buffett-perspective & xixu-me/awesome-persona-distill-skills)* |
| **[skill-designer](skills/skill-designer/)** | Prompts the agent to write its own new skills following repo conventions. |
| **[dual-axis-skill-reviewer](skills/dual-axis-skill-reviewer/)** | Deterministic + LLM deep review of your skills. Gates PRs with a 0-100 quality score. |
| **[grill-me](skills/grill-me/)** | The agent interviews you relentlessly about an idea until the decision tree is fully mapped. |
| **[caveman](skills/caveman/)** | Forces the agent into ultra-compressed communication mode. Cuts token usage by ~75%. |

---

## 💼 Enterprise Consulting & Custom Integrations

The days of manual trading and generic ChatGPT prompts are over. If you are a hedge fund, prop desk, or SaaS founder looking to implement autonomous workflows, custom LLM strategy evaluators, or high-frequency data pipelines:

- **Newsletter & Deep Dives:** [mphinance.substack.com](https://mphinance.substack.com/)
- **Trading Tools:** [TraderDaddy Pro](https://www.traderdaddy.pro/?ref=8DUEMWAJ)
- **Support the Project:** [Buy me a coffee on Ko-fi](https://ko-fi.com/mphinance)

*Built by [@mphinance](https://github.com/mphinance).*


## 📚 Full Skills Directory

A complete index of all available skills in this repository.

| Skill | Description |
|-------|-------------|
| **[audio-jingle](skills/audio-jingle/)** | Audio generation skill — jingles, beds, voiceover, and sound effects.   Routes music requests to Suno V5 / Udio / Lyria, speech to MiniMax   TTS / FishAudio / ElevenLabs V3, and SFX to ElevenLabs SFX or   AudioCraft. Output is one MP3/WAV file saved to the project folder. |
| **[backtest-expert](skills/backtest-expert/)** | Expert guidance for systematic backtesting of trading strategies. Use when developing, testing, stress-testing, or validating quantitative trading strategies. Covers "beating ideas to death" methodology, parameter robustness testing, slippage modeling, bias prevention, and interpreting backtest results. Applicable when user asks about backtesting, strategy validation, robustness testing, avoiding overfitting, or systematic trading development. |
| **[blog-post](skills/blog-post/)** | A long-form article / blog post — masthead, hero image placeholder,   article body with figures and pull quotes, author byline, related posts.   Use when the brief asks for "blog", "article", "post", "essay", or   "case study". |
| **[breadth-chart-analyst](skills/breadth-chart-analyst/)** | This skill should be used when analyzing market breadth charts, specifically the S&P 500 Breadth Index (200-Day MA based) and the US Stock Market Uptrend Stock Ratio charts. Use this skill when the user provides breadth chart images for analysis, requests market breadth assessment, positioning strategy recommendations, or wants to understand medium-term strategic and short-term tactical market outlook based on breadth indicators. Also works WITHOUT chart images by fetching CSV data directly from public sources. All analysis and output are conducted in English. |
| **[breakout-trade-planner](skills/breakout-trade-planner/)** | Generate Minervini-style breakout trade plans from VCP screener output with worst-case risk calculation, portfolio heat management, and Alpaca-compatible order templates (stop-limit bracket for pre-placement, limit bracket for post-confirmation). Use when user has VCP screener results and wants actionable trade plans with entry/stop/target levels and position sizing. |
| **[canslim-screener](skills/canslim-screener/)** | Screen US stocks using William O'Neil's CANSLIM growth stock methodology. Use when user requests CANSLIM stock screening, growth stock analysis, momentum stock identification, or wants to find stocks with strong earnings and price momentum following O'Neil's investment system. |
| **[caveman](skills/caveman/)** | Ultra-compressed communication mode. Cuts token usage ~75% by dropping   filler, articles, and pleasantries while keeping full technical accuracy.   Use when user says "caveman mode", "talk like caveman", "use caveman",   "less tokens", "be brief", or invokes /caveman. |
| **[critique](skills/critique/)** | Run a 5-dimension expert design review on any HTML artifact in the   project — Philosophy / Visual hierarchy / Detail / Functionality /   Innovation, each scored 0–10. Outputs a single self-contained HTML   report with a radar chart, evidence-backed scores, and three lists:   Keep / Fix / Quick-wins. Use when the brief asks for a "design   review", "design critique", "5 维度评审", "design audit", or "what's   wrong with my design". |
| **[dashboard](skills/dashboard/)** | Admin / analytics dashboard in a single HTML file. Fixed left sidebar,   top bar with user/search, main grid of KPI cards and one or two charts.   Use when the brief asks for a "dashboard", "admin", "analytics", or   "control panel" screen. |
| **[data-quality-checker](skills/data-quality-checker/)** | Validate data quality in market analysis documents and blog articles before publication. Use when checking for price scale inconsistencies (ETF vs futures), instrument notation errors, date/day-of-week mismatches, allocation total errors, and unit mismatches. Supports English and Japanese content. Advisory mode -- flags issues as warnings for human review, not as blockers. |
| **[dating-web](skills/dating-web/)** | A consumer-feeling dating / matchmaking dashboard — left rail navigation,   ticker bar of community signals, headline KPIs, a 30-day mutual-matches   bar chart, and a match-rate trend block. Editorial typography, restrained   accent. Use when the brief asks for a "dating site", "matchmaking",   "community dashboard", "social network dashboard", or any consumer   product where the data is the story. |
| **[design-an-interface](skills/design-an-interface/)** | Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice". |
| **[design-brief](skills/design-brief/)** | Parse a structured design brief written in I-Lang protocol format into a   concrete design spec. Eliminates ambiguity from vague requests like   "make it professional" by requiring explicit dimensions: palette, typography,   layout, mood, density, and constraints.   Trigger keywords: "design brief", "create a design brief", "ilang brief", "structured brief". |
| **[diagnose](skills/diagnose/)** | Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression. |
| **[digital-eguide](skills/digital-eguide/)** | A two-spread digital e-guide preview — page 1 is a cover (display title,   author, "What's inside" stats, table of contents teaser); page 2 is a   spread (lesson body with pull-quote and a step list). Lifestyle / creator   brand tone. Use when the brief asks for an "e-guide", "digital guide",   "lookbook", "lead magnet", "creator guide", "playbook", "PDF guide",   or "电子指南". |
| **[dividend-growth-pullback-screener](skills/dividend-growth-pullback-screener/)** | Use this skill to find high-quality dividend growth stocks (12%+ annual dividend growth, 1.5%+ yield) that are experiencing temporary pullbacks, identified by RSI oversold conditions (RSI ≤40). This skill combines fundamental dividend analysis with technical timing indicators to identify buying opportunities in strong dividend growers during short-term weakness. |
| **[docs-page](skills/docs-page/)** | A documentation page — left nav, scrollable article body, right-rail   table of contents. Use when the brief mentions "docs", "documentation",   "guide", "API reference", or "tutorial". |
| **[downtrend-duration-analyzer](skills/downtrend-duration-analyzer/)** | Analyze historical downtrend durations and generate interactive HTML histograms showing typical correction lengths by sector and market cap. |
| **[dual-axis-skill-reviewer](skills/dual-axis-skill-reviewer/)** | Review skills in any project using a dual-axis method: (1) deterministic code-based checks (structure, scripts, tests, execution safety) and (2) LLM deep review findings. Use when you need reproducible quality scoring for `skills/*/SKILL.md`, want to gate merges with a score threshold (for example 90+), or need concrete improvement items for low-scoring skills. Works across projects via --project-root. |
| **[earnings-calendar](skills/earnings-calendar/)** | This skill retrieves upcoming earnings announcements for US stocks using the Financial Modeling Prep (FMP) API. Use this when the user requests earnings calendar data, wants to know which companies are reporting earnings in the upcoming week, or needs a weekly earnings review. The skill focuses on mid-cap and above companies (over $2B market cap) that have significant market impact, organizing the data by date and timing in a clean markdown table format. Supports multiple environments (CLI, Desktop, Web) with flexible API key management. |
| **[earnings-trade-analyzer](skills/earnings-trade-analyzer/)** | Analyze recent post-earnings stocks using a 5-factor scoring system (Gap Size, Pre-Earnings Trend, Volume Trend, MA200 Position, MA50 Position). Scores each stock 0-100 and assigns A/B/C/D grades. Use when user asks about earnings trade analysis, post-earnings momentum screening, earnings gap scoring, or finding best recent earnings reactions. |
| **[economic-calendar-fetcher](skills/economic-calendar-fetcher/)** | Fetch upcoming economic events and data releases using FMP API. Retrieve scheduled central bank decisions, employment reports, inflation data, GDP releases, and other market-moving economic indicators for specified date ranges (default: next 7 days). The script outputs raw JSON or text; the assistant filters, assesses impact, and generates the Markdown report. |
| **[edge-candidate-agent](skills/edge-candidate-agent/)** | Generate and prioritize US equity long-side edge research tickets from EOD observations, then export pipeline-ready candidate specs for trade-strategy-pipeline Phase I. Use when users ask to turn hypotheses/anomalies into reproducible research tickets, convert validated ideas into `strategy.yaml` + `metadata.json`, or preflight-check interface compatibility (`edge-finder-candidate/v1`) before running pipeline backtests. |
| **[edge-concept-synthesizer](skills/edge-concept-synthesizer/)** | Abstract detector tickets and hints into reusable edge concepts with thesis, invalidation signals, and strategy playbooks before strategy design/export. |
| **[edge-hint-extractor](skills/edge-hint-extractor/)** | Extract edge hints from daily market observations and news reactions, with optional LLM ideation, and output canonical hints.yaml for downstream concept synthesis and auto detection. |
| **[edge-pipeline-orchestrator](skills/edge-pipeline-orchestrator/)** | Orchestrate the full edge research pipeline from candidate detection through strategy design, review, revision, and export. Use when coordinating multi-stage edge research workflows end-to-end. |
| **[edge-signal-aggregator](skills/edge-signal-aggregator/)** | Aggregate and rank signals from multiple edge-finding skills (edge-candidate-agent, theme-detector, sector-analyst, institutional-flow-tracker) into a prioritized conviction dashboard with weighted scoring, deduplication, and contradiction detection. |
| **[edge-strategy-designer](skills/edge-strategy-designer/)** | Convert abstract edge concepts into strategy draft variants and optional exportable ticket YAMLs for edge-candidate-agent export/validation. |
| **[edge-strategy-reviewer](skills/edge-strategy-reviewer/)** | Critically review strategy drafts from edge-strategy-designer for edge   plausibility, overfitting risk, sample size adequacy, and execution realism.   Use when strategy_drafts/*.yaml exists and needs quality gate before pipeline   export. Outputs PASS/REVISE/REJECT verdicts with confidence scores. |
| **[edit-article](skills/edit-article/)** | Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft. |
| **[email-marketing](skills/email-marketing/)** | A brand product-launch email — masthead with wordmark, hero image block,   headline lockup with skewed-italic accent, body copy, primary CTA, and a   specifications grid. Pure HTML email layout (centered single column, table   fallback). Use when the brief asks for an "email", "newsletter blast",   "MJML", "product launch email", or "email template". |
| **[eng-runbook](skills/eng-runbook/)** | An engineering runbook — service overview, alerts table, dashboards   links, common procedures with copy-pasteable commands, on-call rotation,   and an incident-response checklist. Use when the brief mentions   "runbook", "ops doc", "on-call guide", "SRE doc", or "运维手册". |
| **[exposure-coach](skills/exposure-coach/)** | Generate a one-page Market Posture summary with net exposure ceiling, growth-vs-value bias, participation breadth, and new-entry-allowed vs cash-priority recommendation by integrating signals from breadth, regime, and flow analysis skills. |
| **[finance-report](skills/finance-report/)** | Quarterly / monthly financial report — masthead with KPIs, revenue and   burn charts, P&L summary table, top-line highlights, and an outlook   paragraph. Use when the brief mentions "financial report", "Q3 report",   "MRR review", "P&L", or "财报". |
| **[finviz-screener](skills/finviz-screener/)** | Build and open FinViz screener URLs from natural language requests. Use when user wants to screen stocks, find stocks matching criteria, filter by fundamentals or technicals, or asks to open FinViz with specific conditions. Supports both Japanese and English input (e.g., "高配当で成長している小型株を探したい", "Find oversold large caps with high ROE"). |
| **[ftd-detector](skills/ftd-detector/)** | Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology. Dual-index tracking (S&P 500 + NASDAQ) with state machine for rally attempt, FTD qualification, and post-FTD health monitoring. Use when user asks about market bottom signals, follow-through days, rally attempts, re-entry timing after corrections, or whether it's safe to increase equity exposure. Complementary to market-top-detector (defensive) - this skill is offensive (bottom confirmation). |
| **[future-predictor](skills/future-predictor/)** | The Oracle. Anticipates your next moves, predicts market shifts, and tells you what   you will ask for next based on current codebase context and open files. |
| **[gamified-app](skills/gamified-app/)** | A multi-frame gamified mobile-app prototype — three phone frames on a dark   showcase stage. Frame 1: cover / poster, Frame 2: today's quests with XP   ribbons and a level bar, Frame 3: quest detail. Vivid quest tiles, level   ribbon, bottom tab bar. Use when the brief asks for a "gamified app",   "habit tracker", "RPG-style life app", "level-up app", "daily quests",   "XP / streak app", or "ELI5-style explainer app". |
| **[ghost-auto-trader](skills/ghost-auto-trader/)** | Architect and deploy the Ghost Auto-Trader framework: a zero-DTE options trading pipeline using TradingView webhooks, AI-gate validation, and broker execution. |
| **[grill-me](skills/grill-me/)** | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me". |
| **[grill-with-docs](skills/grill-with-docs/)** | Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions. |
| **[guizang-ppt](skills/guizang-ppt/)** | 生成"电子杂志 × 电子墨水"风格的横向翻页网页 PPT（单 HTML 文件），含 WebGL 流体背景、衬线标题 + 非衬线正文、章节幕封、数据大字报、图片网格等模板。当用户需要制作分享 / 演讲 / 发布会风格的网页 PPT，或提到"杂志风 PPT"、"horizontal swipe deck"、"editorial magazine"、"e-ink presentation"时使用。 |
| **[hr-onboarding](skills/hr-onboarding/)** | A new-hire onboarding plan as a single page — first week schedule,   buddy + manager intro, learning track, equipment checklist, and "you're   set when…" outcomes. Use when the brief mentions "onboarding",   "new hire", "first week plan", or "入职". |
| **[hyperframes](skills/hyperframes/)** | Create video compositions, animations, title cards, overlays, captions, voiceovers, audio-reactive visuals, and scene transitions in HyperFrames HTML. Use when asked to build any HTML-based video content, add captions or subtitles synced to audio, generate text-to-speech narration, create audio-reactive animation (beat sync, glow, pulse driven by music), add animated text highlighting (marker sweeps, hand-drawn circles, burst lines, scribble, sketchout), or add transitions between scenes (crossfades, wipes, reveals, shader transitions). Covers composition authoring, timing, media, and the full video production workflow. For CLI commands (init, lint, preview, render, transcribe, tts) see the hyperframes-cli skill. |
| **[ibd-distribution-day-monitor](skills/ibd-distribution-day-monitor/)** | Detect IBD-style Distribution Days for QQQ/SPY (close down at least 0.2% on higher volume), track 25-session expiration and 5% invalidation, count d5/d15/d25 clusters, classify market risk (NORMAL/CAUTION/HIGH/SEVERE), and emit TQQQ/QQQ exposure recommendations. Use after market close, before TQQQ exposure changes, or as input to FTD/market-state frameworks. Does not execute trades. |
| **[image-poster](skills/image-poster/)** | Single-image generation skill for posters, key art, and editorial   illustrations. Defaults to gpt-image-2 but is provider-agnostic — the   same workflow drives Flux, Imagen, or Midjourney via the active   upstream tooling. Output is one or more PNG/JPEG files saved to the   project folder. |
| **[improve-codebase-architecture](skills/improve-codebase-architecture/)** | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable. |
| **[institutional-flow-tracker](skills/institutional-flow-tracker/)** | Use this skill to track institutional investor ownership changes and portfolio flows using 13F filings data. Analyzes hedge funds, mutual funds, and other institutional holders to identify stocks with significant smart money accumulation or distribution. Helps discover stocks before major moves by following where sophisticated investors are deploying capital. |
| **[invoice](skills/invoice/)** | A printable invoice page — sender + recipient block, line items table,   tax breakdown, totals, and payment instructions. Use when the brief   mentions "invoice", "bill", "billing statement", or "发票". |
| **[kanban-board](skills/kanban-board/)** | Kanban / task board with columns (To do / In progress / In review / Done),   draggable-looking cards, assignee avatars, swimlanes, and a top filter   bar. Use when the brief mentions "kanban", "task board", "sprint board",   "trello", "看板". |
| **[kanchi-dividend-review-monitor](skills/kanchi-dividend-review-monitor/)** | Monitor dividend portfolios with Kanchi-style forced-review triggers (T1-T5) and convert anomalies into OK/WARN/REVIEW states without auto-selling. Use when users ask for 減配検知, 8-Kガバナンス監視, 配当安全性モニタリング, REVIEWキュー自動化, or periodic dividend risk checks. |
| **[kanchi-dividend-sop](skills/kanchi-dividend-sop/)** | Convert Kanchi-style dividend investing into a repeatable US-stock operating procedure. Use when users ask for かんち式配当投資, dividend screening, dividend growth quality checks, PERxPBR adaptation for US sectors, pullback limit-order planning, or one-page stock memo creation. Covers screening, deep dive, entry planning, and post-purchase monitoring cadence. |
| **[kanchi-dividend-us-tax-accounting](skills/kanchi-dividend-us-tax-accounting/)** | Provide US dividend tax and account-location workflow for Kanchi-style income portfolios. Use when users ask about qualified vs ordinary dividends, 1099-DIV interpretation, REIT/BDC distribution treatment, holding-period checks, or taxable-vs-IRA account placement decisions for dividend assets. |
| **[macro-regime-detector](skills/macro-regime-detector/)** | Detect structural macro regime transitions (1-2 year horizon) using cross-asset ratio analysis. Analyze RSP/SPY concentration, yield curve, credit conditions, size factor, equity-bond relationship, and sector rotation to identify regime shifts between Concentration, Broadening, Contraction, Inflationary, and Transitional states. Run when user asks about macro regime, market regime change, structural rotation, or long-term market positioning. |
| **[magazine-poster](skills/magazine-poster/)** | An editorial-style poster — newsprint paper, dateline, oversized serif   headline with a struck-through word and italic accent, a 2-column body   block, and 6 numbered sections with annotated pull-quote captions.   Reads like a Sunday-paper full-page essay or a thoughtful launch poster.   Use when the brief asks for "magazine poster", "editorial poster",   "newsprint", "essay layout", or "manifesto". |
| **[market-breadth-analyzer](skills/market-breadth-analyzer/)** | Quantifies market breadth health using TraderMonty's public CSV data. Generates a 0-100 composite score across 6 components (100 = healthy). No API key required. Use when user asks about market breadth, participation rate, advance-decline health, whether the rally is broad-based, or general market health assessment. |
| **[market-environment-analysis](skills/market-environment-analysis/)** | Comprehensive market environment analysis and reporting tool. Analyzes global markets including US, European, Asian markets, forex, commodities, and economic indicators. Provides risk-on/risk-off assessment, sector analysis, and technical indicator interpretation. Triggers on keywords like market analysis, market environment, global markets, trading environment, market conditions, investment climate, market sentiment, forex analysis, stock market analysis, 相場環境, 市場分析, マーケット状況, 投資環境. |
| **[market-news-analyst](skills/market-news-analyst/)** | This skill should be used when analyzing recent market-moving news events and their impact on equity markets and commodities. Use this skill when the user requests analysis of major financial news from the past 10 days, wants to understand market reactions to monetary policy decisions (FOMC, ECB, BOJ), needs assessment of geopolitical events' impact on commodities, or requires comprehensive review of earnings announcements from mega-cap stocks. The skill automatically collects news using WebSearch/WebFetch tools and produces impact-ranked analysis reports. All analysis thinking and output are conducted in English. |
| **[market-top-detector](skills/market-top-detector/)** | Detects market top probability using O'Neil Distribution Days, Minervini Leading Stock Deterioration, and Monty Defensive Sector Rotation. Generates a 0-100 composite score with risk zone classification. Use when user asks about market top risk, distribution days, defensive rotation, leadership breakdown, or whether to reduce equity exposure. Focuses on 2-8 week tactical timing signals for 10-20% corrections. |
| **[meeting-notes](skills/meeting-notes/)** | Meeting notes page — title bar with attendees, agenda checklist, decisions   block, action items table with owners + dates, and a "next meeting" footer.   Use when the brief mentions "meeting notes", "minutes", "1:1 notes",   "all-hands recap", or "会议纪要". |
| **[mental-model-evaluator](skills/mental-model-evaluator/)** | Applies multi-disciplinary cognitive frameworks (e.g., Inversion, First Principles,   Second-Order Thinking) to user plans and system designs to stress-test decisions. |
| **[mobile-app](skills/mobile-app/)** | A mobile-app screen rendered inside a pixel-accurate iPhone 15 Pro frame   on the page. Built by copying the seed `assets/template.html` and pasting   one screen archetype from `references/layouts.md`. Use when the brief asks   for "mobile app", "iOS app", "Android app", "phone screen", or "app UI". |
| **[mobile-onboarding](skills/mobile-onboarding/)** | A multi-screen mobile onboarding flow rendered as three phone frames   side by side — splash, value-prop, sign-in. Status bar, swipe dots,   primary CTA. Use when the brief mentions "mobile onboarding", "iOS   onboarding", "phone signup", or "移动端引导". |
| **[motion-frames](skills/motion-frames/)** | A single-frame motion-design composition with looping CSS animations —   rotating type ring, animated globe, ticking timer, parallax labels.   Renders as a hero video poster you can hand straight to HyperFrames or   any keyframe-based exporter. Use when the brief asks for "motion design",   "animated hero", "loop", "video poster", "title card", or pairs Open   Claude Design with HyperFrames for a kinetic export. |
| **[mph-substack-writer](skills/mph-substack-writer/)** | Write Substack articles in Michael Hanko's exact voice. Enforces strict styling rules (no em dashes, no markdown tables) and captures his irreverent, self-deprecating, recovery-infused tone. |
| **[options-strategy-advisor](skills/options-strategy-advisor/)** | Options trading strategy analysis and simulation tool. Provides theoretical pricing using Black-Scholes model, Greeks calculation, strategy P/L simulation, and risk management guidance. Use when user requests options strategy analysis, covered calls, protective puts, spreads, iron condors, earnings plays, or options risk management. Includes volatility analysis, position sizing, and earnings-based strategy recommendations. Educational focus with practical trade simulation. |
| **[pair-trade-screener](skills/pair-trade-screener/)** | Statistical arbitrage tool for identifying and analyzing pair trading opportunities. Detects cointegrated stock pairs within sectors, analyzes spread behavior, calculates z-scores, and provides entry/exit recommendations for market-neutral strategies. Use when user requests pair trading opportunities, statistical arbitrage screening, mean-reversion strategies, or market-neutral portfolio construction. Supports correlation analysis, cointegration testing, and spread backtesting. |
| **[pead-screener](skills/pead-screener/)** | Screen post-earnings gap-up stocks for PEAD (Post-Earnings Announcement Drift) patterns. Analyzes weekly candle formation to detect red candle pullbacks and breakout signals. Supports two input modes - FMP earnings calendar (Mode A) or earnings-trade-analyzer JSON output (Mode B). Use when user asks about PEAD screening, post-earnings drift, earnings gap follow-through, red candle breakout patterns, or weekly earnings momentum setups. |
| **[pine-to-python](skills/pine-to-python/)** | Translate TradingView PineScript strategies into vectorized Python strategies suitable for Optuna optimization and walk-forward analysis. |
| **[pm-spec](skills/pm-spec/)** | Product spec / PRD as a single page — problem, success metrics, scope,   user stories, design notes, rollout plan, open questions. Use when the   brief mentions "PRD", "spec", "product spec", "feature brief", or "需求文档". |
| **[portable-memory-core](skills/portable-memory-core/)** | A meta-skill that establishes a 'One Brain' portable memory folder (.agent/).   It persists context, user preferences, identity rules, and execution history    across different AI harnesses (Claude Code, Cursor, Windsurf, OpenClaw). |
| **[portfolio-manager](skills/portfolio-manager/)** | Comprehensive portfolio analysis using Alpaca MCP Server integration to fetch holdings and positions, then analyze asset allocation, risk metrics, individual stock positions, diversification, and generate rebalancing recommendations. Use when user requests portfolio review, position analysis, risk assessment, performance evaluation, or rebalancing suggestions for their brokerage account. |
| **[position-sizer](skills/position-sizer/)** | Calculate risk-based position sizes for long stock trades. Use when user asks about position sizing, how many shares to buy, risk per trade, Kelly criterion, ATR-based sizing, or portfolio risk allocation. Supports stop-loss distance calculation, volatility scaling, and sector concentration checks. |
| **[pricing-page](skills/pricing-page/)** | A standalone pricing page — header, plan tiers, feature comparison table,   and an FAQ. Use when the brief asks for "pricing", "plans",   "subscription tiers", or a "compare plans" page. |
| **[qa](skills/qa/)** | Interactive QA session where user reports bugs or issues conversationally, and the agent files GitHub issues. Explores the codebase in the background for context and domain language. Use when user wants to report bugs, do QA, file issues conversationally, or mentions "QA session". |
| **[quant-feature-engineer](skills/quant-feature-engineer/)** | Act as a Renaissance Tech-level quantitative systems engineer. Build unified feature engines instead of isolated strategies, rigorously test predictive variables, and assemble scoring models. |
| **[replit-deck](skills/replit-deck/)** | Single-file horizontal-swipe HTML deck in the style of Replit Slides's   landing-page template gallery. Eight distinct themes (helix, holm, vance,   bevel, world-dark, world-mint, atlas, bluehouse) — each a complete visual   system (palette + type + accent) captured from replit.com/slides. Pick one   theme, do not mix. For pitch decks, board reports, brand memos, campaign   reveals — when the user explicitly wants "Replit Slides style". |
| **[request-refactor-plan](skills/request-refactor-plan/)** | Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps. |
| **[saas-landing](skills/saas-landing/)** | Single-page SaaS landing with hero, features, social proof, pricing, and CTA.   Respects the active DESIGN.md color/typography/layout tokens.   Trigger keywords: "saas landing", "marketing page", "product landing". |
| **[scenario-analyzer](skills/scenario-analyzer/)** | ニュースヘッドラインを入力として18ヶ月シナリオを分析するスキル。   scenario-analystエージェントで主分析を実行し、   strategy-reviewerエージェントでセカンドオピニオンを取得。   1次・2次・3次影響、推奨銘柄、レビューを含む包括的レポートを日本語で生成。   使用例: /scenario-analyzer "Fed raises rates by 50bp"   トリガー: ニュース分析、シナリオ分析、18ヶ月展望、中長期投資戦略 |
| **[sector-analyst](skills/sector-analyst/)** | This skill should be used when analyzing sector rotation patterns and market cycle positioning. It fetches sector uptrend data from CSV (no API key required) and optionally accepts chart images for supplementary analysis. Use this skill when the user requests sector rotation analysis, cyclical vs defensive assessment, overbought/oversold identification, or market cycle phase estimation. All analysis and output are conducted in English. |
| **[signal-postmortem](skills/signal-postmortem/)** | Record and analyze post-trade outcomes for signals generated by edge pipeline and other skills. Track false positives, missed opportunities, and regime mismatches. Feed results back to edge-signal-aggregator weights and skill improvement backlog. |
| **[simple-deck](skills/simple-deck/)** | Single-file horizontal-swipe HTML deck. Built by copying the seed   `assets/template.html` (which carries the proven 5-rule iframe nav script)   and pasting slide layouts from `references/layouts.md`. Pitch decks,   product overviews, study material — when you don't need the magazine   aesthetic of `magazine-web-ppt`. |
| **[skill-designer](skills/skill-designer/)** | Design new Claude skills from structured idea specifications. Use when the skill auto-generation pipeline needs to produce a Claude CLI prompt that creates a complete skill directory (SKILL.md, references, scripts, tests) following repository conventions. |
| **[skill-idea-miner](skills/skill-idea-miner/)** | Mine Claude Code session logs for skill idea candidates. Use when running the weekly skill generation pipeline to extract, score, and backlog new skill ideas from recent coding sessions. |
| **[skill-integration-tester](skills/skill-integration-tester/)** | Validate multi-skill workflows defined in CLAUDE.md by checking skill existence, inter-skill data contracts (JSON schema compatibility), file naming conventions, and handoff integrity. Use when adding new workflows, modifying skill outputs, or verifying pipeline health before release. |
| **[skill-warden](skills/skill-warden/)** | Security scanner and health check for your AI agent skills tree. Identifies   dead skills, missing documentation, and unsafe shell execution paths. |
| **[social-carousel](skills/social-carousel/)** | A three-card social-media carousel laid out as 1080×1080 squares —   three cinematic, on-brand panels with display headlines that connect   across the series ("onwards." → "to the next one." → "looking ahead.").   Each card has a brand mark, a number / total, a caption, and a "loop"   affordance. Use when the brief asks for a "carousel post", "social   carousel", "Instagram carousel", "LinkedIn series", "X thread cards",   or "三连发". |
| **[sprite-animation](skills/sprite-animation/)** | A pixel / sprite-style animated explainer slide — full-bleed cream stage,   bold display year, animated pixel-art mascot (e.g. Hanafuda card, mushroom,   or 8-bit console), kinetic Japanese display type, ticking timeline ribbon.   Reads like a single frame of an educational motion video — looping CSS   keyframes, no JS, ready to be screen-recorded into a vertical video.   Use when the brief asks for a "sprite animation", "pixel-art video",   "8-bit explainer", "history of X explainer", "kinetic typography history",   "Nintendo-style", "精灵图动画", "像素动画", or "复古动画". |
| **[stanley-druckenmiller-investment](skills/stanley-druckenmiller-investment/)** | Druckenmiller Strategy Synthesizer - Integrates 8 upstream skill outputs (Market Breadth, Uptrend Analysis, Market Top, Macro Regime, FTD Detector, VCP Screener, Theme Detector, CANSLIM Screener) into a unified conviction score (0-100), pattern classification, and allocation recommendation. Use when user asks about overall market conviction, portfolio positioning, asset allocation, strategy synthesis, or Druckenmiller-style analysis. Triggers on queries like "What is my conviction level?", "How should I position?", "Run the strategy synthesizer", "Druckenmiller analysis", "総合的な市場判断", "確信度スコア", "ポートフォリオ配分", "ドラッケンミラー分析". |
| **[strategy-pivot-designer](skills/strategy-pivot-designer/)** | Detect backtest iteration stagnation and generate structurally different strategy pivot proposals when parameter tuning reaches a local optimum. |
| **[tdd](skills/tdd/)** | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development. |
| **[team-okrs](skills/team-okrs/)** | OKR tracker page — quarter banner, three objectives with their key   results as progress bars, owner avatars, status pills, and a "this   quarter at a glance" sidebar. Use when the brief mentions "OKRs",   "key results", "objectives", or "目标". |
| **[technical-analyst](skills/technical-analyst/)** | This skill should be used when analyzing weekly price charts for stocks, stock indices, cryptocurrencies, or forex pairs. Use this skill when the user provides chart images and requests technical analysis, trend identification, support/resistance levels, scenario planning, or probability assessments based purely on chart data without consideration of news or fundamental factors. |
| **[theme-detector](skills/theme-detector/)** | Detect and analyze trending market themes across sectors. Use when user asks about current market themes, trending sectors, sector rotation, thematic investing, what themes are hot or cold, or wants to identify bullish and bearish market narratives with lifecycle analysis. |
| **[to-issues](skills/to-issues/)** | Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into issues. |
| **[to-prd](skills/to-prd/)** | Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context. |
| **[trade-hypothesis-ideator](skills/trade-hypothesis-ideator/)** | Generate falsifiable trade strategy hypotheses from market data, trade logs,   and journal snippets. Use when you have a structured input bundle and want   ranked hypothesis cards with experiment designs, kill criteria, and optional   strategy.yaml export compatible with edge-finder-candidate/v1. |
| **[trader-memory-core](skills/trader-memory-core/)** | Track investment theses across their lifecycle — from screening idea to closed position with postmortem. Register theses from screener outputs, manage state transitions, attach position sizing, review due dates, and generate postmortem reports with P&L and MAE/MFE analysis. Trigger when user says "register thesis", "track this idea", "thesis status", "review due", "close position", "postmortem", or "trading journal". |
| **[triage](skills/triage/)** | Triage issues through a state machine driven by triage roles. Use when user wants to create an issue, triage issues, review incoming bugs or feature requests, prepare issues for an AFK agent, or manage issue workflow. |
| **[tweaks](skills/tweaks/)** | Wrap any HTML artifact with a side panel of live, parameterized   controls — accent color, type scale, density, motion, theme — that   rewrite CSS custom properties in real time and persist to   localStorage. Lets the user explore variants of a design without   re-prompting the agent. Use when the brief asks for "variants",   "side-by-side options", "tweak this", "let me adjust", "live   knobs", or "实时调参". |
| **[uptrend-analyzer](skills/uptrend-analyzer/)** | Analyzes market breadth using Monty's Uptrend Ratio Dashboard data to diagnose the current market environment. Generates a 0-100 composite score from 5 components (breadth, sector participation, rotation, momentum, historical context). Use when asking about market breadth, uptrend ratios, or whether the market environment supports equity exposure. No API key required. |
| **[urithiru](skills/urithiru/)** | Multi-lane AI verification system. When the user says "run this through Urithiru",   "Urithiru check", "full tower", or similar, fan the query out to 5-7 AI models   simultaneously via OpenRouter, collect independent responses, and synthesize the   best answer as the orchestrator. Antigravity is ALWAYS the orchestrator — the   models are lanes (specialists), not the decision-maker. |
| **[us-market-bubble-detector](skills/us-market-bubble-detector/)** | Evaluates market bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger framework v2.1. Prioritizes objective metrics (Put/Call, VIX, margin debt, breadth, IPO data) over subjective impressions. Features strict qualitative adjustment criteria with confirmation bias prevention. Supports practical investment decisions with mandatory data collection and mechanical scoring. Use when user asks about bubble risk, valuation concerns, or profit-taking timing. |
| **[us-stock-analysis](skills/us-stock-analysis/)** | Comprehensive US stock analysis including fundamental analysis (financial metrics, business quality, valuation), technical analysis (indicators, chart patterns, support/resistance), stock comparisons, and investment report generation. Use when user requests analysis of US stock tickers (e.g., "analyze AAPL", "compare TSLA vs NVDA", "give me a report on Microsoft"), evaluation of financial metrics, technical chart analysis, or investment recommendations for American stocks. |
| **[value-dividend-screener](skills/value-dividend-screener/)** | Screen US stocks for high-quality dividend opportunities combining value characteristics (P/E ratio under 20, P/B ratio under 2), attractive yields (3% or higher), and consistent growth (dividend/revenue/EPS trending up over 3 years). Supports two-stage screening using FINVIZ Elite API for efficient pre-filtering followed by FMP API for detailed analysis. Use when user requests dividend stock screening, income portfolio ideas, or quality value stocks with strong fundamentals. |
| **[vcp-screener](skills/vcp-screener/)** | Screen S&P 500 stocks for Mark Minervini's Volatility Contraction Pattern (VCP). Identifies Stage 2 uptrend stocks forming tight bases with contracting volatility near breakout pivot points. Use when user requests VCP screening, Minervini-style setups, tight base patterns, volatility contraction breakout candidates, or Stage 2 momentum stock scanning. |
| **[video-shortform](skills/video-shortform/)** | Short-form video generation skill — 3-10 second clips for product   reveals, motion teasers, ambient loops. Defaults to Seedance 2 but   works the same with Kling 3 / 4, Veo 3 or Sora 2. Output is one MP4   saved to the project folder. When the workspace also ships an   interactive-video / hyperframes skill, prefer composing several short   shots into a single timeline rather than one long monolithic clip. |
| **[web-prototype](skills/web-prototype/)** | General-purpose desktop web prototype. Single self-contained HTML file built   by copying the seed `assets/template.html` and pasting section layouts from   `references/layouts.md`. Default for any landing / marketing / docs / SaaS   page when no more specific skill matches. |
| **[weekly-update](skills/weekly-update/)** | Single-file horizontal-swipe slide deck for a weekly team update —   shipped, in flight, blocked, metrics, asks. 6–8 slides. Use when the   brief mentions "weekly update", "team update slides", "weekly status",   "周报演示". |
| **[wireframe-sketch](skills/wireframe-sketch/)** | A hand-drawn wireframe exploration — graph-paper background, marker /   pencil tone, multiple tab labels for variants, sticky-note annotations,   scribbled chart placeholders, hatched fills. Reads like a designer's   whiteboard before any pixels are committed. Use when the brief asks for   "wireframe", "sketch wireframe", "hand-drawn", "lo-fi", "whiteboard",   "草稿", or "手绘原型". |
| **[write-a-skill](skills/write-a-skill/)** | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill. |

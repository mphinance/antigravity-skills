# Antigravity Skills

> 105 AI agent skills for trading, market analysis, strategy research, and creative production. Built for Claude Code / Gemini agents using the `skills/` directory convention.

Drop these into your `~/.gemini/antigravity/skills/` (or equivalent agent skills directory) and your AI coding assistant gains superpowers.

---

## 🔥 Chad's Starter Pack — Strategy Optimization & Algo Trading

These are the skills most immediately useful if you're building a PineScript optimization engine, futures algo, or strategy evaluation pipeline. **Start here.**

| Skill | What It Does | API Key? |
|-------|-------------|----------|
| **[backtest-expert](skills/backtest-expert/)** | Expert guidance for systematic backtesting. "Beat ideas to death" methodology, parameter robustness, slippage modeling, bias prevention, overfitting detection. | None |
| **[edge-strategy-reviewer](skills/edge-strategy-reviewer/)** | Critical review of strategy drafts for edge plausibility, overfitting risk, sample size adequacy, execution realism. PASS/REVISE/REJECT verdicts with confidence scores. | None |
| **[edge-strategy-designer](skills/edge-strategy-designer/)** | Convert abstract edge concepts into concrete strategy draft variants with exportable YAML specs. | None |
| **[strategy-pivot-designer](skills/strategy-pivot-designer/)** | Detect backtest iteration stagnation and generate structurally different strategy pivot proposals when parameter tuning hits a local optimum. **This is exactly what you need when your optimizer keeps circling.** | None |
| **[trade-hypothesis-ideator](skills/trade-hypothesis-ideator/)** | Generate falsifiable trade strategy hypotheses from market data, trade logs, and journal snippets. Ranked hypothesis cards with experiment designs and kill criteria. | None |
| **[signal-postmortem](skills/signal-postmortem/)** | Record and analyze post-trade outcomes. Track false positives, missed opportunities, regime mismatches. Feed results back into weights. | None |
| **[position-sizer](skills/position-sizer/)** | Risk-based position sizing. Kelly criterion, ATR-based sizing, stop-loss calculation, sector concentration checks. | Tradier (optional) |
| **[options-strategy-advisor](skills/options-strategy-advisor/)** | Black-Scholes pricing, Greeks calculation, strategy P/L simulation, covered calls, spreads, iron condors, earnings plays. | Tradier (optional) |
| **[pine-to-python](skills/pine-to-python/)** | **[NEW]** Translate TradingView PineScript strategies into vectorized Python. Extract parameters for Optuna, translate `ta.*` functions to pandas-ta/numpy, harden against division-by-zero. Built specifically for your optimization engine. | None |
| **[data-quality-checker](skills/data-quality-checker/)** | Validate data quality in market analysis docs. Catch price scale inconsistencies, date/day-of-week mismatches, allocation total errors, unit mismatches. | None |
| **[diagnose](skills/diagnose/)** | Disciplined diagnosis loop for hard bugs. Reproduce, minimise, hypothesise, instrument, fix, regression-test. | None |

---

## 📊 Market Intelligence & Regime Detection

Understand the macro environment before you trade. Most of these pull from free public CSV data.

| Skill | What It Does | API Key? |
|-------|-------------|----------|
| [market-breadth-analyzer](skills/market-breadth-analyzer/) | 0-100 composite breadth score from 6 components using TraderMonty's public CSV data. | **None** |
| [uptrend-analyzer](skills/uptrend-analyzer/) | Market breadth via Monty's Uptrend Ratio Dashboard. 0-100 composite from 5 components. | **None** |
| [breadth-chart-analyst](skills/breadth-chart-analyst/) | Analyze S&P 500 breadth index charts. Can fetch CSV data directly without images. | **None** |
| [sector-analyst](skills/sector-analyst/) | Sector rotation patterns, cyclical vs defensive assessment, market cycle phase estimation. | **None** |
| [macro-regime-detector](skills/macro-regime-detector/) | Structural macro regime transitions (1-2 year horizon). Cross-asset ratio analysis for Concentration/Broadening/Contraction/Inflationary states. | Web search |
| [market-top-detector](skills/market-top-detector/) | 0-100 composite score for market top probability. O'Neil Distribution Days + Minervini Leading Stock Deterioration + Defensive Sector Rotation. | Web search |
| [ftd-detector](skills/ftd-detector/) | Follow-Through Day detection for market bottom confirmation using O'Neil methodology. Dual-index tracking (S&P 500 + NASDAQ). | Web search |
| [ibd-distribution-day-monitor](skills/ibd-distribution-day-monitor/) | IBD-style Distribution Day tracking for QQQ/SPY. 25-session expiration, 5% invalidation, cluster classification. | Web search |
| [us-market-bubble-detector](skills/us-market-bubble-detector/) | Minsky/Kindleberger framework v2.1. Mechanical scoring of Put/Call, VIX, margin debt, breadth, IPO data. | **None** |
| [exposure-coach](skills/exposure-coach/) | One-page Market Posture summary. Net exposure ceiling, growth-vs-value bias, new-entry-allowed recommendation. | Upstream skills |
| [theme-detector](skills/theme-detector/) | Trending market themes across sectors with lifecycle analysis. Hot/cold narratives. | Web search |
| [market-environment-analysis](skills/market-environment-analysis/) | Comprehensive global market analysis — US, European, Asian markets, forex, commodities, risk-on/risk-off. | Web search |
| [market-news-analyst](skills/market-news-analyst/) | Analyze recent market-moving news events. FOMC, ECB, BOJ, geopolitical events, mega-cap earnings. | Web search |
| [scenario-analyzer](skills/scenario-analyzer/) | 18-month scenario analysis from news headlines. 1st/2nd/3rd order effects, recommended positions, reviewer critique. | Web search |
| [downtrend-duration-analyzer](skills/downtrend-duration-analyzer/) | Historical downtrend duration analysis with interactive HTML histograms by sector and market cap. | FMP |

---

## 🔍 Stock Screening & Edge Research

Find trades. The full edge research pipeline flows: **hint extraction → concept synthesis → strategy design → review → export**.

| Skill | What It Does | API Key? |
|-------|-------------|----------|
| [vcp-screener](skills/vcp-screener/) | Minervini Volatility Contraction Pattern scanner for S&P 500. Stage 2 uptrend + tight base + contracting volatility. | FMP |
| [canslim-screener](skills/canslim-screener/) | William O'Neil's CANSLIM growth stock methodology. Earnings + price momentum. | FMP |
| [breakout-trade-planner](skills/breakout-trade-planner/) | Generate Minervini-style breakout trade plans from VCP screener output. Stop-limit brackets, position sizing. | None |
| [pead-screener](skills/pead-screener/) | Post-Earnings Announcement Drift patterns. Red candle pullback + breakout signals. | FMP |
| [earnings-trade-analyzer](skills/earnings-trade-analyzer/) | 5-factor scoring system for post-earnings stocks. Gap Size, Pre-Earnings Trend, Volume, MA200, MA50. | FMP |
| [earnings-calendar](skills/earnings-calendar/) | Upcoming earnings announcements for mid-cap+ US stocks. | FMP |
| [economic-calendar-fetcher](skills/economic-calendar-fetcher/) | Upcoming economic events — central bank decisions, employment, inflation, GDP. | FMP |
| [finviz-screener](skills/finviz-screener/) | Build and open FinViz screener URLs from natural language (English or Japanese). | None |
| [pair-trade-screener](skills/pair-trade-screener/) | Statistical arbitrage. Cointegrated pairs, z-scores, mean-reversion entry/exit. | FMP |
| [dividend-growth-pullback-screener](skills/dividend-growth-pullback-screener/) | Dividend growth stocks (12%+ annual growth, 1.5%+ yield) with RSI oversold pullbacks. | FMP |
| [value-dividend-screener](skills/value-dividend-screener/) | Quality dividend opportunities. P/E < 20, P/B < 2, yield 3%+, consistent growth. | FMP + FINVIZ |
| [us-stock-analysis](skills/us-stock-analysis/) | Comprehensive fundamental + technical analysis for any US ticker. | FMP/Tradier |
| [technical-analyst](skills/technical-analyst/) | Pure chart analysis from images. Trend ID, support/resistance, scenario planning. | None (images) |
| [institutional-flow-tracker](skills/institutional-flow-tracker/) | 13F filings analysis. Hedge fund accumulation/distribution patterns. | FMP |

### Edge Research Pipeline

These skills chain together into a full research pipeline: `hints → concepts → strategies → review → export`.

| Skill | Pipeline Role |
|-------|-------------|
| [edge-hint-extractor](skills/edge-hint-extractor/) | Extract edge hints from daily observations → `hints.yaml` |
| [edge-concept-synthesizer](skills/edge-concept-synthesizer/) | Abstract hints into reusable edge concepts with thesis + invalidation |
| [edge-candidate-agent](skills/edge-candidate-agent/) | Generate prioritized research tickets from observations |
| [edge-strategy-designer](skills/edge-strategy-designer/) | Convert concepts into strategy draft variants |
| [edge-strategy-reviewer](skills/edge-strategy-reviewer/) | Quality gate: PASS/REVISE/REJECT with confidence scores |
| [edge-signal-aggregator](skills/edge-signal-aggregator/) | Aggregate and rank signals from multiple skills |
| [edge-pipeline-orchestrator](skills/edge-pipeline-orchestrator/) | Orchestrate the full pipeline end-to-end |

---

## 🧠 Strategy Synthesis & Portfolio Management

Higher-order skills that combine multiple upstream signals.

| Skill | What It Does |
|-------|-------------|
| [stanley-druckenmiller-investment](skills/stanley-druckenmiller-investment/) | Integrates 8 upstream skills into a unified conviction score (0-100) with Druckenmiller-style allocation recommendations. |
| [portfolio-manager](skills/portfolio-manager/) | Comprehensive portfolio analysis via Alpaca MCP. Asset allocation, risk metrics, rebalancing. |
| [trader-memory-core](skills/trader-memory-core/) | Track investment theses from screening idea → closed position with postmortem. P&L + MAE/MFE analysis. |

---

## 🎯 Dividend & Income Investing

| Skill | What It Does |
|-------|-------------|
| [kanchi-dividend-sop](skills/kanchi-dividend-sop/) | Kanchi-style dividend investing SOP. Screening, deep dive, entry planning, monitoring cadence. |
| [kanchi-dividend-review-monitor](skills/kanchi-dividend-review-monitor/) | Forced-review triggers (T1-T5) for dividend portfolios. OK/WARN/REVIEW states. |
| [kanchi-dividend-us-tax-accounting](skills/kanchi-dividend-us-tax-accounting/) | US dividend tax and account-location workflow. Qualified vs ordinary, REIT/BDC treatment, IRA placement. |

---

## 🛠️ Agent Infrastructure & Skill Development

Build more skills. Test them. Review them.

| Skill | What It Does |
|-------|-------------|
| [urithiru](skills/urithiru/) | Multi-lane AI verification. Fan queries to 5-7 models via OpenRouter, synthesize best answer. | 
| [write-a-skill](skills/write-a-skill/) | Create new agent skills with proper structure and progressive disclosure. |
| [skill-designer](skills/skill-designer/) | Design skills from structured idea specs. Produces complete skill directories. |
| [skill-idea-miner](skills/skill-idea-miner/) | Mine session logs for skill idea candidates. Extract, score, backlog. |
| [skill-integration-tester](skills/skill-integration-tester/) | Validate multi-skill workflows. Check data contracts, naming, handoff integrity. |
| [dual-axis-skill-reviewer](skills/dual-axis-skill-reviewer/) | Review skills using deterministic checks + LLM deep review. Score 0-100. |
| [grill-me](skills/grill-me/) | Interview you relentlessly about a plan until reaching shared understanding. |
| [grill-with-docs](skills/grill-with-docs/) | Grill your plan against the existing domain model and update docs inline. |
| [design-an-interface](skills/design-an-interface/) | Generate multiple radically different interface designs using parallel sub-agents. |
| [improve-codebase-architecture](skills/improve-codebase-architecture/) | Find deepening opportunities in a codebase. Refactoring, consolidation, testability. |
| [request-refactor-plan](skills/request-refactor-plan/) | Create a detailed refactor plan with tiny commits via user interview. |
| [tdd](skills/tdd/) | Test-driven development with red-green-refactor loop. |
| [diagnose](skills/diagnose/) | Disciplined diagnosis loop for hard bugs. Reproduce → minimise → hypothesise → fix. |
| [qa](skills/qa/) | Interactive QA session. Report bugs conversationally, agent files GitHub issues. |
| [triage](skills/triage/) | Triage issues through a state machine driven by triage roles. |
| [to-issues](skills/to-issues/) | Break a plan/spec/PRD into independently-grabbable issues. |
| [to-prd](skills/to-prd/) | Turn conversation context into a PRD and publish to issue tracker. |
| [caveman](skills/caveman/) | Ultra-compressed communication mode. Cuts token usage ~75%. |

---

## 🎨 Design, Content & Creative Production

These aren't trading-related but they're powerful creative tools.

| Skill | What It Does |
|-------|-------------|
| [web-prototype](skills/web-prototype/) | General-purpose desktop web prototype. Single self-contained HTML file. |
| [dashboard](skills/dashboard/) | Admin/analytics dashboard. Fixed sidebar, KPI cards, charts. |
| [saas-landing](skills/saas-landing/) | Single-page SaaS landing with hero, features, pricing, CTA. |
| [pricing-page](skills/pricing-page/) | Standalone pricing page with plan tiers, feature comparison, FAQ. |
| [simple-deck](skills/simple-deck/) | Horizontal-swipe HTML slide deck. Pitch decks, product overviews. |
| [replit-deck](skills/replit-deck/) | Replit Slides-style horizontal deck. 8 visual themes. |
| [blog-post](skills/blog-post/) | Long-form article/blog post with hero, pull quotes, byline. |
| [edit-article](skills/edit-article/) | Edit and improve articles. Restructure, clarify, tighten prose. |
| [social-carousel](skills/social-carousel/) | Three-card 1080x1080 social media carousel. Instagram/LinkedIn/X. |
| [email-marketing](skills/email-marketing/) | Brand product-launch email. HTML email layout. |
| [mobile-app](skills/mobile-app/) | Mobile app screen inside pixel-accurate iPhone 15 Pro frame. |
| [mobile-onboarding](skills/mobile-onboarding/) | Multi-screen mobile onboarding flow. Splash, value-prop, sign-in. |
| [wireframe-sketch](skills/wireframe-sketch/) | Hand-drawn wireframe. Graph-paper, marker/pencil, sticky-note annotations. |
| [magazine-poster](skills/magazine-poster/) | Editorial-style newsprint poster. Oversized serif headline, 2-column body. |
| [guizang-ppt](skills/guizang-ppt/) | E-magazine style horizontal HTML PPT with WebGL fluid background. |
| [motion-frames](skills/motion-frames/) | Single-frame motion design. Rotating type ring, animated globe, parallax. |
| [sprite-animation](skills/sprite-animation/) | Pixel/sprite-style animated explainer slide. 8-bit, kinetic type. |
| [hyperframes](skills/hyperframes/) | Video compositions, animations, title cards, captions, voiceovers in HTML. |
| [image-poster](skills/image-poster/) | Single-image generation for posters, key art, editorial illustrations. |
| [video-shortform](skills/video-shortform/) | 3-10 second video clips. Product reveals, motion teasers, ambient loops. |
| [audio-jingle](skills/audio-jingle/) | Audio generation. Jingles, beds, voiceover, sound effects. |
| [critique](skills/critique/) | 5-dimension expert design review. Radar chart, evidence-backed scores. |
| [tweaks](skills/tweaks/) | Wrap HTML artifacts with live parameterized controls panel. |
| [design-brief](skills/design-brief/) | Parse structured design brief into concrete design spec. |
| [digital-eguide](skills/digital-eguide/) | Two-spread digital e-guide preview. Cover + lesson spread. |
| [gamified-app](skills/gamified-app/) | Multi-frame gamified mobile app prototype. Quests, XP, level bars. |
| [dating-web](skills/dating-web/) | Consumer dating/matchmaking dashboard. |
| [docs-page](skills/docs-page/) | Documentation page with left nav, article body, right-rail TOC. |
| [pm-spec](skills/pm-spec/) | Product spec / PRD page. Problem, metrics, scope, user stories. |
| [finance-report](skills/finance-report/) | Quarterly/monthly financial report. KPIs, charts, P&L, outlook. |
| [invoice](skills/invoice/) | Printable invoice page. Line items, tax, totals, payment instructions. |
| [kanban-board](skills/kanban-board/) | Kanban task board with columns, cards, assignee avatars, swimlanes. |
| [meeting-notes](skills/meeting-notes/) | Meeting notes page. Agenda, decisions, action items, owners. |
| [team-okrs](skills/team-okrs/) | OKR tracker. Objectives, key results, progress bars, status pills. |
| [hr-onboarding](skills/hr-onboarding/) | New-hire onboarding plan. First week schedule, buddy intro, checklist. |
| [eng-runbook](skills/eng-runbook/) | Engineering runbook. Service overview, alerts, procedures, on-call. |
| [weekly-update](skills/weekly-update/) | Weekly team update slide deck. Shipped, in-flight, blocked, metrics. |

---

## Setup

1. Clone this repo
2. Copy `skills/` into your agent's skills directory (e.g. `~/.gemini/antigravity/skills/`)
3. Skills that need API keys will tell you — most common are:
   - `FMP_API_KEY` — Financial Modeling Prep (free tier available at financialmodelingprep.com)
   - `TRADIER_API_KEY` — Tradier brokerage API
   - `OPENROUTER_API_KEY` — OpenRouter (for Urithiru multi-lane verification)

---

*Built by [@mphinance](https://github.com/mphinance) with Antigravity. 105 skills and counting.*

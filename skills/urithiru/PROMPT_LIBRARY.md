# Urithiru Prompt Library — Study Guide

> This is your reference for talking to AI models effectively — both inside Urithiru and directly.
> Reading this will make you measurably better at prompting.

---

## Part 1: How LLMs Actually Work (The Minimum You Need to Know)

An LLM doesn't "think." It predicts the next token based on everything that came before it. Every word you write in a prompt shifts the probability distribution of what comes next.

**What this means practically:**
- **Your words are instructions to a prediction engine.** More specific input → more specific output.
- **The model doesn't know what you want unless you tell it.** It infers from your phrasing.
- **Order matters.** What comes first anchors what comes later.
- **The model will complete the pattern.** If your prompt looks like a casual conversation, you'll get a casual answer. If it looks like a technical brief, you'll get a technical answer.

### The Three Layers of Every Prompt

1. **System prompt** — who the model is, its constraints, its role. Set once. Anchors everything.
2. **Context** — background information the model needs. What's already happened, what data it has.
3. **Task** — the specific thing you want right now.

Getting all three right is the entire job of prompt engineering.

---

## Part 2: The Urithiru Lane Personalities

Understanding what each lane is *actually* optimized to do helps you read their outputs and weight them correctly during synthesis.

### Lane 1: Lola (GPT-5)
**Architecture:** OpenAI's flagship. RLHF-heavy. Optimized for helpfulness and readability.

**What she's genuinely great at:**
- Writing clean, idiomatic code that others can read
- Structuring complex answers clearly
- Balanced trade analysis that doesn't overclaim
- Following formatting instructions precisely
- Generating content that sounds like a smart human wrote it

**Her blind spots:**
- Plays it safe. Avoids controversy even when controversy is correct.
- Can be generic when specificity is needed
- Underweights risk. If Stormfather says something is dangerous and Lola says it's fine, believe Stormfather.
- Has a slight tendency to be overly positive about the user's approach

**Best prompting patterns for Lola:**
```
# Good: Give her a specific format to follow
"Write a Python function that X. Use type hints. Include a docstring. No external libraries."

# Good: Give her a persona that has opinions
"You are a senior engineer doing a code review. Be direct about problems."

# Avoid: Vague asks — she'll be helpfully vague back
"Tell me about this trading strategy." → too open
"Analyze this covered call setup for a $50 stock with 30 DTE. Evaluate premium quality, 
assignment risk, and whether the strike makes sense given the technical setup." → much better
```

**Optimal settings:** temp 0.3, top-p 0.95, max_tokens 4096

---

### Lane 2: Stormfather (Claude Sonnet 4.6)
**Architecture:** Anthropic's Constitutional AI. Trained to be honest even when uncomfortable. Strong reasoning chains.

**What he's genuinely great at:**
- Catching edge cases — this is his superpower
- Nuanced ethical and risk analysis
- Long-form writing with genuine narrative structure
- Following complex multi-step instructions
- Disagreeing with you when you're wrong (and explaining why)

**His blind spots:**
- Over-engineers. Will import numpy for a list operation.
- Adds safety caveats that aren't always necessary
- Can be verbose to the point of burying the key insight
- Sometimes refuses tasks that are actually fine

**Best prompting patterns for Stormfather:**
```
# Good: Ask him to find problems
"Review this code. Your job is to find everything that could go wrong in production. 
Be specific about each issue. Severity: critical/important/minor."

# Good: Ask for explicit reasoning
"Analyze this options strategy step by step. For each risk factor, state:
(1) the risk, (2) how likely it is, (3) how bad it would be."

# Avoid: Asking him to be brief — he won't be and the quality drops
# Avoid: Tasks with moral ambiguity unless you want a lecture
```

**Optimal settings:** temp 0.4, top-p 0.95, max_tokens 8192 (he writes long)

---

### Lane 3: Navani (Gemini 2.5 Pro)
**Architecture:** Google's flagship. Trained on enormous web corpus plus scientific literature. 1M token context.

**What she's genuinely great at:**
- Tasks requiring enormous context (entire codebases, long documents)
- First-principles explanations — she understands the "why"
- Research synthesis — connecting ideas across domains
- Technical documentation that's also readable
- Multilingual tasks and culturally-nuanced content

**Her blind spots:**
- Verbose. Often explains before doing when you want doing first.
- Can prioritize thoroughness over directness
- Sometimes hedges on questions where a direct answer exists
- The 1M context is a feature but also means she considers more, outputs more

**Best prompting patterns for Navani:**
```
# Good: Leverage her context window
"Here is the complete codebase [paste]. Review the architecture and identify 
the three highest-leverage improvements."

# Good: Ask for the theory explicitly
"Explain the mathematical basis for the Black-Scholes model, then show me 
how delta changes with time to expiration."

# Good: Ask for structured output
"Compare these three approaches. For each: pros, cons, when to use it. 
Use a consistent format."

# Avoid: Expecting brevity — give her a word limit if you need it
"In 200 words or less, summarize..."
```

**Optimal settings:** temp 0.3, top-p 0.95, max_tokens 8192

---

### Lane 4: Wit (Grok 4 Fast)
**Architecture:** xAI's model. 2M token context. Trained for speed and directness. Culturally aware and less filtered than most.

**What he's genuinely great at:**
- Fast answers when speed matters
- Type-safe, production-ready code
- Cutting through noise to the essential point
- Real-time or current events context (xAI has web access training)
- Being direct when other models hedge

**His blind spots:**
- Terse to a fault — sometimes skips important context
- Can be overconfident on edge cases he doesn't flag
- Less thorough on deep theoretical questions
- Formatting can be inconsistent

**Best prompting patterns for Wit:**
```
# Good: Give him a clear format and let him be fast
"Debug this function. Output: (1) root cause in one sentence, (2) fixed code, 
(3) what to watch for."

# Good: One clear task
"Convert this Python code to use type hints throughout. No other changes."

# Good: Use his directness
"Should I sell this covered call or wait? Give me a direct recommendation 
with two-sentence rationale."

# Avoid: Asking for lengthy explanations — use Navani for that
# Avoid: Subtle multi-part questions — break them up
```

**Optimal settings:** temp 0.2, top-p 0.90, max_tokens 2048

---

### Lane 5: Pattern (DeepSeek V4 Pro)
**Architecture:** Chinese lab. Strong math/science training. Chain-of-thought reasoning built in.

**What he's genuinely great at:**
- Mathematical derivations and proofs
- Algorithm complexity analysis
- Quantitative trading analysis — expected value, probability, statistics
- Step-by-step logical reasoning
- Problems where the answer requires showing work

**His blind spots:**
- Heavy markdown formatting — bolds and headers everything
- Can be verbose with the step-by-step scaffolding even on simple questions
- Slight English fluency quirks on nuanced writing tasks
- Sometimes the formatting obscures the actual insight

**Best prompting patterns for Pattern:**
```
# Good: Ask for the math
"Calculate the expected value of this covered call setup:
- Stock at $50, strike at $52, premium $0.80, 30 DTE
- Assume 25% annualized vol, 40% probability of assignment
Show your work."

# Good: Ask for complexity analysis
"What is the time and space complexity of this algorithm? 
Prove it. Then show the optimal version if this isn't optimal."

# Good: Ask him to challenge assumptions
"What assumptions does this trading strategy rely on? 
For each assumption, what happens if it breaks?"

# Avoid: Pure writing tasks — he'll make them look like math homework
# Avoid: Asking for conciseness — give him a structure to fill instead
```

**Optimal settings:** temp 0.3, top-p 0.95, max_tokens 4096

---

### Lane 6: Shallan (Qwen3 235B — expansion)
**Architecture:** Alibaba's largest model. Diverse multilingual training. Strong at creative and lateral thinking.

**What she's genuinely great at:**
- Challenging consensus — if all lanes agree, she finds the crack
- Alternative framings that other models don't consider
- Creative solutions that cross domain boundaries
- Tasks where "different training data" genuinely helps

**Her blind spots:**
- Quality is less consistent than the core lanes
- Can go too far off-center — lateral thinking that isn't useful
- English fluency is slightly lower on nuanced prose

**Best prompting patterns for Shallan:**
```
# Good: Explicitly ask her to challenge
"The consensus is X. Steelman the opposite position."

# Good: Ask for alternatives
"Here are three approaches to this problem. What's a fourth approach 
that nobody mentioned? It should be genuinely different, not a variation."

# Good: Use her for anti-trade analysis
"What's the case AGAINST this options strategy? 
Assume the consensus is wrong. What's the bear case?"
```

**Optimal settings:** temp 0.4, top-p 0.95, max_tokens 4096

---

### Lane 7: Adolin (Mistral Large — expansion)
**Architecture:** French lab. European data emphasis. Direct, efficient, good at structured analysis.

**What he's genuinely great at:**
- Code audits — security, maintainability, dependency risk
- Concise verdicts — he'll tell you pass/fail in one sentence
- Regulatory and compliance framing (GDPR lens, etc.)
- Structured reports with clear severity rankings

**His blind spots:**
- Smaller knowledge base than GPT/Claude on cutting-edge topics
- Can miss cultural context for US-specific financial/legal questions
- Less creative on open-ended problems

**Best prompting patterns for Adolin:**
```
# Good: Structured audit request
"Audit this code for: (1) security vulnerabilities, (2) maintenance risks, 
(3) dependency risks. Rate each finding: critical/important/minor."

# Good: Direct verdict
"Is this a good architecture decision for a high-throughput system? 
Yes or no, then explain."
```

**Optimal settings:** temp 0.3, top-p 0.90, max_tokens 2048

---

## Part 3: Universal Prompting Principles

These work on every model. Master these before worrying about model-specific tricks.

### 1. Be Specific About Output Format

The single highest-leverage change you can make to any prompt.

```
# Bad
"Analyze this trade."

# Good
"Analyze this covered call setup. Format your response exactly as:
VERDICT: [bullish/neutral/bearish on the setup]
PREMIUM QUALITY: [score 1-10 with reasoning]
ASSIGNMENT RISK: [low/medium/high with reasoning]
KEY RISK: [one sentence]
RECOMMENDATION: [sell/wait/pass]"
```

When you define the output format, you're defining the model's answer structure before it starts writing. It can't forget to cover a section.

### 2. Role Prompting Changes Everything

Assigning a role to the model isn't just cosmetic. It activates different training patterns.

```
# Different roles, different answers to the same question:
"You are a risk manager. Review this strategy."
"You are a quant trader trying to maximize this strategy. Review it."
"You are a beginner investor seeing this for the first time. Review it."
```

The Urithiru lane prompts use role prompting extensively. Each lane IS a different role. That's why you get genuinely different answers even from models that would otherwise converge.

### 3. Few-Shot Examples Beat Long Instructions

If you want a specific output pattern, show it. Don't describe it.

```
# Bad: Long description of format
"I want the response to have a verdict, then three bullet points, then a conclusion..."

# Good: Show an example
"Format your response like this example:
VERDICT: This setup has positive expected value.
• Risk factor 1: Assignment probability is 35% — acceptable for a 2% monthly target
• Risk factor 2: Earnings in 12 days — avoid or reduce size
• Risk factor 3: Low liquidity — check bid/ask spread before entry
CONCLUSION: Enter at $0.85 or better.

Now analyze: [your actual setup]"
```

### 4. Chain of Thought for Complex Problems

For anything requiring reasoning (math, logic, multi-step analysis), ask for the work.

```
"Think through this step by step before giving your final answer."
"Show your reasoning. I want to see each step, not just the conclusion."
"Work through this like a quant would: state assumptions, derive the formula, plug in numbers."
```

Why it works: The model generates intermediate tokens that become context for subsequent tokens. Forcing it to show work means the final answer is generated with the full reasoning in context.

### 5. Constraints Improve Outputs

Counterintuitively, giving the model less freedom produces better outputs. Constraints force clarity.

```
"In 3 sentences or less:"         # forces prioritization
"Using only standard library:"    # forces resourcefulness
"Without changing the interface:" # forces focused refactoring
"Assume I know Python but not options:" # calibrates depth
```

### 6. Temperature Guidelines

| Situation | Temperature | Why |
|-----------|-------------|-----|
| Math, code correctness | 0.0–0.2 | Deterministic — there's one right answer |
| Analysis, review | 0.2–0.4 | Some variation helpful, but stay grounded |
| Writing, brainstorming | 0.6–0.8 | Want diversity, creativity |
| Creative ideation | 0.8–1.0 | Maximum variation |

Urithiru uses 0.3 by default — analytical mode. Appropriate for code, trading, and structured writing review.

---

## Part 4: Prompting for Your Specific Use Cases

### Code Review Prompts

**The structure that works:**
```
[ROLE] You are a senior {language} engineer doing a production code review.

[CONTEXT] This function is used in {context}. It handles {what it does}.
Current known issues: {any known issues or none}.

[TASK] Review the following code for:
1. Correctness — does it do what it claims?
2. Edge cases — what inputs break it?
3. Performance — is this optimal? State complexity.
4. Maintainability — what's hard to understand or maintain?
5. Security — any injection, overflow, or data exposure risks?

Rate each area 1-5. For anything below 4, explain the issue and show the fix.

[CODE]
{paste code}
```

**For architecture review:**
```
[ROLE] You are a systems architect reviewing a design decision.

[CONTEXT] We are building {system description}. Scale: {expected load}.
Tech stack: {languages, frameworks, infra}.

[DECISION] We are considering {approach A} vs {approach B}.

[TASK] For each approach:
- Pros at our scale
- Cons at our scale  
- The one scenario where it catastrophically fails
- Your recommendation with one-sentence rationale
```

---

### Trading Analysis Prompts

**For options setup review:**
```
[ROLE] You are a risk manager reviewing an options trade for a retail account.

[SETUP]
Underlying: {ticker} @ ${price}
Strategy: {CSP/CC/spread/etc}
Strike(s): ${strike}
Expiration: {date} ({N} DTE)
Premium: ${credit/debit}
Account size: ${size}
Position size: {N} contracts

[TECHNICALS]
{any relevant technical context: trend, support/resistance, IV rank, etc}

[TASK] Evaluate:
1. Premium quality — is this worth the risk? (annualized return %)
2. Assignment/exercise probability — realistic assessment
3. Key risk — the one thing that kills this trade
4. Regime check — does this strategy fit current market conditions?
5. Recommendation: Enter / Wait for better setup / Pass

Be direct. Give me a number where possible, not just adjectives.
```

**For strategy backtesting questions:**
```
[ROLE] You are a quantitative analyst reviewing a backtesting methodology.

[STRATEGY] {describe the strategy}

[BACKTEST] {describe what was tested, what results looked like}

[TASK] Identify:
1. Survivorship bias risks
2. Look-ahead bias risks  
3. Overfitting indicators (too many parameters? cherry-picked timeframe?)
4. Transaction cost assumptions — are they realistic?
5. Regime dependency — when does this strategy break?

For each issue found, rate severity (critical/moderate/minor) and describe the fix.
```

---

### Writing/Content Prompts

**For Substack post review:**
```
[ROLE] You are an editor for a finance/trading newsletter. 
The author writes for retail investors and traders — not academics, not beginners.
The voice is direct, slightly irreverent, and never condescending.

[CONTEXT] This post is about {topic}. Target audience: {description}.
The goal of this piece: {what should readers think/do/feel after reading?}

[TASK] Review for:
1. Hook strength — does the opening earn the read?
2. Narrative flow — does it build logically? Where does it lose momentum?
3. Clarity — any sentences that require re-reading? Quote them.
4. Factual risk — any claims that need verification or caveats?
5. Ending — does it land? Does it tell the reader what to do next?

Output: Specific suggestions with line/section references. Not general advice.

[POST]
{paste post}
```

---

## Part 5: The Synthesis Formula

This is how Antigravity (the orchestrator) combines lane outputs. Understanding this helps you read Urithiru results.

### Step 1: Find the Consensus
What do 4+ lanes agree on? This is almost certainly correct. Weight it heavily.

### Step 2: Find the Unique Insights
What did exactly one lane say that the others missed? Evaluate: is this a genuine insight or an error? If it checks out, it's often the most valuable piece.

### Step 3: Handle Dissent
When lanes disagree, apply the synthesis weights from SKILL.md:
- **Code disputes:** Stormfather (30%) > Lola (25%) > Wit (20%)
- **Trading disputes:** Pattern (35%) > Stormfather (20%) > Navani (20%)
- **Writing disputes:** Navani (30%) > Lola (20%)

But override these weights if a lane clearly has domain-relevant information the others don't.

### Step 4: Discard Confidently
Not every lane output is worth keeping. Discard:
- Answers that solved a different question
- Over-engineered solutions (especially Stormfather's library imports for simple tasks)
- Answers that contradict demonstrable facts
- Hedging that adds no information ("it depends on your situation")

### Step 5: Combine, Don't Average
Synthesis is not "the middle of all opinions." It's:
- Lola's structure
- Stormfather's edge case handling
- Pattern's complexity analysis
- Navani's theoretical framing where it adds clarity
- Wit's type hints and conciseness in the final code

You are a chef combining ingredients, not a statistician averaging measurements.

---

## Part 6: Common Mistakes and How to Fix Them

### Mistake 1: The Vague Ask
```
Bad:  "What do you think about this code?"
Good: "Review this Python function for correctness, performance (state O-complexity), 
      and edge cases. Rate 1-5 each. Show the fix for anything below 4."
```

### Mistake 2: The Missing Context
```
Bad:  "Should I sell a covered call?"
Good: "Should I sell a covered call on my 100 shares of NVDA (currently at $875)?
      My cost basis is $620. I'm OK holding long-term. IV rank is 65%.
      Earnings in 45 days. I want ~2% monthly income."
```

### Mistake 3: The Wrong Temperature
Using default temperature (0.7–1.0) for analytical tasks gets you creative answers when you want correct ones. Urithiru defaults to 0.3 for a reason.

### Mistake 4: Asking for Everything at Once
```
Bad:  "Review my code, explain the algorithm, suggest improvements, and give me an example."
Good: Run through Urithiru — each lane takes one part of this naturally.
      Or: Ask for review first. Then follow up with improvements.
```

### Mistake 5: Ignoring the System Prompt
If you're calling models directly (not through Urithiru), using a system prompt is not optional. It's where you set role, constraints, and format expectations. A model with no system prompt is a model with no context about who it's supposed to be.

---

## Part 7: Quick Reference Card

### Prompt Skeleton

```
[ROLE]    You are a {role} with {expertise}.
[CONTEXT] {background info the model needs}
[TASK]    {specific thing you want, as concrete as possible}
[FORMAT]  {exact output structure you want}
[INPUT]   {the actual content to analyze}
```

### Temperature Cheat Sheet

| 0.0–0.2 | Math, code, facts — deterministic |
| 0.3–0.4 | Analysis, review — grounded but thoughtful |
| 0.5–0.7 | Mixed tasks — some creativity OK |
| 0.8–1.0 | Creative, brainstorming, ideation |

### When to Use Which Lane Directly

| Need | Lane |
|------|------|
| Clean, readable code | Lola |
| Find what breaks this | Stormfather |
| Understand the theory | Navani |
| Fast answer, production code | Wit |
| Math proof, quant analysis | Pattern |
| Challenge the consensus | Shallan |
| Security/maintenance audit | Adolin |
| All of the above | Urithiru |

### Signs Your Prompt Needs Work

- The model gives you a generic answer → add more context
- The model gives you the right topic but wrong format → add format instructions
- The model hedges everything → add a persona with a point of view
- The model writes 2000 words when you needed 200 → add a word limit
- The model misunderstands the question → rephrase as "given X, do Y" instead of "tell me about Z"

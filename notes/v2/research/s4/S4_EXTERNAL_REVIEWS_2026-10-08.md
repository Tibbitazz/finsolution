# S4 record — external "agentic portfolio" references reviewed 2026-10-08

**Document status:** DRAFT (review record; nothing adopted) · **Basis:**
- owner request 2026-10-08 ("Are some of the methods implementable and useful for our engine? Do a highly critical review");
- review rules: every upload gets FITS / PARTIAL / DOES NOT FIT and the eight-question fit test (S4 plan §E); sources are review inputs, never authorities.

## 1. MongoDB Atlas solutions library: "Agentic AI-Powered Investment Portfolio Management"

**Identity and scope** (`VERIFIED-SOURCE`; page and `leafy-bank-backend-capitalmarkets-agents` README, accessed 2026-10-08):
- A **database-vendor reference demo**: MongoDB Atlas (time series, vector search, LangGraph checkpointer), LangGraph ReAct agents, VoyageAI `voyage-finance-2` embeddings, FinBERT sentiment.
- The LLM is Anthropic on AWS Bedrock; the sample config pins `anthropic.claude-3-haiku-20240307-v1:0`.
- MIT licence.
- **Agents:** six scheduled agents (05:00–05:50 UTC, staggered) for market analysis, news, social media, crypto analysis, crypto news and crypto social media, plus two ReAct "assistant" chat agents.
- **Data:** Yahoo Finance, Yahoo News, Reddit, FRED, Binance, CoinGecko. "simulated portfolio performance data".
- The README itself says "Some components are simplified or emulated to ensure predictable outputs".

**What it does and does not do:**

| Element | Finding |
|---|---|
| Allocation / optimisation | **None.** The "portfolio allocation tool" only *reads* current holdings. There is no optimiser, target weights or rebalancing rule |
| Recommendations | Produced by an LLM ("Portfolio Overall Diagnosis … combined with LLM-based reasoning … to produce tailored portfolio recommendations") |
| Risk | Market-level heuristics only: VIX level and percentage changes "to guide equity exposure"; 50-day moving-average trend. **No portfolio volatility, VaR, covariance or correlation** |
| Evaluation | **No tests, back-tests or accuracy evaluation**; no disclaimer |
| Governance | MCP demo is read-only; checkpoints claimed to support audits. No IPS, approval or limits |

**Critical assessment against our rules:**
- **R1/R8 violation:** an LLM produces the portfolio recommendation and numbers are not bound to deterministic descriptors.
- **No method content:** nothing for the Method Library (S4.5–S4.14) or CRO (S4.16).
- **Data:** Yahoo Finance and Reddit usage conflicts with the licence findings (S6 lead §3). Crypto is out of scope.
- **Contamination:** sentiment and summaries from an LLM on historical news are exposed to look-ahead (`S4_LIT_LOOKAHEAD_2026-10-07.md`); no mitigation is described.
- **Evidence:** zero. It is marketing for a database product.

**Verdict: DOES NOT FIT** as investment methodology. Narrow **PARTIAL** for S8 *infrastructure patterns*, which the developer may evaluate (none is required):

| Pattern | Our counterpart | Note |
|---|---|---|
| Scheduled, staggered batch agents with fixed tool sequences ("structured, deterministic process where tools are invoked in a fixed sequence") | Third-party "mandatory tool sequence" pattern (`S4_GITHUB_IMPL_REVIEW.md`); DR-1 as-of gate | Consistent with R1; generic |
| Agent-state checkpointing (LangGraph checkpointer) | DR-2 learning capture; Decision Records (ADR-0026 §9) | The store is a developer choice (DB-agnostic) |
| Embedding + vector search over news for evidence retrieval | Evidence packets (RQ-34); R8 | Only with point-in-time retrieval and the contamination diagnostics (X-1 … X-5) |
| Read-only MCP access for natural-language querying | ADR-0017 analysis-only default | Generic |

## 2. Medium: "How I Vibe-Coded My Portfolio With Agentic AI" (V. Kulkarni, 23 Nov 2025)

**Identity** (`VERIFIED-SOURCE`; article read in full, 2026-10-08):
- The "portfolio" is the author's **personal portfolio website** (imvinay.com), not an investment portfolio.
- It describes building a Next.js + Tailwind site with AI coding assistants (Cline, Kilo Code, Antigravity + Gemini 3 Pro, VS Code + GPT-5.1-Codex-Max), comparing LLMs for front-end coding, with CI/CD via GitHub Actions.

**Verdict: DOES NOT FIT.** No investment content; outside our mandate (00_CHARTER). The only generic lesson is "Markdown spec documents as the source for agentic coding". Our specification-first workflow already embodies it, and development tooling is the developer's choice (S8).

## 3. Consequence
No change to the S4 plan, roster, contracts or RQs. The S8 infrastructure patterns above are listed for the developer as non-binding references.

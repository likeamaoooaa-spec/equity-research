## Repository Guidelines

### Project Overview

This repository houses equity research and investment analysis, with AI agents (Codex) assisting in buy-side memo generation, valuation modelling, and alpha-hypothesis testing. Work is organized around tickers and analysis types.

### Project Structure

- `research/[TICKER]/` — Per-company equity research memos and reports
- `valuation/[TICKER]/` — DCF, SOTP, TAM-adj-PEG, Bayesian intrinsic growth, and GF-DMA models
- `alpha/` — Serenity-style alpha hypotheses: news-to-financial-statement mappings with small-cap transmission analysis
- `data/` — Downloaded filings, XBRL extracts, and scraping outputs (gitignored if large)
- `notes/` — Unstructured observations, investment-committee rough notes, and monitoring dashboards

Folders are created on demand. If a ticker has only one analysis type, place the file directly under `research/` or `valuation/` without a subfolder.

### File Naming

- Memos: `[YYYY-MM-DD]_[TICKER]_[type].md` (e.g. `2026-07-11_AAPL_buyside-memo.md`)
- Valuation models: `[TICKER]_[method].md` (e.g. `NVDA_tam-adj-peg.md`)
- Alpha notes: `[YYYY-MM-DD]_[catalyst-tag].md` (e.g. `2026-07-11_nvda-b200-ramp.md`)

### Working with Agents

This repository is designed for use with Codex. When asking an agent to produce analysis, specify:

1. The ticker or catalyst
2. The desired output type (memo, valuation, alpha note)
3. Language preference (Chinese by default)
4. Depth: `quick` (summary) or `deep` (full report)

Available agent skills for this repo: `buy-side-equity-research-memo`, `bayesian-intrinsic-growth-valuation`, `tam-adj-peg`, `gf-dma-health-index`, `serenity-alpha`, and DBS business-toolkit skills.

### Commit Guidelines

- Prefix commits with the ticker: `AAPL: add base-case DCF`
- For multi-ticker or infrastructure changes, use `meta:` or `data:`
- Squash trivial fixups before pushing to keep history scannable

### Source Discipline

All analysis must distinguish reported facts from management guidance, consensus estimates, and analyst inference. Cite sources with document type, date, and access date. Mark unverifiable numbers as `未核验`.

### Language

Default analysis language is Chinese (Simplified). English is used for tickers, file slugs, and commit messages.

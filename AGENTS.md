## Repository Guidelines

### Project Overview

This repository houses equity research and investment analysis, presented as a static website via GitHub Pages. AI agents (Codex) assist in buy-side memo generation, valuation modelling, and alpha-hypothesis testing.

### Project Structure

```
research/[TICKER]/    — 个股研究：buy-side memos, chronicles, investment audits, biographies
notes/[sector]/       — 行业笔记：按行业分子目录（如 space/, semiconductor/, ai/）
valuation/[TICKER]/   — 估值模型：DCF, SOTP, TAM-adj-PEG, Bayesian intrinsic growth, GF-DMA
alpha/                — Serenity-style alpha hypotheses
data/                 — 下载的 filings, XBRL, 抓取数据（gitignored）
```

Folders are created on demand.

### File Naming

- Memos: `[YYYY-MM-DD]_[TICKER]_[type].md` (e.g. `2026-07-11_AAPL_buyside-memo.md`)
- Valuation models: `[TICKER]_[method].md` (e.g. `NVDA_tam-adj-peg.md`)
- Alpha notes: `[YYYY-MM-DD]_[catalyst-tag].md` (e.g. `2026-07-11_nvda-b200-ramp.md`)
- Notes: `[YYYY-MM-DD]_[topic-slug].md` (e.g. `2026-07-12_space-industry-investment-report.md`)

### Frontend Website

The repository is served via GitHub Pages from the `master` branch root. Key files:

- `index.html` — Single-page app with collapsible sidebar tree and Markdown rendering (marked.js)
- Sidebar structure is driven by the `TREE` object in `index.html` → **when adding new files, update the TREE object**
- Directory collapsing state is persisted in `localStorage`

### Working with Agents

When asking an agent to produce analysis, specify:

1. The ticker or catalyst
2. The desired output type (memo, valuation, alpha note, chronicle, biography, audit)
3. Language preference (Chinese by default)
4. Depth: `quick` (summary) or `deep` (full report)

Available agent skills: `buy-side-equity-research-memo`, `bayesian-intrinsic-growth-valuation`, `tam-adj-peg`, `gf-dma-health-index`, `serenity-alpha`, and DBS business-toolkit skills.

### Commit Guidelines

- Prefix commits with the ticker: `AAPL: add base-case DCF`
- For multi-ticker or infrastructure changes, use `meta:` or `data:`
- Squash trivial fixups before pushing to keep history scannable

### Source Discipline

All analysis must distinguish reported facts from management guidance, consensus estimates, and analyst inference. Cite sources with document type, date, and access date. Mark unverifiable numbers as `未核验`.

### Language

Default analysis language is Chinese (Simplified). English is used for tickers, file slugs, and commit messages.

### Git & GitHub Workflow

- AGENTS.md is local-only (in `.gitignore`) — used by agents, never pushed
- **After generating or modifying any report file**, the agent MUST:
  1. `git add` the new/changed files
  2. Commit with an appropriate ticker/meta prefix
  3. `git push` to GitHub
- The repository is public and served via GitHub Pages at `https://likeamaoooaa-spec.github.io/equity-research/`
- When adding a new report file, also update the `TREE` object in `index.html` to reflect the new entry

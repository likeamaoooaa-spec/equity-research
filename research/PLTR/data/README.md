# Palantir Technologies (PLTR) — SEC Filings Archive (FY2020–2026)

SEC filings downloaded via [edgartools](https://github.com/dgunning/edgartools) from the SEC EDGAR system.

## Coverage

| Form | Period Range | Count | Description |
|------|-------------|-------|-------------|
| **10-K** | FY2020 – FY2025 | 6 | Annual reports |
| **10-Q** | Q3 2020 – Q1 2026 | 17 | Quarterly reports |
| **8-K** | 2024 – 2026 | 10 | Material event disclosures |

**Total**: 33 filings, ~43 MB

## Directory Structure

```
data/PLTR_SEC/
├── 10-K/
│   ├── 10-K_FY2020_2021-02-26.html
│   ├── 10-K_FY2021_2022-02-24.html
│   ├── 10-K_FY2022_2023-02-21.html
│   ├── 10-K_FY2023_2024-02-20.html
│   ├── 10-K_FY2024_2025-02-18.html
│   └── 10-K_FY2025_2026-02-17.html
├── 10-Q/
│   ├── 10-Q_2020_09_30_2020-11-13.html
│   ├── ... (through Q1 2026)
│   └── 10-Q_2026_03_31_2026-05-05.html
├── 8-K/
│   ├── 8-K_2024-11-14.html  (Nasdaq transfer announcement)
│   ├── ...
│   └── 8-K_2026-06-09.html
└── README.md
```

## Source

- **Provider**: U.S. Securities and Exchange Commission (SEC EDGAR)
- **CIK**: 0001321655
- **Ticker**: PLTR (Nasdaq)
- **Download tool**: edgartools v5.42.0
- **Download date**: 2026-07-12

## Usage Notes

- All files are HTML as-downloaded from SEC EDGAR
- For financial data extraction, use XBRL datasets or parse with edgartools
- These are primary-source documents for fundamental research; always cross-reference with latest filings

## Related Research

See `research/PLTR/` for analysis reports:
- `2026-07-11_PLTR_buyside-memo.md` — Buy-side equity research memo
- `2026-07-12_PLTR_chronicle.md` — Company chronicle (2003–2026)

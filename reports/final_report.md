# Fundamental Health Screener: Findings

## Purpose

This report summarizes a small illustrative cohort of public-company 10-K facts downloaded from the SEC EDGAR Company Facts API. It is a trend-screening output, not investment research, investment advice, or a company-quality ranking.

## Latest reported fiscal-year results

| Ticker | FY | Revenue growth | Operating margin | Net margin | Receivables growth | Flags | Status |
|---|---|---|---|---|---|---|---|
| GOOGL | 2024 | 9.8% | 26.5% | 21.2% | 19.1% | 2 | review |
| AAPL | 2024 | 7.8% | 30.3% | 25.3% | 4.7% | 1 | watch |
| KO | 2024 | 11.2% | 25.4% | 22.2% | -2.2% | 1 | watch |
| MSFT | 2024 | 18.0% | 42.1% | 36.7% | 10.0% | 0 | stable |
| NVDA | 2024 | 61.4% | 37.3% | 36.2% | -17.7% | 0 | stable |

## How to read the result

Each alert is a prompt to read the underlying filing. A `margin contraction` flag identifies a year-over-year operating-margin decline of at least 3 percentage points. A `growth deceleration` flag identifies a material slowing relative to the prior year’s growth rate. A `receivables warning` flag identifies receivables growth at least 10 percentage points above revenue growth.

The labels are deliberately conservative:

- **Stable:** no mechanical flags in the latest year.
- **Watch:** one flag; inspect the notes and business context.
- **Review:** two or more flags; prioritize deeper filing-level review.

## Limits on interpretation

Companies operate in different industries and use different fiscal calendars. Acquisitions, divestitures, accounting choices, and amended filings can materially affect these metrics. The model does not account for valuation, cash flow, debt, stock price, guidance, segment mix, or non-financial risk.

See `docs/methodology.md` for data extraction rules and limitations.

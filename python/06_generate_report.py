"""Generate a concise, non-investment-advice report from the SQL output."""
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT = PROJECT_ROOT / "data" / "processed" / "company_health.csv"
REPORT = PROJECT_ROOT / "reports" / "final_report.md"


def markdown_table(frame: pd.DataFrame) -> str:
    header = "| " + " | ".join(frame.columns) + " |"
    divider = "|" + "|".join(["---"] * len(frame.columns)) + "|"
    rows = ["| " + " | ".join(map(str, row)) + " |" for row in frame.itertuples(index=False, name=None)]
    return "\n".join([header, divider, *rows])


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError("Run python/04_export_analysis.py first.")
    data = pd.read_csv(INPUT)
    latest = data.loc[data.groupby("ticker")["fiscal_year"].idxmax()].copy()
    latest = latest.sort_values(["flag_count", "ticker"], ascending=[False, True])
    display = latest[["ticker", "fiscal_year", "revenue_growth_pct", "operating_margin_pct", "net_margin_pct", "receivables_growth_pct", "flag_count", "health_status"]].copy()
    for column in ["revenue_growth_pct", "operating_margin_pct", "net_margin_pct", "receivables_growth_pct"]:
        display[column] = display[column].map(lambda value: "n/a" if pd.isna(value) else f"{value:.1f}%")
    display.columns = ["Ticker", "FY", "Revenue growth", "Operating margin", "Net margin", "Receivables growth", "Flags", "Status"]
    report = f"""# Fundamental Health Screener: Findings

## Purpose

This report summarizes a small illustrative cohort of public-company 10-K facts downloaded from the SEC EDGAR Company Facts API. It is a trend-screening output, not investment research, investment advice, or a company-quality ranking.

## Latest reported fiscal-year results

{markdown_table(display)}

## How to read the result

Each alert is a prompt to read the underlying filing. A `margin contraction` flag identifies a year-over-year operating-margin decline of at least 3 percentage points. A `growth deceleration` flag identifies a material slowing relative to the prior year’s growth rate. A `receivables warning` flag identifies receivables growth at least 10 percentage points above revenue growth.

The labels are deliberately conservative:

- **Stable:** no mechanical flags in the latest year.
- **Watch:** one flag; inspect the notes and business context.
- **Review:** two or more flags; prioritize deeper filing-level review.

## Limits on interpretation

Companies operate in different industries and use different fiscal calendars. Acquisitions, divestitures, accounting choices, and amended filings can materially affect these metrics. The model does not account for valuation, cash flow, debt, stock price, guidance, segment mix, or non-financial risk.

See `docs/methodology.md` for data extraction rules and limitations.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

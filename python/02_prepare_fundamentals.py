"""Standardize annual 10-K fundamentals from downloaded Company Facts JSON."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT = PROJECT_ROOT / "data" / "processed" / "annual_fundamentals.csv"
TICKERS = ["AAPL", "MSFT", "NVDA", "KO", "GOOGL"]

METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_income": ["OperatingIncomeLoss"],
    "accounts_receivable": ["AccountsReceivableNetCurrent", "AccountsReceivableNet"],
}


def annual_facts(facts: dict, metric: str) -> pd.DataFrame:
    """Select annual, latest-filed USD facts from the best available explicit tag."""
    candidates = []
    for tag in METRICS[metric]:
        tag_data = facts.get("us-gaap", {}).get(tag, {})
        rows = tag_data.get("units", {}).get("USD", [])
        cleaned = []
        for item in rows:
            if item.get("form") not in {"10-K", "10-K/A"} or item.get("fp") != "FY":
                continue
            if not item.get("fy") or not item.get("filed") or item.get("val") is None:
                continue
            fiscal_year = int(item["fy"])
            if fiscal_year < 2021 or fiscal_year > 2024:
                continue
            # Income-statement facts must be annual duration facts, not quarter-to-date values.
            if metric in {"revenue", "net_income", "operating_income"}:
                if not item.get("start"):
                    continue
                days = (pd.Timestamp(item["end"]) - pd.Timestamp(item["start"])).days
                if days < 300:
                    continue
            cleaned.append({"fiscal_year": fiscal_year, "value": float(item["val"]), "filed": item["filed"], "end": item.get("end"), "source_tag": tag})
        if cleaned:
            frame = pd.DataFrame(cleaned).sort_values(["fiscal_year", "filed"], ascending=[True, False])
            candidates.append(frame.drop_duplicates("fiscal_year", keep="first"))
    if candidates:
        # A later fallback can have fuller historical coverage than an otherwise valid first tag.
        return max(candidates, key=lambda frame: frame["fiscal_year"].nunique())
    raise ValueError(f"No annual 10-K USD fact found for {metric}. Tried: {METRICS[metric]}")


def main() -> None:
    rows = []
    for ticker in TICKERS:
        file_path = RAW_DIR / f"{ticker}_companyfacts.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Missing {file_path.name}. Run python/01_fetch_sec_data.py first.")
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        metric_frames = {metric: annual_facts(payload["facts"], metric) for metric in METRICS}
        years = set.intersection(*(set(frame["fiscal_year"]) for frame in metric_frames.values()))
        if len(years) < 3:
            raise ValueError(f"{ticker} has fewer than three common fiscal years across required metrics.")
        for fiscal_year in sorted(years):
            row = {"ticker": ticker, "company_name": payload["entityName"], "fiscal_year": fiscal_year}
            for metric, frame in metric_frames.items():
                record = frame.loc[frame["fiscal_year"] == fiscal_year].iloc[0]
                row[metric] = record["value"]
                row[f"{metric}_tag"] = record["source_tag"]
                row["filing_date"] = record["filed"]
                row["period_end"] = record["end"]
            rows.append(row)
    if not rows:
        raise FileNotFoundError("No raw SEC JSON found. Run python/01_fetch_sec_data.py first.")
    output = pd.DataFrame(rows).sort_values(["ticker", "fiscal_year"]).reset_index(drop=True)
    if output.duplicated(["ticker", "fiscal_year"]).any() or output[list(METRICS)].isna().any().any():
        raise ValueError("Prepared fundamentals failed uniqueness or completeness checks.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT, index=False, float_format="%.2f")
    print(f"Wrote {len(output)} annual records for {output.ticker.nunique()} companies.")
    print(output[["ticker", "fiscal_year", "revenue_tag", "accounts_receivable_tag"]].to_string(index=False))


if __name__ == "__main__":
    main()

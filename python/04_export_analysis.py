"""Export the SQL health view for charts, reporting, and Power BI/Excel use."""
from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "data" / "fundamental_screener.db"
OUTPUT = PROJECT_ROOT / "data" / "processed" / "company_health.csv"


def main() -> None:
    if not DATABASE.exists():
        raise FileNotFoundError("Run python/03_build_database.py first.")
    with sqlite3.connect(DATABASE) as connection:
        data = pd.read_sql_query("SELECT * FROM company_health WHERE fiscal_year >= 2021 ORDER BY ticker, fiscal_year", connection)
    if data.empty or data.duplicated(["ticker", "fiscal_year"]).any():
        raise ValueError("Company health export failed validation.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT, index=False, float_format="%.4f")
    print(f"Exported {len(data)} health records to {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

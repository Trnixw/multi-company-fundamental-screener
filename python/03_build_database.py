"""Create SQLite database and the SQL window-function health view."""
from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT = PROJECT_ROOT / "data" / "processed" / "annual_fundamentals.csv"
DATABASE = PROJECT_ROOT / "data" / "fundamental_screener.db"
SCHEMA = PROJECT_ROOT / "sql" / "schema.sql"
VIEW = PROJECT_ROOT / "sql" / "health_view.sql"


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError("Run python/02_prepare_fundamentals.py first.")
    data = pd.read_csv(INPUT)
    if DATABASE.exists():
        DATABASE.unlink()
    with sqlite3.connect(DATABASE) as connection:
        connection.executescript(SCHEMA.read_text(encoding="utf-8"))
        data.to_sql("annual_fundamentals", connection, if_exists="append", index=False)
        connection.executescript(VIEW.read_text(encoding="utf-8"))
        rows = connection.execute("SELECT COUNT(*) FROM company_health").fetchone()[0]
    print(f"Created {DATABASE.name} with {rows} health-view records.")


if __name__ == "__main__":
    main()

"""Fetch a small, documented cohort of SEC EDGAR company-facts responses."""
from __future__ import annotations

import gzip
import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
COMPANIES = {
    "AAPL": {"name": "Apple Inc.", "cik": "0000320193"},
    "MSFT": {"name": "Microsoft Corporation", "cik": "0000789019"},
    "NVDA": {"name": "NVIDIA Corporation", "cik": "0001045810"},
    "KO": {"name": "The Coca-Cola Company", "cik": "0000021344"},
    "GOOGL": {"name": "Alphabet Inc.", "cik": "0001652044"},
}


def fetch_json(cik: str, user_agent: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    request = Request(url, headers={"User-Agent": user_agent, "Accept-Encoding": "gzip"})
    with urlopen(request, timeout=60) as response:
        body = response.read()
        if response.headers.get("Content-Encoding") == "gzip":
            body = gzip.decompress(body)
    return json.loads(body)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    user_agent = os.getenv("SEC_USER_AGENT", "student-portfolio-project/1.0 contact: project-builder@localhost")
    for ticker, metadata in COMPANIES.items():
        output = RAW_DIR / f"{ticker}_companyfacts.json"
        payload = fetch_json(metadata["cik"], user_agent)
        output.write_text(json.dumps(payload), encoding="utf-8")
        print(f"Fetched {ticker}: {payload['entityName']}")
        time.sleep(0.2)  # respectful pace for the public API


if __name__ == "__main__":
    main()

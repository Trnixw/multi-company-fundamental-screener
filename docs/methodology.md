# Methodology and Responsible Use

## Data extraction

The SEC Company Facts API exposes machine-readable facts reported in XBRL filings. The pipeline requests company-specific JSON from `data.sec.gov`, uses annual 10-K facts, and pulls fiscal years 2021–2024 when available. It keeps the source XBRL tag selected for each metric in the processed output.

Companies can report similar concepts with different XBRL tags. The tool evaluates an explicit fallback list and selects the available tag with the strongest annual coverage. A missing required value is an error; it is never imputed.

## Alert interpretation

The flags compare a company with its own previous periods. They do not establish cause, predict returns, or treat companies as identical. A flag may arise from acquisitions, divestitures, accounting changes, seasonality, fiscal calendars, or other factors that require filing-level research.

## Limitations

1. Five companies are an illustrative project cohort, not a market-wide screen.
2. Fiscal years can end on different dates.
3. XBRL facts can be amended or revised after initial filing.
4. Receivables definitions and materiality vary by company.
5. This project is not investment research or investment advice.

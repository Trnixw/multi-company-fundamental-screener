CREATE TABLE IF NOT EXISTS annual_fundamentals (
    ticker TEXT NOT NULL,
    company_name TEXT NOT NULL,
    fiscal_year INTEGER NOT NULL,
    revenue REAL NOT NULL,
    net_income REAL NOT NULL,
    operating_income REAL NOT NULL,
    accounts_receivable REAL NOT NULL,
    revenue_tag TEXT NOT NULL,
    net_income_tag TEXT NOT NULL,
    operating_income_tag TEXT NOT NULL,
    accounts_receivable_tag TEXT NOT NULL,
    filing_date TEXT NOT NULL,
    period_end TEXT NOT NULL,
    PRIMARY KEY (ticker, fiscal_year)
);

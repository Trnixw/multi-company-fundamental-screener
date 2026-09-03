-- Latest available fiscal-year screening view for each company.
WITH latest_year AS (
    SELECT ticker, MAX(fiscal_year) AS fiscal_year
    FROM company_health
    GROUP BY ticker
)
SELECT
    h.ticker,
    h.company_name,
    h.fiscal_year,
    ROUND(h.revenue / 1000000000.0, 1) AS revenue_usd_bn,
    h.revenue_growth_pct,
    h.operating_margin_pct,
    h.net_margin_pct,
    h.receivables_growth_pct,
    h.flag_count,
    h.health_status
FROM company_health h
JOIN latest_year l USING (ticker, fiscal_year)
ORDER BY h.flag_count DESC, h.revenue_growth_pct ASC;

-- Trend alerts ordered from most flags to fewest.
SELECT
    ticker,
    fiscal_year,
    revenue_growth_pct,
    operating_margin_pct,
    receivables_growth_pct,
    margin_contraction_flag,
    growth_deceleration_flag,
    receivables_warning_flag,
    health_status
FROM company_health
WHERE fiscal_year >= 2022
ORDER BY flag_count DESC, ticker, fiscal_year;

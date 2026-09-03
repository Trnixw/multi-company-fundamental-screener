CREATE VIEW company_health AS
WITH base AS (
    SELECT
        ticker,
        company_name,
        fiscal_year,
        revenue,
        net_income,
        operating_income,
        accounts_receivable,
        filing_date,
        period_end,
        ROUND(100.0 * operating_income / revenue, 2) AS operating_margin_pct,
        ROUND(100.0 * net_income / revenue, 2) AS net_margin_pct,
        LAG(revenue) OVER (PARTITION BY ticker ORDER BY fiscal_year) AS prior_revenue,
        LAG(accounts_receivable) OVER (PARTITION BY ticker ORDER BY fiscal_year) AS prior_receivables,
        LAG(100.0 * operating_income / revenue) OVER (PARTITION BY ticker ORDER BY fiscal_year) AS prior_operating_margin_pct
    FROM annual_fundamentals
), trends AS (
    SELECT
        *,
        ROUND(100.0 * (revenue / NULLIF(prior_revenue, 0) - 1), 2) AS revenue_growth_pct,
        ROUND(100.0 * (accounts_receivable / NULLIF(prior_receivables, 0) - 1), 2) AS receivables_growth_pct,
        LAG(100.0 * (revenue / NULLIF(prior_revenue, 0) - 1)) OVER (PARTITION BY ticker ORDER BY fiscal_year) AS prior_revenue_growth_pct
    FROM base
), flagged AS (
    SELECT
        *,
        CASE WHEN prior_operating_margin_pct IS NOT NULL AND operating_margin_pct - prior_operating_margin_pct <= -3 THEN 1 ELSE 0 END AS margin_contraction_flag,
        CASE WHEN prior_revenue_growth_pct IS NOT NULL AND revenue_growth_pct - prior_revenue_growth_pct <= -5 THEN 1 ELSE 0 END AS growth_deceleration_flag,
        CASE WHEN revenue_growth_pct IS NOT NULL AND receivables_growth_pct - revenue_growth_pct >= 10 THEN 1 ELSE 0 END AS receivables_warning_flag
    FROM trends
)
SELECT
    *,
    margin_contraction_flag + growth_deceleration_flag + receivables_warning_flag AS flag_count,
    CASE
        WHEN margin_contraction_flag + growth_deceleration_flag + receivables_warning_flag >= 2 THEN 'review'
        WHEN margin_contraction_flag + growth_deceleration_flag + receivables_warning_flag = 1 THEN 'watch'
        ELSE 'stable'
    END AS health_status
FROM flagged;

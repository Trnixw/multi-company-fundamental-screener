"""Generate three portfolio-ready views of company fundamentals."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT = PROJECT_ROOT / "data" / "processed" / "company_health.csv"
OUTPUT = PROJECT_ROOT / "visualizations"


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError("Run python/04_export_analysis.py first.")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(INPUT)
    data["revenue_usd_bn"] = data["revenue"] / 1_000_000_000
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.lineplot(data=data, x="fiscal_year", y="revenue_usd_bn", hue="ticker", marker="o", linewidth=2, ax=ax)
    ax.set(title="Annual revenue trend by company", xlabel="Fiscal year", ylabel="Revenue (US$ billions)")
    ax.legend(title="Ticker")
    fig.tight_layout()
    fig.savefig(OUTPUT / "01_revenue_trend.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    plot = data.dropna(subset=["revenue_growth_pct", "operating_margin_pct"])
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.scatterplot(data=plot, x="revenue_growth_pct", y="operating_margin_pct", hue="ticker", size="revenue_usd_bn", sizes=(80, 600), ax=ax)
    for row in plot.loc[plot["fiscal_year"] == plot["fiscal_year"].max()].itertuples():
        ax.annotate(f"{row.ticker} {row.fiscal_year}", (row.revenue_growth_pct, row.operating_margin_pct), xytext=(4, 4), textcoords="offset points", fontsize=7)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.axvline(0, color="grey", linewidth=0.8)
    ax.set(title="Revenue growth and operating margin", xlabel="Revenue growth (%)", ylabel="Operating margin (%)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    fig.tight_layout()
    fig.savefig(OUTPUT / "02_growth_margin.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    latest = data.loc[data.groupby("ticker")["fiscal_year"].idxmax()].sort_values("flag_count", ascending=False)
    colors = latest["health_status"].map({"stable": "#2A9D8F", "watch": "#E9C46A", "review": "#E76F51"})
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(latest["ticker"], latest["flag_count"], color=colors)
    for y, row in enumerate(latest.itertuples()):
        ax.text(row.flag_count + 0.04, y, f"{row.health_status.title()} ({row.flag_count})", va="center")
    ax.set(title="Latest fiscal-year screening flags", xlabel="Number of flags", ylabel="", xlim=(0, 3.2))
    fig.tight_layout()
    fig.savefig(OUTPUT / "03_latest_flags.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("Wrote three charts to visualizations/.")


if __name__ == "__main__":
    main()

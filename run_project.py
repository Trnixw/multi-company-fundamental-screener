"""Run the full SEC fundamental-screening pipeline."""
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "python/01_fetch_sec_data.py",
    "python/02_prepare_fundamentals.py",
    "python/03_build_database.py",
    "python/04_export_analysis.py",
    "python/05_visualize.py",
    "python/06_generate_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n--- Running {script} ---")
        runpy.run_path(str(ROOT / script), run_name="__main__")
    print("\nPipeline complete. Open reports/final_report.md and visualizations/.")


if __name__ == "__main__":
    main()

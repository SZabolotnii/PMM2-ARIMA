# PMM2-ARIMA Reproducibility Package

This directory bundles everything reviewers need to regenerate the empirical results that feed into `latex/PMM2_ARIMA.tex`. The scripts reproduce both the WTI case-study analysis and the Monte Carlo experiments from Section 3.

## Repository Layout

- `data/` – immutable inputs delivered with the package (`DCOILWTICO.csv` from FRED).
- `scripts/` – R entry points that orchestrate analysis, plotting, and reporting.
- `results/` – auto-generated artefacts (CSV tables, RDS stores, plots, Markdown report, Monte Carlo summaries).
- `latex/` – manuscript sources (`PMM2_ARIMA.tex`, `references.bib`).
- `DESCRIPTION` – declared R dependencies for quick inspection/tooling.

## Requirements

- R ≥ 4.3 (tested with 4.3.2).
- R packages: `EstemPMM`, `ggplot2`, `gridExtra`, `RColorBrewer`, `tseries`, `knitr`, `MASS`.
  - Install via CRAN where possible, and obtain `EstemPMM` from the project repository:  
    `remotes::install_github("SZabolotnii/EstemPMM")`
- Optional: `pandoc` if you plan to convert the Markdown report to HTML/PDF, and a LaTeX distribution (`TeXLive`, `TinyTeX`, …) to compile `latex/PMM2_ARIMA.tex`.

## Reproducing the WTI Experiment

From the root of this directory, run:

```bash
Rscript scripts/run_full_study.R
```

The command will:

1. Fit all ARIMA specifications with CSS-ML vs PMM2 (`scripts/comprehensive_study.R`).
2. Regenerate the 10 publication plots (`scripts/create_visualizations.R`).
3. Rebuild the narrative Markdown report (`scripts/generate_report.R`).

You can also execute any step individually:

```bash
# Quick console-only sanity check
Rscript scripts/arima_oil_quick_demo.R

# Full modelling pipeline
Rscript scripts/comprehensive_study.R

# Visuals and report (after the previous step)
Rscript scripts/create_visualizations.R
Rscript scripts/generate_report.R
```

## Output Map

After a successful run you should see:

- `results/full_results.csv` – values used in Table \ref{tab:wti_comprehensive_results} of the manuscript.
- `results/method_comparison.csv` – deltas reported in Table \ref{tab:wti_method_comparison}.
- `results/descriptive_stats.csv` – descriptive panel in Section 4.
- `results/plots/*.png` – Figures 1–10 (numbered to match captions).
- `results/ANALYTICAL_REPORT.md` – extended prose that aligns with the LaTeX discussion.
- `results/monte_carlo/*.csv` – simulation summaries mirroring the Monte Carlo tables (per-model metrics, relative efficiencies, residual cumulants).
- `results/monte_carlo/article_comparison.csv` – expanded table that juxtaposes симуляційні оцінки з опублікованими у статті величинами та додає відхилення/співвідношення.

The numerical values in the LaTeX tables were exported by doubling the AIC/BIC scores for formatting purposes; the CSV files contain the raw outputs from R. Reviewers can regenerate the manuscript by re-running the scripts and then compiling `latex/PMM2_ARIMA.tex`.

## Monte Carlo симуляції

The dedicated driver `scripts/run_monte_carlo.R` reconstructs the simulation study (default: 2000 повторень на комбінацію, seed = 12345). Expect the full run to take 20–40 хвилин залежно від обладнання.

```bash
# Повний запуск Monte Carlo
Rscript scripts/run_monte_carlo.R

# Кастомізація (менше повторень для швидкої перевірки)
Rscript scripts/run_monte_carlo.R --reps=200 --seed=20250101

# Варіація припущень
Rscript scripts/run_monte_carlo.R --standardize-innov=false --css-method=CSS-ML
```

Опції `--standardize-innov` та `--css-method` дають змогу перевіряти чутливість до масштабу інновацій та типу класичної оцінки (доступні значення: `CSS`, `CSS-ML`, `ML`). Прапорець `--m-est=false` вимикає додаткові робастні оцінки, які за замовчуванням обчислюються для AR-компонент.

Ключові артефакти:

- `monte_carlo_metrics.csv` – повний зріз метрик (bias, var, MSE, RE, VR) для кожної моделі, параметра й розподілу.
- `arima110_summary.csv`, `arima110_re_vs_sample_size.csv` – дані для таблиць ARIMA(1,1,0) та залежності RE від N.
- `arima011_summary.csv`, `arima111_summary.csv`, `arima210_summary.csv` – скорочені порівняння для інших конфігурацій.
- `arima110_residual_cumulants.csv` – середні кумулянти залишків PMM2 (Таблиця \ref{tab:residual_cumulants}).
- `article_comparison.csv` – порівняння симуляцій з опублікованими значеннями та нові колонки з відхиленнями.
- Колонка `M-EST` у зведених файлах містить результати Hubерівських M-оцінок для AR-компонентів, що дає змогу порівняти PMM2/CSS з робастними оцінками.

## Open Items

- **`EstemPMM` provenance:** document the exact commit or release used when you freeze the archive so reviewers can install the same implementation.

## Housekeeping

- `results/` ships with a `.gitignore`; delete or replace the placeholder when publishing generated artefacts.
- Use `DESCRIPTION` with `renv` or `pak` if you wish to create a fully locked environment before sharing.

# PMM2-ARIMA Reproducibility Package

This directory bundles everything reviewers need to regenerate the empirical results that feed into `latex/PMM2_ARIMA.tex`. Running the scripts rebuilds the WTI case-study tables, figures, and analytical markdown report without touching the Monte Carlo material (see *Open Items* below).

## Repository Layout

- `data/` – immutable inputs delivered with the package (`DCOILWTICO.csv` from FRED).
- `scripts/` – R entry points that orchestrate analysis, plotting, and reporting.
- `results/` – auto-generated artefacts (CSV tables, RDS stores, plots, Markdown report).
- `latex/` – manuscript sources (`PMM2_ARIMA.tex`, `references.bib`).
- `DESCRIPTION` – declared R dependencies for quick inspection/tooling.

## Requirements

- R ≥ 4.3 (tested with 4.3.2).
- R packages: `EstemPMM`, `ggplot2`, `gridExtra`, `RColorBrewer`, `tseries`, `knitr`.
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

The numerical values in the LaTeX tables were exported by doubling the AIC/BIC scores for formatting purposes; the CSV files contain the raw outputs from R. Reviewers can regenerate the manuscript by re-running the scripts and then compiling `latex/PMM2_ARIMA.tex`.

## Open Items

- **Monte Carlo experiments:** Section 3 of the manuscript summarises simulation studies that are not yet scripted in this repository. Porting those experiments is the last missing component for full reproducibility.
- **`EstemPMM` provenance:** document the exact commit or release used when you freeze the archive so reviewers can install the same implementation.

## Housekeeping

- `results/` ships with a `.gitignore`; delete or replace the placeholder when publishing generated artefacts.
- Use `DESCRIPTION` with `renv` or `pak` if you wish to create a fully locked environment before sharing.


.PHONY: all analysis plots report quick-demo latex clean

all: analysis plots report

analysis:
	Rscript scripts/comprehensive_study.R

plots:
	Rscript scripts/create_visualizations.R

report:
	Rscript scripts/generate_report.R

quick-demo:
	Rscript scripts/arima_oil_quick_demo.R

latex:
	latexmk -pdf -cd latex/PMM2_ARIMA.tex

clean:
	find results -mindepth 1 ! -name '.gitignore' -delete

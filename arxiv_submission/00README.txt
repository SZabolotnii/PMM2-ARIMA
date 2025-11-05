arXiv Submission Package for PMM2ARIMA Paper
=============================================

IMPORTANT: This directory is ready for submission to arXiv.org
You can either upload this as a ZIP archive or upload individual files.

Title: Applying the Polynomial Maximization Method to Estimate ARIMA Models
       with Asymmetric Non-Gaussian Innovations

Author: Serhii Zabolotnii
        Cherkasy State Business College, Cherkasy, Ukraine

Date: November 2025

FILES INCLUDED:
---------------

1. PMM2_ARIMA.tex        - Main LaTeX source file
2. references.bib        - BibTeX bibliography file
3. figures/              - Directory with 13 PDF figures

COMPILATION INSTRUCTIONS:
-------------------------

To compile this document, run the following commands in sequence:

  pdflatex PMM2_ARIMA.tex
  bibtex PMM2_ARIMA
  pdflatex PMM2_ARIMA.tex
  pdflatex PMM2_ARIMA.tex

The document uses standard LaTeX packages and should compile without issues
on the arXiv system.

COMPILER: PDFLaTeX
FIGURE FORMAT: PDF (version 1.4)
BIBLIOGRAPHY STYLE: unsrt

NOTES FOR arXiv:
----------------

- All figures are in PDF format (compatible with PDFLaTeX)
- No external dependencies beyond standard LaTeX packages
- UTF-8 encoding with T1 font encoding
- Document class: article (11pt, a4paper)

For questions, contact: zabolotnii.serhii@csbc.edu.ua

Generated: 2025-11-05

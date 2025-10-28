#!/bin/bash
# ============================================
# LaTeX Compilation Script for PMM2-ARIMA Paper
# ============================================
# This script compiles the LaTeX document with bibliography
# Usage: ./compile.sh [filename_without_extension]
# Example: ./compile.sh PMM2_ARIMA_Part1
# ============================================

# Check if filename provided
if [ -z "$1" ]; then
    echo "Usage: $0 <filename_without_extension>"
    echo "Example: $0 PMM2_ARIMA_Part1"
    exit 1
fi

FILENAME=$1

# Check if file exists
if [ ! -f "${FILENAME}.tex" ]; then
    echo "Error: ${FILENAME}.tex not found!"
    exit 1
fi

echo "============================================"
echo "Compiling ${FILENAME}.tex..."
echo "============================================"

# First pass - generate aux file
echo "[1/4] Running pdflatex (first pass)..."
pdflatex -interaction=nonstopmode "${FILENAME}.tex" > /dev/null

if [ $? -ne 0 ]; then
    echo "Error in first pdflatex pass! Check ${FILENAME}.log for details"
    exit 1
fi

# Generate bibliography
echo "[2/4] Running bibtex..."
bibtex "${FILENAME}" > /dev/null

if [ $? -ne 0 ]; then
    echo "Warning: bibtex had issues. Continuing anyway..."
fi

# Second pass - incorporate bibliography
echo "[3/4] Running pdflatex (second pass)..."
pdflatex -interaction=nonstopmode "${FILENAME}.tex" > /dev/null

if [ $? -ne 0 ]; then
    echo "Error in second pdflatex pass! Check ${FILENAME}.log for details"
    exit 1
fi

# Final pass - resolve all references
echo "[4/4] Running pdflatex (final pass)..."
pdflatex -interaction=nonstopmode "${FILENAME}.tex" > /dev/null

if [ $? -ne 0 ]; then
    echo "Error in final pdflatex pass! Check ${FILENAME}.log for details"
    exit 1
fi

echo "============================================"
echo "✓ Compilation successful!"
echo "Output: ${FILENAME}.pdf"
echo "============================================"

# Clean up auxiliary files (optional)
read -p "Clean up auxiliary files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "${FILENAME}.aux" "${FILENAME}.log" "${FILENAME}.out" \
          "${FILENAME}.toc" "${FILENAME}.bbl" "${FILENAME}.blg"
    echo "✓ Auxiliary files cleaned"
fi

# Open PDF (if on macOS/Linux with xdg-open)
if command -v xdg-open &> /dev/null; then
    read -p "Open PDF? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open "${FILENAME}.pdf" &
    fi
fi

echo "Done!"

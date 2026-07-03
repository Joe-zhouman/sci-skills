#!/usr/bin/env bash
# Compile script for LaTeX cover letter with bibliography

BASENAME="cover_letter"

# Clean previous build artifacts
rm -f "${BASENAME}".{aux,bbl,blg,dvi,log,out,pdf}

# Run pdflatex (first pass - generates .aux file)
pdflatex "${BASENAME}.tex"

# Run bibtex if bibliography exists and is non-empty
if [ -s "sample.bib" ]; then
    bibtex "${BASENAME}"
    # Second pdflatex pass - incorporates bibliography
    pdflatex "${BASENAME}.tex"
    # Third pdflatex pass - resolves references
    pdflatex "${BASENAME}.tex"
fi

echo "Compilation complete: ${BASENAME}.pdf"

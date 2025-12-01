# LaTeX Report - AMD Final Project A1

## Structure

- `report.tex` - Main LaTeX document
- `figures/` - Directory for images (to be created)

## Required Images

Place the following images in the `figures/` directory:

1. `dataset_description.png` - Screenshot of dataset description
2. `dataset_original.png` - Screenshot of original CSV file
3. `dataset_orange.png` - Screenshot of dataset loaded in Orange
4. `oneR_execution.png` - Screenshot of 1R execution in terminal
5. `data_table.png` - Screenshot of data table in Orange
6. `distribution_classes.png` - Screenshot of class distribution
7. `tree_classification.png` - Screenshot of Tree classifier result
8. `rf_confusion_matrix.png` - Screenshot of Random Forest confusion matrix
9. `pythagorean_forest.png` - Screenshot of Pythagorean Forest visualization
10. `tree_confusion_matrix.png` - Screenshot of Tree confusion matrix

## Compilation

### Using pdflatex
```bash
cd report_latex
pdflatex report.tex
pdflatex report.tex  # Run twice for table of contents
```

### Using latexmk (recommended)
```bash
cd report_latex
latexmk -pdf report.tex
```

### Using online editors
Upload `report.tex` to [Overleaf](https://www.overleaf.com/) or similar online LaTeX editors.

## Required LaTeX Packages

All packages used are standard and should be included in most LaTeX distributions:
- inputenc
- babel (Portuguese)
- graphicx
- geometry
- hyperref
- fancyhdr
- titlesec
- enumitem
- float

## Notes

- The document is set to A4 paper size with 12pt font
- Portuguese language support is enabled
- All figure references use `\ref{}` for automatic numbering
- The document includes a title page and table of contents

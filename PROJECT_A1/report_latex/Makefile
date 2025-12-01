# Makefile for LaTeX report compilation

# Main document name (without .tex extension)
DOCUMENT = report

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex

# Output directory
OUTDIR = .

.PHONY: all clean cleanall view

# Default target
all: $(DOCUMENT).pdf

# Compile PDF (run twice for references)
$(DOCUMENT).pdf: $(DOCUMENT).tex
	$(LATEX) -output-directory=$(OUTDIR) $(DOCUMENT).tex
	$(LATEX) -output-directory=$(OUTDIR) $(DOCUMENT).tex

# Clean auxiliary files
clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz

# Clean all generated files including PDF
cleanall: clean
	rm -f $(DOCUMENT).pdf

# View the PDF (Linux)
view: $(DOCUMENT).pdf
	xdg-open $(DOCUMENT).pdf &

# Help target
help:
	@echo "Available targets:"
	@echo "  all       - Compile the PDF (default)"
	@echo "  clean     - Remove auxiliary files"
	@echo "  cleanall  - Remove all generated files including PDF"
	@echo "  view      - Open the PDF with default viewer"
	@echo "  help      - Show this help message"

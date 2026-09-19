#!/bin/sh
# One-command build of the Beamer presentation (run from Project_Simulator/).
set -e
pdflatex -interaction=nonstopmode phase3_presentation_beamer.tex
pdflatex -interaction=nonstopmode phase3_presentation_beamer.tex

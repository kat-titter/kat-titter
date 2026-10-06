#!/bin/sh
# Render the PDFs from the self-contained HTML sources with headless Chrome.
set -e
cd "$(dirname "$0")"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/Katherine_Titterton_Resume.pdf" "file://$PWD/resume.html"
"$CH" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/Katherine_Titterton_CV.pdf"     "file://$PWD/cv.html"
echo "rendered Katherine_Titterton_Resume.pdf and Katherine_Titterton_CV.pdf"

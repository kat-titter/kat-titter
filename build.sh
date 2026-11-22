#!/bin/sh
# Check references and fit, then render the PDFs from the self-contained HTML sources with headless Chrome.
set -e
cd "$(dirname "$0")"
python3 check_refs.py
python3 measure_fit.py resume.html
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/Katherine_Titterton_Resume.pdf" "file://$PWD/resume.html" 2>/dev/null
"$CH" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/Katherine_Titterton_CV.pdf"     "file://$PWD/cv.html" 2>/dev/null
echo "rendered Katherine_Titterton_Resume.pdf and Katherine_Titterton_CV.pdf"

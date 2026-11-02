#!/usr/bin/env bash
# Assemble the self-contained Springer camera-ready package for PanAfriCon AI 2026
# and compile it from scratch inside the package, so the bundled PDF corresponds
# exactly to the bundled sources. Output: submission/ and submission112.zip.
set -euo pipefail
cd "$(dirname "$0")"

OUT=submission
rm -rf "$OUT" submission112.zip
mkdir "$OUT"

cp llncs.cls splncs04.bst NotoSansEthiopic-Regular.ttf "$OUT"/
cp ../references.bib "$OUT"/main.bib
sed 's#\\bibliography{../references}#\\bibliography{main}#' main.tex > "$OUT"/main.tex
grep -q '\\bibliography{main}' "$OUT"/main.tex

cat > "$OUT"/README.txt <<'EOF'
Submission 112, PanAfriCon AI 2026 (Springer CCIS), camera-ready sources.

Compile with LuaLaTeX (required for the Ge'ez-script sample):
  lualatex main && bibtex main && lualatex main && lualatex main

Files:
  main.tex                      paper source (LLNCS template v2.25)
  main.bib, main.bbl            references (splncs04 style)
  main.pdf                      final PDF, built from these files
  DescriptionTexts.txt          alternative text for Fig. 1 (written by llncs.cls)
  llncs.cls, splncs04.bst       Springer class and bibliography style
  NotoSansEthiopic-Regular.ttf  Ge'ez-script font (SIL Open Font License 1.1)

Corresponding author: Hailay Kidu Teklehaymanot (teklehaymanot@l3s.de)
EOF

cd "$OUT"
lualatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
bibtex main >/dev/null
lualatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
lualatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
rm -f main.aux main.blg main.log main.out
cd ..

zip -q -r submission112.zip "$OUT"
echo "Built $OUT/ and submission112.zip"

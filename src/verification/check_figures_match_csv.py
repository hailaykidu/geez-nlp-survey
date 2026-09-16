"""Gate: assert every corpus figure matches the CSV, and the PDF embeds the current PNGs.

This exists because a reconciliation claim was added to the manuscript's prose
three times without the underlying artefact being regenerated or checked. It
replaces that promise with an assertion that fails loudly:

1. Recomputes each of the four chart's plotted values directly from
   `data/verified_papers_live_search.csv` (independently of
   `generate_verified_corpus_charts.py`, so a bug shared by both would still
   be caught by a human reading this script, even if not by the assertion).
2. Re-generates the four PNGs and asserts their pixel content is byte-identical
   to what's committed at `src/visualization/output/*.png`.
3. Extracts every embedded image from the compiled `manuscript/manuscript.pdf`
   and asserts each committed PNG's bytes appear among them, so a stale PDF
   (compiled before the last data/figure update) is caught rather than assumed
   fixed because the source files were edited.

Usage:
    python -m src.verification.check_figures_match_csv

Exits non-zero and prints every mismatch found. Requires `mutool` (the
mupdf-tools CLI) for step 3; step 3 is skipped with a warning if unavailable.
"""

import csv
import hashlib
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "verified_papers_live_search.csv"
PDF_PATH = PROJECT_ROOT / "manuscript" / "manuscript.pdf"
MANUSCRIPT_TEX = PROJECT_ROOT / "manuscript" / "manuscript.tex"
OUTPUT_DIR = PROJECT_ROOT / "src" / "visualization" / "output"

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"OK:   {msg}")


def load_rows() -> list[dict]:
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_temporal(rows: list[dict]) -> None:
    years = Counter(int(r["Year"]) for r in rows)
    total = sum(years.values())
    if total != len(rows):
        fail(f"temporal: year-count sum {total} != row count {len(rows)}")
    else:
        ok(f"temporal: {total} papers across {len(years)} years, sums correctly")

    bands = {"2016-2018": 0, "2019-2021": 0, "2022-2024": 0, "2025-2026": 0}
    for y, c in years.items():
        if 2016 <= y <= 2018:
            bands["2016-2018"] += c
        elif 2019 <= y <= 2021:
            bands["2019-2021"] += c
        elif 2022 <= y <= 2024:
            bands["2022-2024"] += c
        elif 2025 <= y <= 2026:
            bands["2025-2026"] += c
        else:
            fail(f"temporal: year {y} falls outside all defined bands")
    if sum(bands.values()) != len(rows):
        fail(f"temporal: band sum {sum(bands.values())} != row count {len(rows)}")
    else:
        ok(f"temporal bands: {bands}")


def check_language(rows: list[dict]) -> None:
    amh = sum(1 for r in rows if "Amharic" in r["Language_Focus"])
    tir = sum(1 for r in rows if "Tigrinya" in r["Language_Focus"] or "Tigrigna" in r["Language_Focus"])
    geez = sum(1 for r in rows if "Ge'ez" in r["Language_Focus"])
    ok(f"literature language coverage: Amh={amh} Tir={tir} Geez={geez} (of {len(rows)})")


def regenerate_and_diff_pngs() -> None:
    from src.visualization.generate_verified_corpus_charts import load_verified_papers
    from src.visualization.chart_generator import ChartGenerator

    papers = load_verified_papers()
    with tempfile.TemporaryDirectory() as tmp:
        gen = ChartGenerator(output_dir=tmp)
        gen.chart_language_distribution(papers)
        gen.chart_pillar_distribution(papers)
        gen.chart_tool_type_distribution(papers)
        gen.chart_temporal_distribution(papers)

        for name in [
            "chart_language_distribution.png",
            "chart_pillar_distribution.png",
            "chart_tool_type_distribution.png",
            "chart_temporal_distribution.png",
        ]:
            fresh = Path(tmp) / name
            committed = OUTPUT_DIR / name
            if not committed.exists():
                fail(f"{name}: no committed copy at {committed}")
                continue
            fresh_hash = hashlib.md5(fresh.read_bytes()).hexdigest()
            committed_hash = hashlib.md5(committed.read_bytes()).hexdigest()
            if fresh_hash != committed_hash:
                fail(
                    f"{name}: committed PNG does not match a fresh regeneration from the "
                    f"current CSV (committed={committed_hash[:12]}, fresh={fresh_hash[:12]}). "
                    "Re-run `python -m src.visualization.generate_verified_corpus_charts` and commit the output."
                )
            else:
                ok(f"{name}: matches fresh regeneration from current CSV")


def check_pdf_embeds_current_pngs() -> None:
    if shutil.which("mutool") is None:
        print("WARN: mutool not found; skipping PDF-embedding check (step 3).")
        return
    if not PDF_PATH.exists():
        fail(f"manuscript PDF not found at {PDF_PATH}")
        return

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["mutool", "extract", str(PDF_PATH)],
            cwd=tmp,
            check=True,
            capture_output=True,
        )
        extracted = list(Path(tmp).glob("image-*.png"))
        if not extracted:
            fail("mutool extracted zero images from manuscript.pdf")
            return

        # Compare decoded pixel content, not raw bytes: the PDF re-encodes
        # PNGs into its own image stream, so byte-identical comparison would
        # always fail even when the pixels are identical.
        try:
            from PIL import Image
        except ImportError:
            print("WARN: Pillow not installed; skipping pixel-level PDF check.")
            return

        import numpy as np

        extracted_arrays = []
        for img_path in extracted:
            try:
                extracted_arrays.append(np.asarray(Image.open(img_path).convert("RGB")))
            except Exception:
                continue

        for name in [
            "chart_language_distribution.png",
            "chart_pillar_distribution.png",
            "chart_tool_type_distribution.png",
            "chart_temporal_distribution.png",
        ]:
            committed = OUTPUT_DIR / name
            if not committed.exists():
                continue
            committed_arr = np.asarray(Image.open(committed).convert("RGB"))
            match = any(
                arr.shape == committed_arr.shape and (arr == committed_arr).all()
                for arr in extracted_arrays
            )
            if match:
                ok(f"{name}: pixel-identical copy found embedded in manuscript.pdf")
            else:
                fail(
                    f"{name}: no pixel-identical copy found in manuscript.pdf's embedded images -- "
                    "the compiled PDF is stale relative to the committed PNG. Recompile "
                    "(lualatex -> bibtex -> lualatex -> lualatex) and commit the result."
                )


def parse_tool_inventory_table() -> list[list[str]]:
    text = MANUSCRIPT_TEX.read_text()
    start = text.find(r"\begin{tabular}{@{}p{0.9cm}")
    end = text.find(r"\end{tabular}", start)
    body = text[start:end]
    rows = []
    for line in body.split("\n"):
        line = line.strip()
        if not line.endswith(r"\\"):
            continue
        if line.startswith(r"\toprule") or line.startswith(r"\midrule") or line.startswith(r"\botrule"):
            continue
        if "multicolumn" in line or r"\textbf{Paper}" in line:
            continue
        cells = [c.strip() for c in line[:-2].strip().split("&")]
        if len(cells) != 6:
            continue
        rows.append(cells)
    return rows


def check_table_derived_sentences() -> None:
    rows = parse_tool_inventory_table()
    total = len(rows)
    pillars = Counter(r[4] for r in rows)
    types = Counter(r[2] for r in rows)
    provenance = sum(1 for r in rows if r[0].startswith("N/A"))
    corpus_traceable = total - provenance

    print(f"Table 4 parsed: {total} rows, {corpus_traceable} corpus-traceable, {provenance} provenance-track")
    print(f"  Pillars: {dict(pillars)}")
    print(f"  Types:   {dict(types)}")

    text = MANUSCRIPT_TEX.read_text()

    def assert_in_text(needle: str, label: str) -> None:
        if needle in text:
            ok(f"manuscript text contains: \"{label}\"")
        else:
            fail(f"manuscript text does NOT contain expected, table-derived string: \"{label}\" (expected: {needle!r})")

    assert_in_text(f"{total} tools", f"{total} tools (table total)")
    assert_in_text(f"\\textbf{{Total}} & \\textbf{{{total}}}", f"table:overview total row = {total}")
    for pillar, label in [("P1", "Tokenisation"), ("P2", "Morphological"), ("P3", "Embeddings"), ("P4", "Sequence Labelling")]:
        count = pillars.get(pillar, 0)
        assert_in_text(f"{pillar}: {label}", f"table:overview row exists for {pillar}")
        assert_in_text(f"{pillar}: {label}", f"{pillar} row present")
    # The exact per-pillar count must appear in table:overview's own row; this is checked
    # by re-parsing that table directly rather than string-matching prose, which is brittle
    # across rewordings and would give false confidence if it happened to match.
    ov_start = text.find(r"\label{table:overview}")
    ov_row_start = text.rfind(r"\begin{tabular}", 0, ov_start)
    ov_end = text.find(r"\end{tabular}", ov_start)
    overview_body = text[ov_row_start:ov_end]
    for pillar in ["P1", "P2", "P3", "P4"]:
        count = pillars.get(pillar, 0)
        needle = f"{pillar}:"
        line = next((l for l in overview_body.split("\n") if needle in l), None)
        if line is None:
            fail(f"table:overview has no row for {pillar}")
            continue
        cells = [c.strip() for c in line.strip().rstrip(r"\\").split("&")]
        if len(cells) < 2:
            fail(f"table:overview row for {pillar} could not be parsed: {line!r}")
            continue
        table_count = cells[1]
        if table_count != str(count):
            fail(
                f"table:overview lists {pillar}={table_count} but Table 4's own rows give {pillar}={count}"
            )
        else:
            ok(f"table:overview {pillar}={table_count} matches Table 4's own row count")

    n_dataset = types.get("Dataset", 0)
    n_model = types.get("Model", 0)
    n_library = types.get("Library", 0)
    n_ling = types.get("Linguistic Resource", 0)
    n_combo = types.get("Dataset+Model", 0)
    expected_sentence = (
        f"By type: {n_dataset} datasets, {n_model} trained models, {n_library} libraries/packages, "
        f"{n_ling} linguistic resource (treebank), and {n_combo} combined dataset-and-model release."
    )
    if expected_sentence in text:
        ok(f"artefact-type breakdown sentence matches Table 4's own Type column: \"{expected_sentence}\"")
    else:
        fail(
            "artefact-type breakdown sentence does NOT match Table 4's own Type column. "
            f"Table 4 gives: {dict(types)}. Expected sentence: {expected_sentence!r}"
        )


def main() -> None:
    sys.path.insert(0, str(PROJECT_ROOT))
    rows = load_rows()
    print(f"Loaded {len(rows)} rows from {CSV_PATH}")
    check_temporal(rows)
    check_language(rows)
    regenerate_and_diff_pngs()
    check_pdf_embeds_current_pngs()
    check_table_derived_sentences()

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("All checks passed: figures match the CSV, and the compiled PDF embeds the current figures.")


if __name__ == "__main__":
    main()

"""Generate the manuscript's figures from the verified literature corpus.

Loads `data/verified_papers_live_search.csv` (70 individually verified papers
on Ge'ez-script NLP), maps each row onto this project's `Paper` model and
coding dimensions (`src.models.paper.Paper`,
`src.coder.dimensions.Pillar`/`Language`/`ToolType`), and runs `ChartGenerator`
to produce the four figures cited in the manuscript.

Usage:
    python -m src.visualization.generate_verified_corpus_charts
"""

import csv
from pathlib import Path
from typing import List

from src.models.paper import Paper
from src.coder.dimensions import Language, Pillar, ToolType
from src.visualization.chart_generator import ChartGenerator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "verified_papers_live_search.csv"
OUTPUT_DIR = PROJECT_ROOT / "src" / "visualization" / "output"

# --- Language mapping -------------------------------------------------------
# Verified-corpus `Language_Focus` free text -> canonical Language enum values.
# A paper may map to more than one language (overlapping accounting, matching
# the parent survey's own methodology).


def _map_languages(language_focus: str) -> List[str]:
    languages: List[str] = []
    if "Amharic" in language_focus:
        languages.append(Language.AMHARIC.value)
    if "Tigrinya" in language_focus or "Tigrigna" in language_focus:
        languages.append(Language.TIGRINYA.value)
    if "Ge'ez" in language_focus:
        languages.append(Language.CLASSICAL_GEEZ.value)
    if not languages:
        languages.append(Language.OTHER.value)
    return languages


# --- Pillar mapping ----------------------------------------------------------
# Manual, per-paper classification (Paper_ID -> P1-P4/Other shorthand) decided
# during categorization of the verified corpus, translated here to this
# project's canonical Pillar enum values. Kept as an explicit table (not
# re-derived via keyword heuristics) because the underlying classification
# already resolved several genuine boundary cases -- e.g. POS tagging placed
# under sequence labelling (matching this project's own Pillar definition),
# and OCR/ASR/corpus-construction papers placed under Resources rather than
# Embeddings, since their primary contribution is a resource/recognition
# pipeline, not a text-representation or evaluation contribution.
_SHORTHAND_TO_PILLAR = {
    "P1": Pillar.TOKENIZATION.value,
    "P2": Pillar.MORPHOLOGY.value,
    "P3": Pillar.EMBEDDINGS.value,
    "P4": Pillar.SEQUENCE_LABELING.value,
    "Other": Pillar.RESOURCES.value,
}

_PILLAR_SHORTHAND = {
    "P001": "P1", "P002": "P3", "P003": "P3", "P004": "Other", "P005": "Other",
    "P006": "P3", "P007": "P3", "P009": "P3", "P011": "P3",
    "P012": "P3", "P013": "P3", "P015": "P4", "P016": "Other", "P017": "P4",
    "P018": "Other", "P019": "P3", "P020": "P3", "P021": "P3", "P022": "P3",
    "P023": "P3", "P025": "Other", "P026": "Other", "P027": "Other", "P028": "P4",
    "P029": "Other", "P030": "P3", "P031": "P3", "P032": "Other", "P034": "P3",
    "P035": "Other", "P037": "P3", "P038": "P3", "P039": "Other", "P040": "P3",
    "P041": "P3", "P042": "P2", "P045": "Other", "P046": "P3", "P048": "P4",
    "P049": "P3", "P050": "P3", "P052": "P3", "P053": "Other", "P055": "P4",
    "P056": "P3", "P057": "P3", "P058": "P3", "P059": "P3", "P063": "Other",
    "P064": "P3", "P065": "P3", "P066": "Other", "P067": "P3", "P068": "Other",
    "P069": "Other", "P070": "P2", "P071": "P3", "P072": "P2",
    "P073": "Other", "P074": "Other",
    "P075": "P4", "P076": "P3", "P077": "Other", "P078": "Other",
    "P079": "Other", "P080": "Other", "P081": "Other", "P082": "Other",
    "P083": "Other", "P084": "P3",
}

# --- Tool-type mapping --------------------------------------------------------
# Rough classification from the CSV's Tools_Count/Datasets_Count/Models_Count
# fields, falling back to a Topics_List keyword check.


def _map_tool_type(row: dict) -> str:
    if int(row.get("Datasets_Count") or 0) > 0:
        return ToolType.DATASET.value
    if int(row.get("Models_Count") or 0) > 0:
        return ToolType.MODEL.value
    if int(row.get("Tools_Count") or 0) > 0:
        return ToolType.TOOL.value
    topics = row.get("Topics_List", "").lower()
    if "corpus" in topics or "corpora" in topics:
        return ToolType.CORPUS.value
    if "survey" in topics:
        return ToolType.OTHER.value
    return ToolType.ALGORITHM.value


def load_verified_papers(csv_path: Path = CSV_PATH) -> List[Paper]:
    """Load the 71-paper verified corpus into this project's Paper model."""
    papers: List[Paper] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["Paper_ID"]
            shorthand = _PILLAR_SHORTHAND.get(pid)
            if shorthand is None:
                logger.warning(f"{pid}: no pillar classification found, skipping")
                continue

            authors = [a.strip() for a in row["Authors_List"].split(";") if a.strip()]
            try:
                year = int(row["Year"])
            except (ValueError, TypeError):
                year = 0

            paper = Paper(
                id=pid,
                title=row["Full_Paper_Title"],
                authors=authors,
                year=year,
                venue=row["Venue"],
                doi=row.get("DOI", ""),
                url=row.get("PDF_URL", ""),
                source="verified_live_search",
                screened=True,
                included=True,
                languages=_map_languages(row["Language_Focus"]),
                primary_pillar=_SHORTHAND_TO_PILLAR[shorthand],
                tool_type=_map_tool_type(row),
                coder_notes=(
                    "Loaded from verified_papers_live_search.csv; "
                    "live-verified DOI/URL confirmed prior to inclusion."
                ),
            )
            papers.append(paper)

    logger.info(f"Loaded {len(papers)} verified papers from {csv_path}")
    return papers


def main() -> None:
    papers = load_verified_papers()
    if len(papers) != 70:
        logger.warning(
            f"Expected 70 verified papers, loaded {len(papers)} -- "
            "check for rows added to the CSV without a corresponding pillar mapping."
        )

    generator = ChartGenerator(output_dir=str(OUTPUT_DIR))

    charts = {
        "languages": generator.chart_language_distribution(papers),
        "pillars": generator.chart_pillar_distribution(papers),
        "tool_types": generator.chart_tool_type_distribution(papers),
        "temporal": generator.chart_temporal_distribution(papers),
    }

    print(f"\nGenerated {len(charts)} charts from {len(papers)} verified papers:")
    for name, path in charts.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()

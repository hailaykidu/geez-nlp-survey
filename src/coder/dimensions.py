"""Enum definitions used to classify papers by language, pillar, and tool type.

These enums provide the canonical string values used in
`src/visualization/generate_verified_corpus_charts.py` when mapping rows of
`data/verified_papers_live_search.csv` onto the `Paper` model
(`src/models/paper.py`) for figure generation. The value assigned to each
paper (language coverage, pillar, tool type) is the classification reported
in the manuscript's tables, not an automated or keyword-based inference.
"""

from enum import Enum


class Language(str, Enum):
    """Ge'ez-script languages covered by the survey."""

    AMHARIC = "Amharic"
    TIGRINYA = "Tigrinya"
    CLASSICAL_GEEZ = "Classical Ge'ez"
    OTHER = "Other"


class Pillar(str, Enum):
    """The manuscript's four methodological pillars, plus an infrastructure/resources category."""

    TOKENIZATION = "Tokenization & Normalization"
    MORPHOLOGY = "Lexical & Morphological Analysis"
    EMBEDDINGS = "Text Representation & Embeddings"
    SEQUENCE_LABELING = "Sequence Labeling & Structure Extraction"
    LANGUAGE_MODELS = "Language Models & Deep Learning"
    RESOURCES = "Language Resources & Datasets"
    OTHER = "Other NLP"


class ToolType(str, Enum):
    """Artefact type used in the tool-type distribution figure."""

    DATASET = "Dataset"
    LIBRARY = "Library"
    PIPELINE = "Pipeline"
    ALGORITHM = "Algorithm"
    FRAMEWORK = "Framework"
    CORPUS = "Corpus"
    TOOL = "Tool"
    MODEL = "Model"
    OTHER = "Other"

"""Coding dimension definitions for paper classification.

Defines the 5 dimensions used to systematically code papers in the survey:
1. Languages (Amharic, Tigrinya, Classical Ge'ez, Other)
2. Primary Pillar (Tokenization, Morphology, Embeddings, Sequence Labeling, etc.)
3. Tool Type (Dataset, Library, Pipeline, Algorithm)
4. Morphology Focus (Boolean + Assumption Type)
5. Script-Specific Design (Unicode, Fidel, Abugida, Diacritic handling)
"""

from enum import Enum
from typing import Dict, List, Set


class Language(str, Enum):
    """Target languages for coding."""
    AMHARIC = "Amharic"
    TIGRINYA = "Tigrinya"
    CLASSICAL_GEEZ = "Classical Ge'ez"
    OTHER = "Other"


class Pillar(str, Enum):
    """NLP research pillars."""
    TOKENIZATION = "Tokenization & Normalization"
    MORPHOLOGY = "Lexical & Morphological Analysis"
    EMBEDDINGS = "Text Representation & Embeddings"
    SEQUENCE_LABELING = "Sequence Labeling & Structure Extraction"
    LANGUAGE_MODELS = "Language Models & Deep Learning"
    RESOURCES = "Language Resources & Datasets"
    OTHER = "Other NLP"


class ToolType(str, Enum):
    """Type of tool/contribution."""
    DATASET = "Dataset"
    LIBRARY = "Library"
    PIPELINE = "Pipeline"
    ALGORITHM = "Algorithm"
    FRAMEWORK = "Framework"
    CORPUS = "Corpus"
    TOOL = "Tool"
    MODEL = "Model"
    OTHER = "Other"


class MorphologyAssumption(str, Enum):
    """Type of morphological assumption."""
    AGGLUTINATIVE = "Agglutinative"
    FUSIONAL = "Fusional"
    ABUGIDA = "Abugida Script"
    SCRIPT_AWARE = "Script-Aware"
    LANGUAGE_AGNOSTIC = "Language-Agnostic"
    UNKNOWN = "Unknown"


class ScriptProperty(str, Enum):
    """Script-specific properties addressed."""
    UNICODE_HANDLING = "Unicode Handling"
    FIDEL_SCRIPT = "Fidel Script"
    DIACRITIC_MARKS = "Diacritic Marks"
    ABUGIDA_STRUCTURE = "Abugida Structure"
    NORMALIZATION = "Normalization"
    DECOMPOSITION = "Decomposition"
    COMBINING_CHARACTERS = "Combining Characters"


class TransferApproach(str, Enum):
    """Approach to language transfer/adaptation."""
    MONOLINGUAL = "Monolingual"
    CROSS_LINGUAL = "Cross-lingual"
    CROSS_SCRIPT = "Cross-script"
    MULTILINGUAL = "Multilingual"
    TRANSFER_LEARNING = "Transfer Learning"
    ZERO_SHOT = "Zero-shot"
    FEW_SHOT = "Few-shot"


# Keyword mappings for automated coding
LANGUAGE_KEYWORDS: Dict[Language, Set[str]] = {
    Language.AMHARIC: {"amharic", "amh", "ኃምሓራዊ"},
    Language.TIGRINYA: {"tigrinya", "tig", "ትግርኛ"},
    Language.CLASSICAL_GEEZ: {"ge'ez", "geez", "ethiopic", "fidel", "ግዕዝ", "classical ge'ez"},
    Language.OTHER: {"language", "script", "nlp"},
}

PILLAR_KEYWORDS: Dict[Pillar, Set[str]] = {
    Pillar.TOKENIZATION: {
        "tokeniz", "segmentation", "unicode normalization", "fidel", "word boundary",
        "text boundary", "script normalization", "character level"
    },
    Pillar.MORPHOLOGY: {
        "morpholog", "root", "lemm", "stemm", "pos tag", "part-of-speech",
        "affix", "suffix", "prefix", "inflection", "derivation", "compound"
    },
    Pillar.EMBEDDINGS: {
        "embedding", "word2vec", "fasttext", "bert", "xlm", "glove",
        "representation", "vector", "transformer", "contextual", "dense vector"
    },
    Pillar.SEQUENCE_LABELING: {
        "ner", "named entity", "parsing", "chunking", "pos", "tagging",
        "labeling", "sequence label", "crf", "structure extraction"
    },
    Pillar.LANGUAGE_MODELS: {
        "language model", "lm", "lstm", "rnn", "neural", "deep learning",
        "transformer", "gpt", "bert", "pretraining", "fine-tuning"
    },
    Pillar.RESOURCES: {
        "corpus", "dataset", "benchmark", "annotation", "treebank",
        "lexicon", "dictionary", "resource", "data resource"
    },
}

TOOL_TYPE_KEYWORDS: Dict[ToolType, Set[str]] = {
    ToolType.DATASET: {"corpus", "dataset", "benchmark", "treebank", "collection"},
    ToolType.LIBRARY: {"library", "toolkit", "package", "software library", "api"},
    ToolType.PIPELINE: {"pipeline", "framework", "workflow", "orchestration"},
    ToolType.ALGORITHM: {"algorithm", "method", "approach", "technique", "model"},
    ToolType.FRAMEWORK: {"framework", "architecture", "system", "platform"},
    ToolType.CORPUS: {"corpus", "corpora", "annotated data", "parallel corpus"},
    ToolType.TOOL: {"tool", "utility", "converter", "processor"},
    ToolType.MODEL: {"model", "pretrained", "trained model", "weights"},
}

MORPHOLOGY_KEYWORDS: Set[str] = {
    "morpholog", "morphological", "root", "lemm", "stemm", "pos tag",
    "part-of-speech", "affix", "inflection", "agglutinative", "fusional"
}

SCRIPT_KEYWORDS: Dict[ScriptProperty, Set[str]] = {
    ScriptProperty.UNICODE_HANDLING: {"unicode", "utf-8", "encoding", "nfc", "nfd", "nfkc", "nfkd"},
    ScriptProperty.FIDEL_SCRIPT: {"fidel", "abugida", "syllabary", "syllabic"},
    ScriptProperty.DIACRITIC_MARKS: {"diacritic", "diacritics", "accent", "mark", "combining"},
    ScriptProperty.ABUGIDA_STRUCTURE: {"abugida", "syllabic structure", "inherent vowel"},
    ScriptProperty.NORMALIZATION: {"normaliz", "normalization", "standard form"},
    ScriptProperty.DECOMPOSITION: {"decompos", "decomposition", "canonical"},
    ScriptProperty.COMBINING_CHARACTERS: {"combining", "modifier", "base character"},
}

TRANSFER_KEYWORDS: Dict[TransferApproach, Set[str]] = {
    TransferApproach.MONOLINGUAL: {"monolingual", "single language", "language-specific"},
    TransferApproach.CROSS_LINGUAL: {"cross-lingual", "crosslingual", "multilingual", "language transfer"},
    TransferApproach.CROSS_SCRIPT: {"cross-script", "script transfer", "script adaptation"},
    TransferApproach.MULTILINGUAL: {"multilingual", "multiple language", "language universal"},
    TransferApproach.TRANSFER_LEARNING: {"transfer learning", "domain adaptation", "pretrain"},
    TransferApproach.ZERO_SHOT: {"zero-shot", "zero shot"},
    TransferApproach.FEW_SHOT: {"few-shot", "few shot", "low-resource"},
}

# Keyword indicators for reproducibility
CODE_AVAILABLE_KEYWORDS: Set[str] = {
    "github", "code available", "source code", "public repository",
    "open source", "implementation", "codebase"
}

DATA_AVAILABLE_KEYWORDS: Set[str] = {
    "dataset available", "data available", "download", "repository",
    "supplementary", "appendix", "shared data"
}

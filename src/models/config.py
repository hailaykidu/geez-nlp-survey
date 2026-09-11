"""Configuration data models for the Ge'ez-Script NLP survey."""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class SearchConfig:
    """Configuration for the search phase.

    Attributes:
        keywords: Dictionary mapping language codes to search keywords
        sources: Configuration for each search source (API endpoints, auth, etc.)
        filters: Filtering options (year range, peer-reviewed, etc.)
    """

    keywords: Dict[str, List[str]]
    sources: Dict[str, Dict[str, Any]]
    filters: Dict[str, Any]


@dataclass
class ScreeningConfig:
    """Configuration for the screening phase.

    Attributes:
        inclusion_criteria: Dictionary defining criteria for paper inclusion
        exclusion_criteria: Dictionary defining reasons for paper exclusion
        decision_tree: Step-by-step decision tree for screening decisions
    """

    inclusion_criteria: Dict[str, Any]
    exclusion_criteria: Dict[str, Any]
    decision_tree: Dict[str, str]


@dataclass
class CodingConfig:
    """Configuration for the coding phase.

    Attributes:
        dimensions: Dictionary defining the 5 coding dimensions:
            - languages: Target languages (Amharic, Tigrinya, Ge'ez)
            - pillars: NLP pillars (tokenization, morphology, embeddings, sequence_labeling)
            - tool_types: Type of tool (dataset, model, framework, etc.)
            - morphology: Morphology-specific features
            - script_adaptation: Script-specific design and transfer approaches
    """

    dimensions: Dict[str, Dict[str, Any]]

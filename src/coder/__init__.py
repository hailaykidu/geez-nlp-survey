"""Phase 6: Structured extraction and coding across 5 dimensions.

Exports: PaperCoder, CodingValidator, and dimension enums for coding papers.
"""

from src.coder.coder import PaperCoder
from src.coder.validators import CodingValidator
from src.coder.dimensions import (
    Language,
    Pillar,
    ToolType,
    MorphologyAssumption,
    ScriptProperty,
    TransferApproach,
)

__all__ = [
    "PaperCoder",
    "CodingValidator",
    "Language",
    "Pillar",
    "ToolType",
    "MorphologyAssumption",
    "ScriptProperty",
    "TransferApproach",
]

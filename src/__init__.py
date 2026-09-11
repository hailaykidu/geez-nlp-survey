"""
Ge'ez-Script NLP Tools Survey: Core Package

Systematic PRISMA-style extraction and analysis of foundational NLP tools
for Ge'ez-script languages (Amharic, Tigrinya, Classical Ge'ez).
"""

__version__ = "1.0.0"
__author__ = "Hailay Kidu Teklehaymanot"
__email__ = "teklehaymanot@l3s.uni-hannover.de"

from src.models.paper import Paper, Coding, ScreeningDecision
from src.models.config import SearchConfig, ScreeningConfig, CodingConfig

__all__ = [
    "Paper",
    "Coding",
    "ScreeningDecision",
    "SearchConfig",
    "ScreeningConfig",
    "CodingConfig",
]

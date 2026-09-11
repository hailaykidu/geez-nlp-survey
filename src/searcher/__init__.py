"""Phase 1: Paper search across multiple academic sources."""

from src.searcher.base_searcher import BaseSearcher
from src.searcher.semantic_scholar_searcher import SemanticScholarSearcher
from src.searcher.acl_anthology_searcher import ACLAnthologySearcher

__all__ = [
    "BaseSearcher",
    "SemanticScholarSearcher",
    "ACLAnthologySearcher",
]

"""Abstract base class for paper searchers.

Defines the interface that all search implementations must follow,
including Semantic Scholar, ACL Anthology, and other sources.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.paper import Paper


class BaseSearcher(ABC):
    """Abstract base class for paper search implementations.

    All searcher subclasses must implement the search() and get_source_name()
    methods to handle source-specific search logic and paper extraction.

    Attributes:
        config: Configuration dictionary containing source-specific settings
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize searcher with configuration.

        Args:
            config: Configuration dictionary with source settings, API keys, etc.
        """
        self.config = config

    @abstractmethod
    def search(self, keywords: List[str]) -> List[Paper]:
        """Search for papers using provided keywords.

        Must be implemented by subclasses to handle source-specific search logic.

        Args:
            keywords: List of search keywords/queries

        Returns:
            List of Paper objects found

        Raises:
            Various exceptions depending on implementation (network errors, etc.)
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Get the name of the search source.

        Must return a consistent identifier for the source.

        Returns:
            Source name (e.g., 'semantic_scholar', 'acl_anthology')
        """
        pass

    def validate_paper(self, paper: Paper) -> bool:
        """Validate a paper object has required fields.

        Args:
            paper: Paper object to validate

        Returns:
            True if paper is valid, False otherwise
        """
        required_fields = ['title', 'authors', 'year', 'venue']
        for field in required_fields:
            if not getattr(paper, field, None):
                return False
        return True

    def filter_duplicates(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers from a list.

        Uses paper ID to detect duplicates. Keeps first occurrence.

        Args:
            papers: List of papers to filter

        Returns:
            List of unique papers
        """
        seen_ids = set()
        unique_papers = []

        for paper in papers:
            if paper.id not in seen_ids:
                seen_ids.add(paper.id)
                unique_papers.append(paper)

        return unique_papers

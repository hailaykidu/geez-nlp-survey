"""Semantic Scholar API integration for paper search.

Queries the Semantic Scholar API to find peer-reviewed papers on Ge'ez-script
NLP topics (Amharic, Tigrinya, Classical Ge'ez).
"""

import requests
import time
from typing import List, Dict, Any
from src.models.paper import Paper
from src.searcher.base_searcher import BaseSearcher
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SemanticScholarSearcher(BaseSearcher):
    """Search Semantic Scholar API for papers.

    Implements the BaseSearcher interface to query Semantic Scholar's
    paper search API for Ge'ez-script language NLP papers.

    API Documentation: https://api.semanticscholar.org/

    Attributes:
        config: Configuration dictionary with 'sources' containing
                'semantic_scholar' settings (base_url, rate_limit, timeout)
        rate_limit: Seconds to wait between API calls
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize Semantic Scholar searcher.

        Args:
            config: Configuration dictionary with Semantic Scholar settings
        """
        super().__init__(config)
        self.rate_limit = config.get("sources", {}).get("semantic_scholar", {}).get("rate_limit", 1)

    def get_source_name(self) -> str:
        """Get the source identifier.

        Returns:
            "semantic_scholar"
        """
        return "semantic_scholar"

    def search(self, keywords: List[str]) -> List[Paper]:
        """Search Semantic Scholar for papers.

        Queries the Semantic Scholar API with each keyword and extracts
        paper metadata from the results.

        Args:
            keywords: List of search keywords

        Returns:
            List of Paper objects found in Semantic Scholar

        Note:
            Respects rate limiting between API calls to avoid throttling.
        """
        papers = []
        base_url = (
            self.config.get("sources", {})
            .get("semantic_scholar", {})
            .get("base_url", "https://api.semanticscholar.org/graph/v1/paper/search")
        )

        logger.info(f"Starting Semantic Scholar search with {len(keywords)} keywords")

        for i, keyword in enumerate(keywords, 1):
            try:
                logger.debug(f"Searching keyword {i}/{len(keywords)}: {keyword}")

                # Set up API request
                params = {
                    "query": keyword,
                    "limit": 100,
                    "fields": "paperId,title,authors,year,venue,abstract,url,externalIds",
                }
                headers = {"User-Agent": "Geez-NLP-Survey (teklehaymanot@l3s.uni-hannover.de)"}

                # Make API request
                response = requests.get(
                    base_url,
                    params=params,
                    headers=headers,
                    timeout=10,
                )
                response.raise_for_status()

                # Parse response
                data = response.json()
                results = data.get("data", [])

                logger.debug(f"Found {len(results)} papers for keyword: {keyword}")

                # Extract papers
                for item in results:
                    try:
                        paper = self._parse_paper(item)
                        if self.validate_paper(paper):
                            papers.append(paper)
                    except (KeyError, ValueError) as e:
                        logger.debug(f"Skipped invalid paper entry: {e}")
                        continue

                # Rate limiting - respect API limits
                if i < len(keywords):
                    time.sleep(self.rate_limit)

            except requests.exceptions.RequestException as e:
                logger.warning(f"Network error searching Semantic Scholar for '{keyword}': {e}")
            except Exception as e:
                logger.error(f"Unexpected error searching Semantic Scholar for '{keyword}': {e}")

        logger.info(f"Semantic Scholar search complete: found {len(papers)} papers")

        # Remove duplicates
        unique_papers = self.filter_duplicates(papers)
        logger.info(f"After deduplication: {len(unique_papers)} unique papers")

        return unique_papers

    def _parse_paper(self, item: Dict[str, Any]) -> Paper:
        """Parse a paper from Semantic Scholar API response.

        Args:
            item: Paper item from API response

        Returns:
            Paper object

        Raises:
            KeyError: If required fields are missing
            ValueError: If data is invalid
        """
        paper_id = item.get("paperId", "")
        if not paper_id:
            raise ValueError("Missing paperId in API response")

        # Extract authors
        authors = []
        for author in item.get("authors", []):
            author_name = author.get("name", "").strip()
            if author_name:
                authors.append(author_name)

        # Extract DOI from externalIds
        external_ids = item.get("externalIds", {}) or {}
        doi = external_ids.get("DOI", "")

        # Create Paper object
        paper = Paper(
            id=f"ss_{paper_id}",
            title=item.get("title", "").strip(),
            authors=authors,
            year=item.get("year", 0),
            venue=item.get("venue", "Unknown").strip(),
            doi=doi,
            url=item.get("url", ""),
            abstract=item.get("abstract", "").strip(),
            source=self.get_source_name(),
        )

        return paper

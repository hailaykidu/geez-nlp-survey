"""ACL Anthology web scraper for paper discovery.

Scrapes the ACL Anthology repository (https://aclweb.org/anthology/) to find
peer-reviewed NLP papers on Ge'ez-script languages.
"""

import requests
import time
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from src.models.paper import Paper
from src.searcher.base_searcher import BaseSearcher
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ACLAnthologySearcher(BaseSearcher):
    """Search ACL Anthology for papers via web scraping.

    Implements the BaseSearcher interface to search the ACL Anthology repository
    (aclweb.org/anthology) for peer-reviewed NLP conference papers.

    Website: https://aclweb.org/anthology/

    Attributes:
        config: Configuration dictionary with rate limiting and timeout
        rate_limit: Seconds to wait between HTTP requests
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize ACL Anthology searcher.

        Args:
            config: Configuration dictionary with ACL settings
        """
        super().__init__(config)
        self.rate_limit = config.get("sources", {}).get("acl_anthology", {}).get("rate_limit", 1)
        self.session = requests.Session()

    def get_source_name(self) -> str:
        """Get the source identifier.

        Returns:
            "acl_anthology"
        """
        return "acl_anthology"

    def search(self, keywords: List[str]) -> List[Paper]:
        """Search ACL Anthology for papers.

        Performs web search on ACL Anthology using the built-in search functionality.

        Args:
            keywords: List of search keywords

        Returns:
            List of Paper objects found in ACL Anthology

        Note:
            Respects rate limiting to avoid overwhelming the ACL servers.
        """
        papers = []
        base_url = "https://aclweb.org/anthology/"

        logger.info(f"Starting ACL Anthology search with {len(keywords)} keywords")

        for i, keyword in enumerate(keywords, 1):
            try:
                logger.debug(f"Searching keyword {i}/{len(keywords)}: {keyword}")

                # ACL Anthology search URL
                search_url = f"{base_url}search"
                params = {"q": keyword}

                headers = {"User-Agent": "Geez-NLP-Survey (teklehaymanot@l3s.uni-hannover.de)"}

                # Fetch search results page
                response = self.session.get(search_url, params=params, headers=headers, timeout=10)
                response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.content, "html.parser")

                # Find paper entries (ACL Anthology uses specific HTML structure)
                # Papers are typically in div with class 'paper'
                paper_elements = soup.find_all("div", class_="paper")

                logger.debug(f"Found {len(paper_elements)} paper entries for: {keyword}")

                # Extract papers from each element
                for element in paper_elements:
                    try:
                        paper = self._parse_paper_element(element, base_url)
                        if paper and self.validate_paper(paper):
                            papers.append(paper)
                    except (AttributeError, ValueError) as e:
                        logger.debug(f"Skipped invalid paper entry: {e}")
                        continue

                # Rate limiting
                if i < len(keywords):
                    time.sleep(self.rate_limit)

            except requests.exceptions.RequestException as e:
                logger.warning(f"Network error searching ACL for '{keyword}': {e}")
            except Exception as e:
                logger.error(f"Unexpected error searching ACL for '{keyword}': {e}")

        logger.info(f"ACL Anthology search complete: found {len(papers)} papers")

        # Remove duplicates
        unique_papers = self.filter_duplicates(papers)
        logger.info(f"After deduplication: {len(unique_papers)} unique papers")

        return unique_papers

    def _parse_paper_element(self, element: BeautifulSoup, base_url: str) -> Optional[Paper]:
        """Parse a paper from an HTML element.

        Extracts title, authors, venue, URL from ACL Anthology HTML structure.

        Args:
            element: BeautifulSoup element containing paper info
            base_url: Base URL for constructing full paper URLs

        Returns:
            Paper object or None if parsing fails

        Raises:
            AttributeError: If expected HTML structure is missing
            ValueError: If data is invalid
        """
        # Extract title
        title_elem = element.find("span", class_="title")
        if not title_elem:
            raise ValueError("Title element not found")
        title = title_elem.get_text(strip=True)

        if not title:
            raise ValueError("Title is empty")

        # Extract paper link (href)
        link_elem = element.find("a", href=True)
        if not link_elem:
            raise ValueError("Paper link not found")

        paper_id = link_elem.get("href", "").strip("/")
        if not paper_id:
            raise ValueError("Paper ID is empty")

        # Construct full URL
        paper_url = f"{base_url.rstrip('/')}/{paper_id}"

        # Extract authors
        authors = []
        author_elem = element.find("span", class_="authors")
        if author_elem:
            author_text = author_elem.get_text(strip=True)
            # Split authors by common separators
            author_names = [a.strip() for a in author_text.split(",")]
            authors = [a for a in author_names if a]

        # Extract venue/conference
        venue_elem = element.find("span", class_="venue")
        venue = venue_elem.get_text(strip=True) if venue_elem else "ACL"

        # Extract year if available
        year = 0
        year_elem = element.find("span", class_="year")
        if year_elem:
            try:
                year = int(year_elem.get_text(strip=True))
            except ValueError:
                year = 0

        # Create Paper object
        paper = Paper(
            id=f"acl_{paper_id.replace('/', '_')}",
            title=title,
            authors=authors,
            year=year,
            venue=venue,
            url=paper_url,
            source=self.get_source_name(),
        )

        return paper

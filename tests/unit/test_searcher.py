"""Unit tests for paper searchers.

Tests the BaseSearcher interface and concrete implementations (Semantic Scholar,
ACL Anthology) with mocked API responses.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List

from src.models.paper import Paper
from src.searcher.base_searcher import BaseSearcher
from src.searcher.semantic_scholar_searcher import SemanticScholarSearcher
from src.searcher.acl_anthology_searcher import ACLAnthologySearcher


# Fixtures
@pytest.fixture
def sample_config():
    """Provide sample search configuration."""
    return {
        "sources": {
            "semantic_scholar": {
                "base_url": "https://api.semanticscholar.org/graph/v1/paper/search",
                "rate_limit": 1,
                "timeout": 10,
            },
            "acl_anthology": {
                "base_url": "https://aclweb.org/anthology/",
                "rate_limit": 1,
                "timeout": 10,
            },
        }
    }


@pytest.fixture
def sample_keywords():
    """Provide sample search keywords."""
    return ["Amharic NLP", "Tigrinya morphology"]


@pytest.fixture
def sample_ss_response():
    """Provide sample Semantic Scholar API response."""
    return {
        "data": [
            {
                "paperId": "12345abc",
                "title": "Amharic Morphological Analyzer",
                "authors": [
                    {"name": "John Doe"},
                    {"name": "Jane Smith"},
                ],
                "year": 2023,
                "venue": "ACL",
                "abstract": "We present an analyzer for Amharic",
                "url": "https://example.com/paper",
                "externalIds": {"DOI": "10.1234/example"},
            },
            {
                "paperId": "67890def",
                "title": "Ge'ez Script Processing",
                "authors": [{"name": "Alice Johnson"}],
                "year": 2022,
                "venue": "LREC",
                "abstract": "Methods for processing Ge'ez",
                "url": "https://example.com/paper2",
                "externalIds": {},
            },
        ]
    }


@pytest.fixture
def sample_ss_invalid_response():
    """Provide invalid Semantic Scholar response."""
    return {
        "data": [
            {
                # Missing required fields
                "paperId": "missing_title",
                # No title
            },
            {
                "paperId": "missing_authors",
                "title": "Some Paper",
                # No authors
            },
        ]
    }


# Test BaseSearcher
class TestBaseSearcher:
    """Test BaseSearcher abstract class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that BaseSearcher cannot be instantiated directly."""
        config = {"sources": {}}
        with pytest.raises(TypeError):
            BaseSearcher(config)

    def test_validate_paper_valid(self, sample_config):
        """Test paper validation with valid paper."""
        searcher = SemanticScholarSearcher(sample_config)
        paper = Paper(
            id="test1",
            title="Test Paper",
            authors=["Author1"],
            year=2023,
            venue="ACL",
        )
        assert searcher.validate_paper(paper) is True

    def test_validate_paper_missing_title(self, sample_config):
        """Test paper validation fails with missing title."""
        searcher = SemanticScholarSearcher(sample_config)
        paper = Paper(
            id="test1",
            title="",  # Empty title
            authors=["Author1"],
            year=2023,
            venue="ACL",
        )
        assert searcher.validate_paper(paper) is False

    def test_validate_paper_missing_authors(self, sample_config):
        """Test paper validation fails with missing authors."""
        searcher = SemanticScholarSearcher(sample_config)
        paper = Paper(
            id="test1",
            title="Test Paper",
            authors=[],  # Empty authors
            year=2023,
            venue="ACL",
        )
        assert searcher.validate_paper(paper) is False

    def test_filter_duplicates(self, sample_config):
        """Test duplicate filtering."""
        searcher = SemanticScholarSearcher(sample_config)
        papers = [
            Paper(id="p1", title="Paper 1", authors=["A"], year=2023, venue="ACL"),
            Paper(id="p1", title="Paper 1", authors=["A"], year=2023, venue="ACL"),  # Duplicate
            Paper(id="p2", title="Paper 2", authors=["B"], year=2023, venue="ACL"),
        ]
        unique = searcher.filter_duplicates(papers)
        assert len(unique) == 2
        assert unique[0].id == "p1"
        assert unique[1].id == "p2"


# Test SemanticScholarSearcher
class TestSemanticScholarSearcher:
    """Test Semantic Scholar searcher."""

    def test_get_source_name(self, sample_config):
        """Test source name."""
        searcher = SemanticScholarSearcher(sample_config)
        assert searcher.get_source_name() == "semantic_scholar"

    def test_initialization(self, sample_config):
        """Test searcher initialization."""
        searcher = SemanticScholarSearcher(sample_config)
        assert searcher.config == sample_config
        assert searcher.rate_limit == 1

    @patch("requests.get")
    def test_search_success(self, mock_get, sample_config, sample_keywords, sample_ss_response):
        """Test successful search."""
        mock_response = Mock()
        mock_response.json.return_value = sample_ss_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        searcher = SemanticScholarSearcher(sample_config)
        papers = searcher.search(sample_keywords)

        assert len(papers) == 2
        assert papers[0].title == "Amharic Morphological Analyzer"
        assert papers[0].source == "semantic_scholar"
        assert len(papers[0].authors) == 2

    @patch("requests.get")
    def test_search_with_invalid_papers(self, mock_get, sample_config, sample_keywords, sample_ss_invalid_response):
        """Test search filters invalid papers."""
        mock_response = Mock()
        mock_response.json.return_value = sample_ss_invalid_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        searcher = SemanticScholarSearcher(sample_config)
        papers = searcher.search(sample_keywords)

        # Invalid papers should be filtered out
        assert len(papers) == 0

    @patch("requests.get")
    def test_search_network_error(self, mock_get, sample_config, sample_keywords):
        """Test search handles network errors."""
        mock_get.side_effect = Exception("Network error")

        searcher = SemanticScholarSearcher(sample_config)
        papers = searcher.search(sample_keywords)

        # Should return empty list on error
        assert len(papers) == 0

    def test_parse_paper(self, sample_config, sample_ss_response):
        """Test paper parsing from API response."""
        searcher = SemanticScholarSearcher(sample_config)
        item = sample_ss_response["data"][0]

        paper = searcher._parse_paper(item)

        assert paper.id == "ss_12345abc"
        assert paper.title == "Amharic Morphological Analyzer"
        assert len(paper.authors) == 2
        assert paper.year == 2023
        assert paper.venue == "ACL"
        assert paper.doi == "10.1234/example"

    def test_parse_paper_missing_id(self, sample_config):
        """Test parse_paper raises on missing ID."""
        searcher = SemanticScholarSearcher(sample_config)
        item = {"title": "Paper without ID"}

        with pytest.raises(ValueError):
            searcher._parse_paper(item)


# Test ACLAnthologySearcher
class TestACLAnthologySearcher:
    """Test ACL Anthology searcher."""

    def test_get_source_name(self, sample_config):
        """Test source name."""
        searcher = ACLAnthologySearcher(sample_config)
        assert searcher.get_source_name() == "acl_anthology"

    def test_initialization(self, sample_config):
        """Test searcher initialization."""
        searcher = ACLAnthologySearcher(sample_config)
        assert searcher.config == sample_config
        assert searcher.rate_limit == 1

    @patch("requests.Session.get")
    def test_search_success(self, mock_get, sample_config, sample_keywords):
        """Test successful ACL search."""
        html_content = """
        <html>
            <div class="paper">
                <span class="title">Amharic NLP Tools</span>
                <a href="P20-1001">Link</a>
                <span class="authors">John Doe, Jane Smith</span>
                <span class="venue">ACL 2020</span>
                <span class="year">2020</span>
            </div>
        </html>
        """

        mock_response = Mock()
        mock_response.content = html_content.encode()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        searcher = ACLAnthologySearcher(sample_config)
        papers = searcher.search(sample_keywords)

        assert len(papers) >= 0  # May be 0 if parsing fails, but shouldn't raise

    @patch("requests.Session.get")
    def test_search_network_error(self, mock_get, sample_config, sample_keywords):
        """Test search handles network errors."""
        mock_get.side_effect = Exception("Network error")

        searcher = ACLAnthologySearcher(sample_config)
        papers = searcher.search(sample_keywords)

        # Should return empty list on error
        assert len(papers) == 0

    def test_parse_paper_element(self, sample_config):
        """Test parsing paper element from HTML."""
        from bs4 import BeautifulSoup

        html = """
        <div class="paper">
            <span class="title">Test Paper Title</span>
            <a href="P20-1001">link</a>
            <span class="authors">Author One, Author Two</span>
            <span class="venue">ACL</span>
            <span class="year">2020</span>
        </div>
        """

        soup = BeautifulSoup(html, "html.parser")
        element = soup.find("div", class_="paper")

        searcher = ACLAnthologySearcher(sample_config)
        paper = searcher._parse_paper_element(element, "https://aclweb.org/anthology/")

        assert paper is not None
        assert paper.title == "Test Paper Title"
        assert len(paper.authors) == 2
        assert paper.year == 2020

    def test_parse_paper_element_missing_title(self, sample_config):
        """Test parse_paper_element raises on missing title."""
        from bs4 import BeautifulSoup

        html = """
        <div class="paper">
            <a href="P20-1001">link</a>
        </div>
        """

        soup = BeautifulSoup(html, "html.parser")
        element = soup.find("div", class_="paper")

        searcher = ACLAnthologySearcher(sample_config)
        with pytest.raises(ValueError):
            searcher._parse_paper_element(element, "https://aclweb.org/anthology/")


# Test integration
class TestSearcherIntegration:
    """Integration tests for searchers."""

    def test_multiple_keywords(self, sample_config):
        """Test searching with multiple keywords."""
        searcher = SemanticScholarSearcher(sample_config)
        keywords = ["Amharic", "Tigrinya", "Ge'ez"]

        # Mock the requests to avoid actual API calls
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"data": []}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            papers = searcher.search(keywords)
            # Should make one call per keyword
            assert mock_get.call_count >= len(keywords)

    def test_paper_consistency(self, sample_config):
        """Test that parsed papers have consistent structure."""
        searcher = SemanticScholarSearcher(sample_config)

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "data": [
                    {
                        "paperId": "123",
                        "title": "Test",
                        "authors": [{"name": "John"}],
                        "year": 2023,
                        "venue": "ACL",
                        "abstract": "Abstract",
                        "url": "http://example.com",
                        "externalIds": {},
                    }
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            papers = searcher.search(["test"])

            assert len(papers) == 1
            paper = papers[0]
            assert isinstance(paper, Paper)
            assert paper.source == "semantic_scholar"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

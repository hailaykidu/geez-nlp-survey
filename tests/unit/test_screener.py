"""Unit tests for PRISMA screening logic.

Tests the PRISMAScreener class with inclusion/exclusion criteria,
decision logic, and result persistence.
"""

import pytest
import json
import tempfile
from pathlib import Path

from src.models.paper import Paper
from src.screener.prisma_screener import PRISMAScreener, ScreeningResult


@pytest.fixture
def sample_papers():
    """Provide sample papers for testing."""
    return [
        # Should be included
        Paper(
            id="p1",
            title="Amharic Morphological Analyzer using Deep Learning",
            authors=["John Doe", "Jane Smith"],
            year=2023,
            venue="ACL",
            abstract="We present a deep learning approach to morphological analysis for Amharic",
            source="semantic_scholar",
        ),
        # Should be excluded - no target language
        Paper(
            id="p2",
            title="English NLP Techniques",
            authors=["Bob Author"],
            year=2022,
            venue="EMNLP",
            abstract="A survey of NLP tools for English",
            source="semantic_scholar",
        ),
        # Should be excluded - year out of range
        Paper(
            id="p3",
            title="Tigrinya Tokenizer",
            authors=["Alice Dev"],
            year=2010,
            venue="LREC",
            abstract="A tokenizer for Tigrinya language",
            source="acl_anthology",
        ),
        # Should be excluded - no NLP focus
        Paper(
            id="p4",
            title="History of Ge'ez Script",
            authors=["Historical Author"],
            year=2020,
            venue="Journal",
            abstract="A historical analysis of the Ge'ez writing system",
            source="semantic_scholar",
        ),
        # Should be included - Tigrinya with embeddings
        Paper(
            id="p5",
            title="Word Embeddings for Tigrinya",
            authors=["ML Researcher"],
            year=2021,
            venue="ACL",
            abstract="We develop word embeddings for the Tigrinya language using word2vec",
            source="semantic_scholar",
        ),
    ]


@pytest.fixture
def sample_config():
    """Provide sample screening configuration."""
    return {
        "metadata": {
            "version": "1.0",
            "description": "PRISMA inclusion/exclusion criteria",
        },
        "inclusion_criteria": {
            "peer_reviewed": {"enabled": True},
            "target_language_mentioned": {
                "enabled": True,
                "keywords": [
                    "Amharic",
                    "Tigrinya",
                    "Classical Ge'ez",
                    "Ge'ez",
                    "Geez",
                    "Ethiopic",
                    "Fidel",
                    "Ethiopian",
                    "Abugida",
                ],
            },
            "foundational_tool_contribution": {
                "enabled": True,
                "pillars": ["tokenization", "morphology", "embeddings", "sequence_labeling"],
            },
            "tool_development_central": {"enabled": True},
        },
        "exclusion_criteria": {
            "non_peer_reviewed": {
                "enabled": True,
                "codes": ["technical_report", "blog", "thesis", "preprint_only"],
            },
            "no_target_language": {
                "enabled": True,
                "code": "no_geez_script_language",
            },
            "no_nlp_focus": {
                "enabled": True,
                "codes": ["linguistics_only", "historical", "computational_linguistics_no_tools"],
            },
            "no_tool_contribution": {
                "enabled": True,
                "code": "no_foundational_tool",
            },
            "downstream_only": {
                "enabled": True,
                "code": "downstream_application_only",
            },
        },
        "decision_tree": {
            "step_1": "Is paper peer-reviewed?",
            "step_2": "Does paper mention target language?",
            "step_3": "Does paper describe NLP tool?",
            "step_4": "Is tool development central?",
        },
        "filters": {"year_min": 2016, "year_max": 2026},
    }


class TestPRISMAScreenerInit:
    """Test PRISMAScreener initialization."""

    def test_initialization(self):
        """Test screener initializes correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()

            # Create minimal config
            screening_config = {
                "filters": {"year_min": 2016, "year_max": 2026},
                "inclusion_criteria": {
                    "target_language_mentioned": {"keywords": ["Amharic"]}
                },
            }
            (config_dir / "screening_criteria.json").write_text(json.dumps(screening_config))

            screener = PRISMAScreener(config_dir=str(config_dir))
            assert screener.config is not None
            assert screener.included == []
            assert screener.excluded == []

    def test_missing_config_raises_error(self):
        """Test error when config file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                PRISMAScreener(config_dir=tmpdir)


class TestYearRangeCheck:
    """Test year range validation."""

    @pytest.fixture
    def screener(self, sample_config):
        """Create screener with sample config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            yield PRISMAScreener(config_dir=str(config_dir))

    def test_paper_in_valid_year_range(self, screener):
        """Test paper within year range passes."""
        paper = Paper(
            id="test",
            title="Test",
            authors=["Author"],
            year=2020,
            venue="ACL",
        )
        assert screener._check_year_range(paper) is True

    def test_paper_below_min_year(self, screener):
        """Test paper below minimum year fails."""
        paper = Paper(
            id="test",
            title="Test",
            authors=["Author"],
            year=2010,
            venue="ACL",
        )
        assert screener._check_year_range(paper) is False

    def test_paper_above_max_year(self, screener):
        """Test paper above maximum year fails."""
        paper = Paper(
            id="test",
            title="Test",
            authors=["Author"],
            year=2030,
            venue="ACL",
        )
        assert screener._check_year_range(paper) is False


class TestTargetLanguageCheck:
    """Test target language detection."""

    @pytest.fixture
    def screener(self, sample_config):
        """Create screener with sample config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            yield PRISMAScreener(config_dir=str(config_dir))

    def test_amharic_detected(self, screener):
        """Test Amharic language detection."""
        paper = Paper(
            id="test",
            title="Amharic NLP",
            authors=["Author"],
            year=2020,
            venue="ACL",
            abstract="Tools for Amharic processing",
        )
        assert screener._check_target_language(paper) is True

    def test_tigrinya_detected(self, screener):
        """Test Tigrinya language detection."""
        paper = Paper(
            id="test",
            title="Tigrinya Tokenizer",
            authors=["Author"],
            year=2020,
            venue="ACL",
            abstract="A tokenizer for Tigrinya",
        )
        assert screener._check_target_language(paper) is True

    def test_no_target_language(self, screener):
        """Test no target language fails."""
        paper = Paper(
            id="test",
            title="English NLP",
            authors=["Author"],
            year=2020,
            venue="ACL",
            abstract="English language processing tools",
        )
        assert screener._check_target_language(paper) is False

    def test_case_insensitive_matching(self, screener):
        """Test case-insensitive language matching."""
        paper = Paper(
            id="test",
            title="amharic NLP",  # lowercase
            authors=["Author"],
            year=2020,
            venue="ACL",
            abstract="Tools",
        )
        assert screener._check_target_language(paper) is True


class TestNLPFocusCheck:
    """Test NLP focus detection."""

    @pytest.fixture
    def screener(self, sample_config):
        """Create screener with sample config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            yield PRISMAScreener(config_dir=str(config_dir))

    def test_morphology_detected(self, screener):
        """Test morphology keyword detection."""
        paper = Paper(
            id="test",
            title="Morphological Analyzer",
            authors=["Author"],
            year=2020,
            venue="ACL",
        )
        assert screener._check_nlp_focus(paper) is True

    def test_tokenization_detected(self, screener):
        """Test tokenization keyword detection."""
        paper = Paper(
            id="test",
            title="Tokenizer for Amharic",
            authors=["Author"],
            year=2020,
            venue="ACL",
        )
        assert screener._check_nlp_focus(paper) is True

    def test_no_nlp_focus(self, screener):
        """Test non-NLP paper fails."""
        paper = Paper(
            id="test",
            title="History of Language",
            authors=["Author"],
            year=2020,
            venue="Journal",
            abstract="A historical study",
        )
        assert screener._check_nlp_focus(paper) is False


class TestToolCentralityCheck:
    """Test tool development centrality."""

    @pytest.fixture
    def screener(self, sample_config):
        """Create screener with sample config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            yield PRISMAScreener(config_dir=str(config_dir))

    def test_tool_development_central(self, screener):
        """Test tool development is considered central."""
        paper = Paper(
            id="test",
            title="We propose a morphological analyzer",
            authors=["Author"],
            year=2020,
            venue="ACL",
        )
        assert screener._check_tool_centrality(paper) is True

    def test_downstream_application_only(self, screener):
        """Test downstream application only is excluded."""
        paper = Paper(
            id="test",
            title="Machine translation using BERT",
            authors=["Author"],
            year=2020,
            venue="ACL",
            abstract="We apply machine translation to Amharic",
        )
        assert screener._check_tool_centrality(paper) is False


class TestScreeningWorkflow:
    """Test complete screening workflow."""

    def test_full_screening_workflow(self, sample_papers, sample_config):
        """Test complete screening with multiple papers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            output_dir = Path(tmpdir) / "screened"

            screener = PRISMAScreener(
                config_dir=str(config_dir),
                output_dir=str(output_dir),
            )

            included, excluded = screener.screen(sample_papers)

            # Should have some included papers
            assert len(included) > 0
            # Should have some excluded papers
            assert len(excluded) > 0
            # Total should match
            assert len(included) + len(excluded) == len(sample_papers)

    def test_screening_output_files_created(self, sample_papers, sample_config):
        """Test that output files are created correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            output_dir = Path(tmpdir) / "screened"

            screener = PRISMAScreener(
                config_dir=str(config_dir),
                output_dir=str(output_dir),
            )

            screener.screen(sample_papers)

            # Check output files exist
            included_file = output_dir / "included" / "papers.json"
            excluded_file = output_dir / "excluded" / "papers.json"
            summary_file = output_dir / "screening_summary.json"

            assert included_file.exists()
            assert excluded_file.exists()
            assert summary_file.exists()

            # Verify JSON is valid
            with open(included_file) as f:
                included_data = json.load(f)
                assert isinstance(included_data, list)

            with open(summary_file) as f:
                summary = json.load(f)
                assert "total_papers" in summary
                assert "included" in summary
                assert "excluded" in summary

    def test_get_summary(self, sample_papers, sample_config):
        """Test screening summary generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            screener = PRISMAScreener(config_dir=str(config_dir))
            screener.screen(sample_papers)

            summary = screener.get_summary()

            assert "total_papers_screened" in summary
            assert "papers_included" in summary
            assert "papers_excluded" in summary
            assert "inclusion_rate" in summary
            assert summary["total_papers_screened"] == len(sample_papers)


class TestScreeningResults:
    """Test screening result objects."""

    def test_screening_result_creation(self):
        """Test ScreeningResult creation."""
        result = ScreeningResult(
            paper_id="p1",
            title="Test Paper",
            included=True,
            reason="Meets all criteria",
            criteria_results={
                "year_range": True,
                "target_language": True,
                "nlp_focus": True,
                "tool_centrality": True,
            },
        )

        assert result.paper_id == "p1"
        assert result.included is True
        assert len(result.criteria_results) == 4


class TestPaperStateChanges:
    """Test that papers' state is updated during screening."""

    def test_paper_screened_flag_set(self, sample_papers, sample_config):
        """Test that screened flag is set on papers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            screener = PRISMAScreener(config_dir=str(config_dir))
            screener.screen(sample_papers)

            for paper in sample_papers:
                assert paper.screened is True

    def test_paper_included_flag_set(self, sample_papers, sample_config):
        """Test that included flag is set correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            (config_dir / "screening_criteria.json").write_text(json.dumps(sample_config))

            screener = PRISMAScreener(config_dir=str(config_dir))
            screener.screen(sample_papers)

            for paper in screener.included:
                assert paper.included is True

            for paper in screener.excluded:
                assert paper.included is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

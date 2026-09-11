"""Unit tests for paper coder and coding validators."""

import pytest
import tempfile
from pathlib import Path

from src.models.paper import Paper
from src.coder.coder import PaperCoder
from src.coder.validators import CodingValidator
from src.coder.dimensions import (
    Language, Pillar, ToolType, MorphologyAssumption, TransferApproach
)


@pytest.fixture
def sample_papers():
    """Provide sample papers for testing."""
    return [
        Paper(
            id="p1",
            title="Amharic Morphological Analyzer using Deep Learning",
            authors=["Author One"],
            year=2023,
            venue="ACL",
            abstract="We present a deep learning approach to morphological analysis for Amharic language",
            source="semantic_scholar",
        ),
        Paper(
            id="p2",
            title="Tigrinya Embeddings and Transfer Learning",
            authors=["Author Two"],
            year=2022,
            venue="EMNLP",
            abstract="Word embeddings for Tigrinya using cross-lingual transfer learning",
            source="acl_anthology",
        ),
        Paper(
            id="p3",
            title="Ge'ez Unicode Normalization Dataset",
            authors=["Author Three"],
            year=2021,
            venue="LREC",
            abstract="A corpus for Ge'ez script with unicode handling and normalization",
            source="semantic_scholar",
        ),
        Paper(
            id="p4",
            title="Named Entity Recognition for Ethiopian Languages",
            authors=["Author Four"],
            year=2023,
            venue="ACL",
            abstract="NER pipeline for Amharic and Tigrinya with GitHub code available",
            source="semantic_scholar",
        ),
    ]


class TestPaperCoder:
    """Test PaperCoder functionality."""

    def test_initialization(self):
        """Test coder initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)
            assert coder.coded_papers == []
            assert coder.output_dir.exists()

    def test_code_languages(self, sample_papers):
        """Test language coding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            # Amharic paper
            coder._code_languages(sample_papers[0], sample_papers[0].title.lower())
            assert Language.AMHARIC.value in sample_papers[0].languages

            # Tigrinya paper
            coder._code_languages(sample_papers[1], sample_papers[1].title.lower())
            assert Language.TIGRINYA.value in sample_papers[1].languages

            # Ge'ez paper
            coder._code_languages(sample_papers[2], sample_papers[2].title.lower())
            assert Language.CLASSICAL_GEEZ.value in sample_papers[2].languages

    def test_code_primary_pillar(self, sample_papers):
        """Test primary pillar coding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            # Morphology focus
            text1 = sample_papers[0].title.lower()
            coder._code_primary_pillar(sample_papers[0], text1)
            assert sample_papers[0].primary_pillar == Pillar.MORPHOLOGY.value

            # Embeddings focus
            text2 = sample_papers[1].title.lower()
            coder._code_primary_pillar(sample_papers[1], text2)
            assert sample_papers[1].primary_pillar == Pillar.EMBEDDINGS.value

            # Sequence labeling (NER)
            text4 = sample_papers[3].title.lower()
            coder._code_primary_pillar(sample_papers[3], text4)
            assert sample_papers[3].primary_pillar == Pillar.SEQUENCE_LABELING.value

    def test_code_tool_type(self, sample_papers):
        """Test tool type coding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            # Dataset
            text3 = sample_papers[2].title.lower()
            coder._code_tool_type(sample_papers[2], text3)
            assert sample_papers[2].tool_type == ToolType.DATASET.value

            # Pipeline/Framework
            text4 = sample_papers[3].title.lower()
            coder._code_tool_type(sample_papers[3], text4)
            assert sample_papers[3].tool_type is not None

    def test_code_morphology(self, sample_papers):
        """Test morphology coding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            text1 = sample_papers[0].title.lower() + " " + sample_papers[0].abstract.lower()
            coder._code_morphology(sample_papers[0], text1)
            assert sample_papers[0].morphology_focus is True
            assert sample_papers[0].morphological_assumption is not None

    def test_code_script_design(self, sample_papers):
        """Test script design coding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            text3 = sample_papers[2].title.lower() + " " + sample_papers[2].abstract.lower()
            coder._code_script_design(sample_papers[2], text3)
            assert sample_papers[2].script_specific_design is True

    def test_code_reproducibility(self, sample_papers):
        """Test code and data availability coding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            text4 = sample_papers[3].title.lower() + " github"
            coder._code_reproducibility(sample_papers[3], text4)
            assert sample_papers[3].code_available is True

    def test_full_coding_workflow(self, sample_papers):
        """Test complete coding workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)

            coded = coder.code(sample_papers)

            assert len(coded) == len(sample_papers)
            assert all(p.languages for p in coded)
            assert all(p.primary_pillar for p in coded)


class TestCodingValidator:
    """Test CodingValidator functionality."""

    def test_validate_complete_paper(self, sample_papers):
        """Test validation of complete paper."""
        coder = PaperCoder()
        coder._code_paper(sample_papers[0])

        is_valid, errors = CodingValidator.validate_paper(sample_papers[0])
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_incomplete_paper(self):
        """Test validation of incomplete paper."""
        paper = Paper(
            id="test",
            title="Test",
            authors=["Author"],
            year=2023,
            venue="ACL",
        )

        is_valid, errors = CodingValidator.validate_paper(paper)
        assert is_valid is False
        assert len(errors) > 0

    def test_batch_validation(self, sample_papers):
        """Test batch validation."""
        coder = PaperCoder()
        coded = coder.code(sample_papers)

        validation = CodingValidator.validate_batch(coded)
        assert validation["total"] == len(coded)
        assert validation["valid"] > 0

    def test_coding_completeness(self, sample_papers):
        """Test completeness calculation."""
        coder = PaperCoder()
        coder._code_paper(sample_papers[0])

        completeness = CodingValidator.get_coding_completeness(sample_papers[0])
        assert 0.0 <= completeness <= 1.0
        assert completeness > 0.5  # Well-coded paper should be fairly complete

    def test_batch_completeness(self, sample_papers):
        """Test batch completeness statistics."""
        coder = PaperCoder()
        coded = coder.code(sample_papers)

        stats = CodingValidator.get_batch_completeness(coded)
        assert stats["total"] == len(coded)
        assert 0.0 <= stats["avg_completeness"] <= 1.0
        assert stats["fully_coded"] + stats["partially_coded"] + stats["incomplete"] == len(coded)


class TestCodingSummary:
    """Test coding summary generation."""

    def test_coding_summary_generation(self, sample_papers):
        """Test that coding summary is generated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)
            coder.code(sample_papers)

            summary = coder.get_coding_summary()

            assert summary["total_coded"] == len(sample_papers)
            assert len(summary["languages"]) > 0
            assert len(summary["pillars"]) > 0
            assert len(summary["tool_types"]) > 0

    def test_output_files_created(self, sample_papers):
        """Test that output files are created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            coder = PaperCoder(output_dir=tmpdir)
            coder.code(sample_papers)

            output_path = Path(tmpdir)
            papers_file = output_path / "papers" / "papers.json"
            summary_file = output_path / "coding_summary.json"

            assert papers_file.exists()
            assert summary_file.exists()


class TestDimensionEnums:
    """Test dimension enum definitions."""

    def test_language_enum(self):
        """Test Language enum."""
        assert Language.AMHARIC.value == "Amharic"
        assert Language.TIGRINYA.value == "Tigrinya"
        assert Language.CLASSICAL_GEEZ.value == "Classical Ge'ez"
        assert Language.OTHER.value == "Other"

    def test_pillar_enum(self):
        """Test Pillar enum."""
        assert Pillar.TOKENIZATION.value == "Tokenization & Normalization"
        assert Pillar.MORPHOLOGY.value == "Lexical & Morphological Analysis"
        assert Pillar.EMBEDDINGS.value == "Text Representation & Embeddings"

    def test_tool_type_enum(self):
        """Test ToolType enum."""
        assert ToolType.DATASET.value == "Dataset"
        assert ToolType.LIBRARY.value == "Library"
        assert ToolType.PIPELINE.value == "Pipeline"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

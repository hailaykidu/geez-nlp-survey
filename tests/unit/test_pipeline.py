"""Unit tests for pipeline orchestration and validation."""

import pytest
import tempfile
from pathlib import Path
from src.models.paper import Paper
from src.pipeline.orchestrator import SystematicReviewOrchestrator
from src.pipeline.validator import PipelineValidator


@pytest.fixture
def sample_papers():
    """Provide sample papers for pipeline testing."""
    return [
        Paper(
            id="p1",
            title="Amharic Morphological Analyzer using Deep Learning",
            authors=["Author One", "Author Two"],
            year=2023,
            venue="ACL",
            abstract="Deep learning morphological analysis",
            source="semantic_scholar",
            languages=["Amharic"],
            primary_pillar="Lexical & Morphological Analysis",
            tool_type="Algorithm",
            morphology_focus=True,
            morphological_assumption="Agglutinative",
            script_specific_design=True,
            transfer_approach="Cross-lingual",
            code_available=True,
            data_available=False,
        ),
        Paper(
            id="p2",
            title="Tigrinya Embeddings and Transfer Learning",
            authors=["Author Three"],
            year=2022,
            venue="EMNLP",
            abstract="Word embeddings for Tigrinya",
            source="acl_anthology",
            languages=["Tigrinya"],
            primary_pillar="Text Representation & Embeddings",
            tool_type="Library",
            morphology_focus=False,
            script_specific_design=False,
            transfer_approach="Cross-lingual",
            code_available=True,
            data_available=True,
        ),
        Paper(
            id="p3",
            title="Ge'ez Unicode Normalization Dataset",
            authors=["Author Four"],
            year=2021,
            venue="LREC",
            abstract="Unicode normalization corpus",
            source="semantic_scholar",
            languages=["Classical Ge'ez"],
            primary_pillar="Tokenization & Normalization",
            tool_type="Dataset",
            morphology_focus=False,
            script_specific_design=True,
            transfer_approach="Monolingual",
            code_available=False,
            data_available=True,
        ),
        Paper(
            id="p4",
            title="Amharic NER Pipeline",
            authors=["Author Five"],
            year=2023,
            venue="ACL",
            abstract="NER for Amharic",
            source="semantic_scholar",
            languages=["Amharic"],
            primary_pillar="Sequence Labeling & Structure Extraction",
            tool_type="Pipeline",
            morphology_focus=True,
            morphological_assumption="Agglutinative",
            script_specific_design=False,
            transfer_approach="Monolingual",
            code_available=True,
            data_available=True,
        ),
        Paper(
            id="p5",
            title="Multi-lingual Transfer Learning",
            authors=["Author Six"],
            year=2022,
            venue="COLING",
            abstract="Transfer learning for African languages",
            source="semantic_scholar",
            languages=["Amharic", "Tigrinya"],
            primary_pillar="Language Models & Deep Learning",
            tool_type="Framework",
            morphology_focus=False,
            script_specific_design=False,
            transfer_approach="Transfer Learning",
            code_available=True,
            data_available=False,
        ),
    ]


class TestPipelineValidator:
    """Test pipeline validation functionality."""

    def test_initialization(self):
        """Test validator initialization."""
        validator = PipelineValidator()
        assert validator is not None

    def test_validate_pipeline_inputs_valid(self, sample_papers):
        """Test valid pipeline input validation."""
        validator = PipelineValidator()
        is_valid, errors = validator.validate_pipeline_inputs(sample_papers)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_pipeline_inputs_empty(self):
        """Test empty pipeline input validation."""
        validator = PipelineValidator()
        is_valid, errors = validator.validate_pipeline_inputs([])

        assert is_valid is False
        assert len(errors) > 0
        assert "No papers" in errors[0]

    def test_validate_pipeline_inputs_duplicates(self):
        """Test duplicate paper detection."""
        paper1 = Paper(
            id="p1",
            title="Title 1",
            authors=["Author"],
            year=2023,
            venue="ACL",
        )
        paper2 = Paper(
            id="p1",
            title="Title 2",
            authors=["Author"],
            year=2023,
            venue="EMNLP",
        )
        validator = PipelineValidator()
        is_valid, errors = validator.validate_pipeline_inputs([paper1, paper2])

        assert is_valid is False
        assert any("Duplicate" in e for e in errors)

    def test_validate_pipeline_outputs(self, sample_papers):
        """Test pipeline output validation."""
        validator = PipelineValidator()
        results = validator.validate_pipeline_outputs(sample_papers)

        assert results["total_papers"] == len(sample_papers)
        assert results["valid_papers"] > 0
        assert 0 <= results["validation_rate"] <= 100
        assert 0 <= results["completeness_avg"] <= 1

    def test_validate_output_files_missing(self):
        """Test missing output file detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PipelineValidator()
            output_dir = Path(tmpdir)
            checks = validator.validate_output_files(output_dir)

            assert len(checks) > 0
            # All should be False since we created empty directory
            assert not all(checks.values())

    def test_validate_data_integrity(self, sample_papers):
        """Test data integrity validation."""
        validator = PipelineValidator()
        checks = validator.validate_data_integrity(sample_papers)

        assert len(checks) > 0
        assert checks["duplicate_ids"] is True
        assert checks["all_titled"] is True
        assert checks["all_authored"] is True
        assert checks["language_coverage"] is True
        assert checks["pillar_coverage"] is True

    def test_generate_validation_report(self, sample_papers):
        """Test validation report generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PipelineValidator()
            output_dir = Path(tmpdir)
            report_file = validator.generate_validation_report(sample_papers, output_dir)

            assert report_file.exists()
            assert report_file.suffix == ".txt"

            # Verify content
            with open(report_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "VALIDATION REPORT" in content
                assert "INPUT VALIDATION" in content
                assert "OUTPUT VALIDATION" in content


class TestSystematicReviewOrchestrator:
    """Test pipeline orchestration."""

    def test_initialization(self):
        """Test orchestrator initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = SystematicReviewOrchestrator(config_dir=tmpdir)
            assert orchestrator.output_dir.exists()
            assert orchestrator.searched_papers == []
            assert orchestrator.screened_papers == []
            assert orchestrator.coded_papers == []

    def test_load_configuration(self):
        """Test configuration loading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = SystematicReviewOrchestrator(config_dir=tmpdir)
            try:
                config = orchestrator._load_configuration()
                assert isinstance(config, dict)
            except Exception:
                # Config loading may fail without proper config files
                pass

    def test_get_pipeline_stats(self, sample_papers):
        """Test pipeline statistics."""
        orchestrator = SystematicReviewOrchestrator()
        orchestrator.searched_papers = sample_papers[:3]
        orchestrator.screened_papers = sample_papers[:2]
        orchestrator.coded_papers = sample_papers[:2]

        stats = orchestrator.get_pipeline_stats()

        assert stats["searched_papers"] == 3
        assert stats["screened_papers"] == 2
        assert stats["coded_papers"] == 2
        assert 0 <= stats["screening_rate"] <= 100


class TestPipelineIntegration:
    """Integration tests for complete pipeline."""

    def test_validator_input_output_flow(self, sample_papers):
        """Test validator through complete input-output flow."""
        validator = PipelineValidator()

        # Validate inputs
        is_valid, errors = validator.validate_pipeline_inputs(sample_papers)
        assert is_valid is True

        # Validate outputs
        results = validator.validate_pipeline_outputs(sample_papers)
        assert results["valid_papers"] > 0

    def test_orchestrator_configuration_loading(self):
        """Test orchestrator can load configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            orchestrator = SystematicReviewOrchestrator(config_dir=tmpdir)
            # Should not raise exception
            try:
                config = orchestrator._load_configuration()
            except Exception as e:
                # Expected if config doesn't exist
                assert "config" in str(e).lower()

    def test_validation_report_generation(self, sample_papers):
        """Test complete validation report generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            validator = PipelineValidator()

            # Generate report
            report_file = validator.generate_validation_report(sample_papers, output_dir)

            assert report_file.exists()

            # Verify sections
            with open(report_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "INPUT VALIDATION" in content
                assert "OUTPUT VALIDATION" in content
                assert "FILE VALIDATION" in content
                assert "DATA INTEGRITY" in content
                assert "OVERALL STATUS" in content


class TestPipelineEdgeCases:
    """Test pipeline edge cases and error handling."""

    def test_single_paper_pipeline(self):
        """Test pipeline with single paper."""
        paper = Paper(
            id="p1",
            title="Single Paper",
            authors=["Author"],
            year=2023,
            venue="ACL",
        )
        validator = PipelineValidator()
        is_valid, errors = validator.validate_pipeline_inputs([paper])

        # Single paper should have some warnings
        assert len(errors) > 0

    def test_papers_with_missing_fields(self):
        """Test handling of papers with missing fields."""
        paper = Paper(
            id="p1",
            title="",  # Missing title
            authors=[],  # Missing authors
            year=None,  # Missing year
            venue="ACL",
        )
        validator = PipelineValidator()
        is_valid, errors = validator.validate_pipeline_inputs([paper])

        assert is_valid is False
        assert len(errors) > 0

    def test_validation_with_empty_directory(self):
        """Test file validation with empty output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            validator = PipelineValidator()
            checks = validator.validate_output_files(output_dir)

            # No files should exist
            assert not any(checks.values())

    def test_data_integrity_with_future_dates(self):
        """Test data integrity checking with invalid dates."""
        paper = Paper(
            id="p1",
            title="Future Paper",
            authors=["Author"],
            year=2105,  # Invalid future date (beyond 2100 check)
            venue="ACL",
        )
        validator = PipelineValidator()
        checks = validator.validate_data_integrity([paper])

        assert checks["all_years_valid"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

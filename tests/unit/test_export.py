"""Unit tests for data export and report generation."""

import pytest
import tempfile
import json
from pathlib import Path
from src.models.paper import Paper
from src.export.csv_exporter import CSVExporter
from src.export.json_exporter import JSONExporter
from src.export.report_generator import ReportGenerator


@pytest.fixture
def sample_papers():
    """Provide sample papers for testing."""
    return [
        Paper(
            id="p1",
            title="Amharic Morphological Analyzer using Deep Learning",
            authors=["Author One", "Author Two"],
            year=2023,
            venue="ACL",
            abstract="We present a deep learning approach to morphological analysis",
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
            abstract="Word embeddings for Tigrinya language",
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
            authors=["Author Four", "Author Five"],
            year=2021,
            venue="LREC",
            abstract="A corpus for Ge'ez script normalization",
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
    ]


class TestCSVExporter:
    """Test CSV export functionality."""

    def test_initialization(self):
        """Test CSV exporter initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = CSVExporter(output_dir=tmpdir)
            assert exporter.output_dir.exists()

    def test_export_basic(self, sample_papers):
        """Test basic CSV export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = CSVExporter(output_dir=tmpdir)
            output_file = exporter.export(sample_papers)

            assert output_file.exists()
            assert output_file.suffix == ".csv"

            # Verify content
            with open(output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Header + 3 papers
                assert len(lines) == 4

    def test_export_column_mapping(self, sample_papers):
        """Test correct column mapping."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = CSVExporter(output_dir=tmpdir)
            output_file = exporter.export(sample_papers)

            with open(output_file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                columns = first_line.split(",")

                assert "id" in columns
                assert "title" in columns
                assert "authors" in columns
                assert "languages" in columns
                assert "primary_pillar" in columns

    def test_paper_to_dict(self, sample_papers):
        """Test paper to dictionary conversion."""
        paper = sample_papers[0]
        result = CSVExporter._paper_to_dict(paper)

        assert result["id"] == "p1"
        assert result["title"] == "Amharic Morphological Analyzer using Deep Learning"
        assert result["year"] == 2023
        assert "Author One" in result["authors"]
        assert result["morphology_focus"] == "Yes"

    def test_export_by_dimension(self, sample_papers):
        """Test dimension-based export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = CSVExporter(output_dir=tmpdir)
            outputs = exporter.export_by_dimension(sample_papers)

            # Should have files for languages, pillars, tool types
            assert len(outputs) > 0
            for path in outputs.values():
                assert path.exists()

    def test_group_by_language(self, sample_papers):
        """Test language grouping."""
        groups = CSVExporter._group_by_language(sample_papers)

        assert "Amharic" in groups
        assert "Tigrinya" in groups
        assert "Classical Ge'ez" in groups
        assert len(groups["Amharic"]) == 1
        assert len(groups["Tigrinya"]) == 1

    def test_group_by_pillar(self, sample_papers):
        """Test pillar grouping."""
        groups = CSVExporter._group_by_pillar(sample_papers)

        assert "Lexical & Morphological Analysis" in groups
        assert "Text Representation & Embeddings" in groups
        assert "Tokenization & Normalization" in groups

    def test_custom_filename(self, sample_papers):
        """Test custom filename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = CSVExporter(output_dir=tmpdir)
            output_file = exporter.export(sample_papers, filename="custom.csv")

            assert output_file.name == "custom.csv"
            assert output_file.exists()


class TestJSONExporter:
    """Test JSON export functionality."""

    def test_initialization(self):
        """Test JSON exporter initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = JSONExporter(output_dir=tmpdir)
            assert exporter.output_dir.exists()

    def test_export_basic(self, sample_papers):
        """Test basic JSON export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = JSONExporter(output_dir=tmpdir)
            output_file = exporter.export(sample_papers)

            assert output_file.exists()
            assert output_file.suffix == ".json"

            # Verify valid JSON
            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert len(data) == 3
                assert all("id" in p for p in data)
                assert all("title" in p for p in data)

    def test_export_with_metadata(self, sample_papers):
        """Test JSON export with metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = JSONExporter(output_dir=tmpdir)
            metadata = {
                "total_papers": len(sample_papers),
                "export_date": "2023-01-01",
                "version": "1.0",
            }
            output_file = exporter.export_with_metadata(
                sample_papers, metadata, "export_with_meta.json"
            )

            assert output_file.exists()

            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert "metadata" in data
                assert "papers" in data
                assert data["metadata"]["total_papers"] == 3

    def test_export_schema(self):
        """Test schema export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = JSONExporter(output_dir=tmpdir)
            output_file = exporter.export_schema()

            assert output_file.exists()

            with open(output_file, "r", encoding="utf-8") as f:
                schema = json.load(f)
                assert "fields" in schema
                assert "dimensions" in schema
                assert "languages" in schema["dimensions"]


class TestReportGenerator:
    """Test report generation functionality."""

    def test_initialization(self):
        """Test report generator initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            assert generator.output_dir.exists()

    def test_generate_statistics_report(self, sample_papers):
        """Test statistics report generation."""
        generator = ReportGenerator()
        report = generator.generate_statistics_report(sample_papers)

        assert "summary" in report
        assert "language_statistics" in report
        assert "pillar_statistics" in report
        assert "tool_type_statistics" in report
        assert "morphology_statistics" in report
        assert "reproducibility_statistics" in report

    def test_summary_statistics(self, sample_papers):
        """Test summary statistics."""
        generator = ReportGenerator()
        summary = generator._generate_summary(sample_papers)

        assert summary["total_papers"] == 3
        assert summary["venues"] > 0
        assert summary["unique_authors"] > 0

    def test_language_statistics(self, sample_papers):
        """Test language statistics."""
        generator = ReportGenerator()
        stats = generator._analyze_languages(sample_papers)

        assert stats["total_language_mentions"] >= 3
        assert "Amharic" in stats["distribution"]
        assert stats["amharic_papers"] == 1
        assert stats["tigrinya_papers"] == 1
        assert stats["geez_papers"] == 1

    def test_pillar_statistics(self, sample_papers):
        """Test pillar statistics."""
        generator = ReportGenerator()
        stats = generator._analyze_pillars(sample_papers)

        assert stats["total_papers_with_pillar"] == 3
        assert stats["unique_pillars"] == 3

    def test_tool_type_statistics(self, sample_papers):
        """Test tool type statistics."""
        generator = ReportGenerator()
        stats = generator._analyze_tool_types(sample_papers)

        assert stats["total_papers_with_tool_type"] == 3
        assert "Algorithm" in stats["distribution"]
        assert "Dataset" in stats["distribution"]

    def test_morphology_statistics(self, sample_papers):
        """Test morphology statistics."""
        generator = ReportGenerator()
        stats = generator._analyze_morphology(sample_papers)

        assert stats["morphology_focused_papers"] == 1
        assert 0 <= stats["morphology_percentage"] <= 100

    def test_script_design_statistics(self, sample_papers):
        """Test script design statistics."""
        generator = ReportGenerator()
        stats = generator._analyze_script_design(sample_papers)

        assert stats["script_aware_papers"] >= 1
        assert 0 <= stats["script_awareness_percentage"] <= 100

    def test_reproducibility_statistics(self, sample_papers):
        """Test reproducibility statistics."""
        generator = ReportGenerator()
        stats = generator._analyze_reproducibility(sample_papers)

        assert stats["papers_with_code"] >= 1
        assert stats["papers_with_data"] >= 1
        assert 0 <= stats["code_availability_percentage"] <= 100

    def test_temporal_statistics(self, sample_papers):
        """Test temporal distribution."""
        generator = ReportGenerator()
        stats = generator._analyze_temporal(sample_papers)

        assert "papers_by_year" in stats
        assert len(stats["papers_by_year"]) > 0
        assert stats["latest_year"] >= stats["earliest_year"]

    def test_save_report(self, sample_papers):
        """Test report saving."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ReportGenerator(output_dir=tmpdir)
            report = generator.generate_statistics_report(sample_papers)
            output_file = generator.save_report(report)

            assert output_file.exists()
            assert output_file.suffix == ".txt"

            # Verify content
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "SYSTEMATIC REVIEW STATISTICS REPORT" in content
                assert "SUMMARY" in content
                assert "LANGUAGE_STATISTICS" in content


class TestExportIntegration:
    """Integration tests for export functionality."""

    def test_full_export_pipeline(self, sample_papers):
        """Test complete export pipeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # CSV export
            csv_exporter = CSVExporter(output_dir=tmpdir)
            csv_file = csv_exporter.export(sample_papers)

            # JSON export
            json_exporter = JSONExporter(output_dir=tmpdir)
            json_file = json_exporter.export(sample_papers)
            json_schema = json_exporter.export_schema()

            # Report generation
            report_gen = ReportGenerator(output_dir=tmpdir)
            report = report_gen.generate_statistics_report(sample_papers)
            report_file = report_gen.save_report(report)

            # Verify all files exist
            assert csv_file.exists()
            assert json_file.exists()
            assert json_schema.exists()
            assert report_file.exists()

    def test_export_formats_consistency(self, sample_papers):
        """Test consistency between CSV and JSON exports."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_exporter = CSVExporter(output_dir=tmpdir)
            json_exporter = JSONExporter(output_dir=tmpdir)

            csv_file = csv_exporter.export(sample_papers)
            json_file = json_exporter.export(sample_papers)

            # CSV should have same number of papers (excluding header)
            with open(csv_file, "r", encoding="utf-8") as f:
                csv_lines = f.readlines()
                csv_count = len(csv_lines) - 1  # Exclude header

            # JSON should have same number of papers
            with open(json_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                json_count = len(json_data)

            assert csv_count == json_count == len(sample_papers)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

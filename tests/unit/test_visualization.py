"""Unit tests for visualization and synthesis report generation."""

import pytest
import tempfile
from pathlib import Path
from src.models.paper import Paper
from src.visualization.chart_generator import ChartGenerator
from src.visualization.synthesis_report import SynthesisReportGenerator


@pytest.fixture
def sample_papers():
    """Provide sample papers for visualization testing."""
    return [
        Paper(
            id="p1",
            title="Amharic Morphological Analyzer",
            authors=["Author One"],
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
            title="Tigrinya Embeddings",
            authors=["Author Two"],
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
            title="Ge'ez Unicode Dataset",
            authors=["Author Three"],
            year=2021,
            venue="LREC",
            abstract="Ge'ez normalization corpus",
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
            authors=["Author Four"],
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
            authors=["Author Five"],
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


class TestChartGenerator:
    """Test chart generation functionality."""

    def test_initialization(self):
        """Test chart generator initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            assert generator.output_dir.exists()
            assert generator.dpi == 300

    def test_chart_language_distribution(self, sample_papers):
        """Test language distribution chart generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_language_distribution(sample_papers)

            assert chart_file.exists()
            assert chart_file.suffix == ".png"
            assert chart_file.stat().st_size > 0

    def test_chart_pillar_distribution(self, sample_papers):
        """Test pillar distribution chart generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_pillar_distribution(sample_papers)

            assert chart_file.exists()
            assert chart_file.suffix == ".png"
            assert chart_file.stat().st_size > 0

    def test_chart_tool_type_distribution(self, sample_papers):
        """Test tool type distribution chart generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_tool_type_distribution(sample_papers)

            assert chart_file.exists()
            assert chart_file.suffix == ".png"
            assert chart_file.stat().st_size > 0

    def test_chart_temporal_distribution(self, sample_papers):
        """Test temporal distribution chart generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_temporal_distribution(sample_papers)

            assert chart_file.exists()
            assert chart_file.suffix == ".png"
            assert chart_file.stat().st_size > 0

    def test_chart_morphology_focus(self, sample_papers):
        """Test morphology focus chart generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_morphology_focus(sample_papers)

            assert chart_file.exists()
            assert chart_file.suffix == ".png"
            assert chart_file.stat().st_size > 0

    def test_chart_reproducibility(self, sample_papers):
        """Test reproducibility chart generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_reproducibility(sample_papers)

            assert chart_file.exists()
            assert chart_file.suffix == ".png"
            assert chart_file.stat().st_size > 0

    def test_generate_all_charts(self, sample_papers):
        """Test complete chart generation pipeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            charts = generator.generate_all_charts(sample_papers)

            # Should generate 6 charts
            assert len(charts) == 6
            assert "languages" in charts
            assert "pillars" in charts
            assert "tool_types" in charts
            assert "temporal" in charts
            assert "morphology" in charts
            assert "reproducibility" in charts

            # All should be valid file paths
            for chart_file in charts.values():
                assert chart_file.exists()
                assert chart_file.suffix == ".png"

    def test_chart_output_quality(self, sample_papers):
        """Test that charts are publication quality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            chart_file = generator.chart_language_distribution(sample_papers)

            # File should be reasonably sized for publication
            file_size = chart_file.stat().st_size
            assert file_size > 10000  # At least 10KB
            assert file_size < 1000000  # Less than 1MB


class TestSynthesisReportGenerator:
    """Test synthesis report generation."""

    def test_initialization(self):
        """Test synthesis report generator initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = SynthesisReportGenerator(output_dir=tmpdir)
            assert generator.output_dir.exists()

    def test_generate_synthesis_report(self, sample_papers):
        """Test complete synthesis report generation."""
        generator = SynthesisReportGenerator()
        report = generator.generate_synthesis_report(sample_papers)

        # Should have all major sections
        assert "title" in report
        assert "abstract" in report
        assert "introduction" in report
        assert "key_findings" in report
        assert "research_landscape" in report
        assert "language_specific_findings" in report
        assert "research_pillars" in report
        assert "tool_ecosystem" in report
        assert "morphology_analysis" in report
        assert "script_design_analysis" in report
        assert "reproducibility_assessment" in report
        assert "gaps_and_limitations" in report
        assert "recommendations" in report
        assert "conclusion" in report

    def test_abstract_generation(self, sample_papers):
        """Test abstract generation."""
        generator = SynthesisReportGenerator()
        abstract = generator._generate_abstract(sample_papers)

        assert "systematic review" in abstract.lower()
        assert str(len(sample_papers)) in abstract
        assert "Ge'ez" in abstract or "Geez" in abstract

    def test_introduction_generation(self):
        """Test introduction generation."""
        generator = SynthesisReportGenerator()
        intro = generator._generate_introduction()

        assert "INTRODUCTION" in intro
        assert "Ge'ez" in intro or "Geez" in intro
        assert "morphological" in intro.lower()
        assert "PRISMA" in intro

    def test_key_findings_generation(self, sample_papers):
        """Test key findings generation."""
        generator = SynthesisReportGenerator()
        findings = generator._generate_key_findings(sample_papers)

        assert "KEY FINDINGS" in findings
        assert "Morphological" in findings
        assert "Script-Specific" in findings

    def test_language_findings_generation(self, sample_papers):
        """Test language-specific findings."""
        generator = SynthesisReportGenerator()
        findings = generator._generate_language_findings(sample_papers)

        assert "Amharic" in findings
        assert "Tigrinya" in findings
        assert "Classical Ge'ez" in findings or "Geez" in findings

    def test_recommendations_generation(self):
        """Test recommendations generation."""
        generator = SynthesisReportGenerator()
        recs = generator._generate_recommendations([])

        assert "RECOMMENDATIONS" in recs
        assert "Priority" in recs or "priority" in recs
        assert "Framework" in recs or "framework" in recs

    def test_conclusion_generation(self, sample_papers):
        """Test conclusion generation."""
        generator = SynthesisReportGenerator()
        conclusion = generator._generate_conclusion(sample_papers)

        assert "CONCLUSION" in conclusion
        assert str(len(sample_papers)) in conclusion
        assert "future" in conclusion.lower()

    def test_save_synthesis_report(self, sample_papers):
        """Test synthesis report saving."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = SynthesisReportGenerator(output_dir=tmpdir)
            report = generator.generate_synthesis_report(sample_papers)
            output_file = generator.save_synthesis_report(report)

            assert output_file.exists()
            assert output_file.suffix == ".md"

            # Verify content
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Ge'ez-Script NLP Tools" in content or "Geez" in content
                assert "systematic review" in content.lower()
                assert "INTRODUCTION" in content
                assert "CONCLUSION" in content

    def test_report_markdown_formatting(self, sample_papers):
        """Test that report uses proper markdown formatting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = SynthesisReportGenerator(output_dir=tmpdir)
            report = generator.generate_synthesis_report(sample_papers)
            output_file = generator.save_synthesis_report(report)

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Should have markdown headings
                assert "# " in content or "## " in content
                # Should have bullet points
                assert "- " in content

    def test_report_content_consistency(self, sample_papers):
        """Test that report sections are consistent."""
        generator = SynthesisReportGenerator()
        report = generator.generate_synthesis_report(sample_papers)

        # Key sections should reference paper count
        paper_count = len(sample_papers)
        for section_name in ["key_findings", "language_specific_findings",
                             "research_landscape", "conclusion"]:
            section = report[section_name]
            # At least one section should mention paper count
            if str(paper_count) in section:
                break
        else:
            # At least report should contain paper reference
            full_report = " ".join(str(v) for v in report.values())
            assert str(paper_count) in full_report


class TestVisualizationIntegration:
    """Integration tests for visualization pipeline."""

    def test_full_visualization_pipeline(self, sample_papers):
        """Test complete visualization pipeline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Generate charts
            chart_gen = ChartGenerator(output_dir=tmpdir)
            charts = chart_gen.generate_all_charts(sample_papers)

            # Generate synthesis report
            report_gen = SynthesisReportGenerator(output_dir=tmpdir)
            report = report_gen.generate_synthesis_report(sample_papers)
            report_file = report_gen.save_synthesis_report(report)

            # Verify all outputs
            assert len(charts) == 6
            for chart_file in charts.values():
                assert chart_file.exists()

            assert report_file.exists()
            assert report_file.suffix == ".md"

    def test_multiple_chart_formats(self, sample_papers):
        """Test that charts are generated in expected formats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = ChartGenerator(output_dir=tmpdir)
            charts = generator.generate_all_charts(sample_papers)

            expected_charts = [
                "languages",
                "pillars",
                "tool_types",
                "temporal",
                "morphology",
                "reproducibility",
            ]

            for chart_name in expected_charts:
                assert chart_name in charts
                chart_path = charts[chart_name]
                assert chart_path.suffix == ".png"
                assert "chart_" in chart_path.name

    def test_report_sections_non_empty(self, sample_papers):
        """Test that all report sections have content."""
        generator = SynthesisReportGenerator()
        report = generator.generate_synthesis_report(sample_papers)

        for section_name, section_content in report.items():
            if section_name != "title":
                assert isinstance(section_content, str)
                assert len(section_content) > 50  # Non-trivial content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

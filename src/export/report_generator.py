"""Report generation for systematic review results.

Generates statistical summaries and analysis reports from coded papers.
"""

from pathlib import Path
from typing import List, Dict, Any
from collections import Counter
from src.models.paper import Paper
from src.utils.logger import setup_logger


logger = setup_logger(__name__)


class ReportGenerator:
    """Generate reports from systematic review data."""

    def __init__(self, output_dir: str = "data/exported"):
        """Initialize report generator.

        Args:
            output_dir: Path to output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Report Generator initialized (output: {self.output_dir})")

    def generate_statistics_report(self, papers: List[Paper]) -> Dict[str, Any]:
        """Generate comprehensive statistics report.

        Args:
            papers: List of papers to analyze

        Returns:
            Dictionary with statistics
        """
        logger.info(f"Generating statistics report for {len(papers)} papers...")

        report = {
            "summary": self._generate_summary(papers),
            "language_statistics": self._analyze_languages(papers),
            "pillar_statistics": self._analyze_pillars(papers),
            "tool_type_statistics": self._analyze_tool_types(papers),
            "morphology_statistics": self._analyze_morphology(papers),
            "script_design_statistics": self._analyze_script_design(papers),
            "reproducibility_statistics": self._analyze_reproducibility(papers),
            "temporal_statistics": self._analyze_temporal(papers),
        }

        logger.info("Statistics report generation complete")
        return report

    @staticmethod
    def _generate_summary(papers: List[Paper]) -> Dict[str, Any]:
        """Generate summary statistics."""
        return {
            "total_papers": len(papers),
            "year_range": (
                f"{min(p.year for p in papers if p.year)}-{max(p.year for p in papers if p.year)}"
                if papers
                else "N/A"
            ),
            "venues": len(set(p.venue for p in papers if p.venue)),
            "unique_authors": len(
                set(author for p in papers for author in p.authors)
            ),
        }

    @staticmethod
    def _analyze_languages(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze language distribution."""
        all_languages = []
        for paper in papers:
            all_languages.extend(paper.languages)

        language_counts = Counter(all_languages)

        return {
            "total_language_mentions": len(all_languages),
            "unique_languages": len(language_counts),
            "distribution": dict(language_counts.most_common()),
            "amharic_papers": sum(
                1 for p in papers if "Amharic" in p.languages
            ),
            "tigrinya_papers": sum(
                1 for p in papers if "Tigrinya" in p.languages
            ),
            "geez_papers": sum(
                1 for p in papers if "Classical Ge'ez" in p.languages
            ),
        }

    @staticmethod
    def _analyze_pillars(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze research pillar distribution."""
        pillar_counts = Counter(
            p.primary_pillar for p in papers if p.primary_pillar
        )

        return {
            "total_papers_with_pillar": sum(pillar_counts.values()),
            "unique_pillars": len(pillar_counts),
            "distribution": dict(pillar_counts.most_common()),
        }

    @staticmethod
    def _analyze_tool_types(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze tool type distribution."""
        tool_counts = Counter(p.tool_type for p in papers if p.tool_type)

        return {
            "total_papers_with_tool_type": sum(tool_counts.values()),
            "unique_tool_types": len(tool_counts),
            "distribution": dict(tool_counts.most_common()),
        }

    @staticmethod
    def _analyze_morphology(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze morphology focus."""
        morphology_papers = sum(1 for p in papers if p.morphology_focus)
        assumption_counts = Counter(
            p.morphological_assumption
            for p in papers
            if p.morphological_assumption
        )

        return {
            "morphology_focused_papers": morphology_papers,
            "morphology_percentage": (
                morphology_papers / len(papers) * 100 if papers else 0
            ),
            "morphological_assumptions": dict(assumption_counts.most_common()),
        }

    @staticmethod
    def _analyze_script_design(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze script-specific design."""
        script_papers = sum(1 for p in papers if p.script_specific_design)
        transfer_counts = Counter(
            p.transfer_approach for p in papers if p.transfer_approach
        )

        return {
            "script_aware_papers": script_papers,
            "script_awareness_percentage": (
                script_papers / len(papers) * 100 if papers else 0
            ),
            "transfer_approaches": dict(transfer_counts.most_common()),
        }

    @staticmethod
    def _analyze_reproducibility(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze code and data availability."""
        code_available = sum(1 for p in papers if p.code_available)
        data_available = sum(1 for p in papers if p.data_available)

        return {
            "papers_with_code": code_available,
            "code_availability_percentage": (
                code_available / len(papers) * 100 if papers else 0
            ),
            "papers_with_data": data_available,
            "data_availability_percentage": (
                data_available / len(papers) * 100 if papers else 0
            ),
            "fully_reproducible": sum(
                1 for p in papers if p.code_available and p.data_available
            ),
        }

    @staticmethod
    def _analyze_temporal(papers: List[Paper]) -> Dict[str, Any]:
        """Analyze temporal distribution."""
        year_counts = Counter(p.year for p in papers if p.year)

        return {
            "papers_by_year": dict(sorted(year_counts.most_common(), reverse=True)),
            "year_range": (
                f"{min(year_counts.keys())}-{max(year_counts.keys())}"
                if year_counts
                else "N/A"
            ),
            "latest_year": max(year_counts.keys()) if year_counts else None,
            "earliest_year": min(year_counts.keys()) if year_counts else None,
        }

    def save_report(
        self, report: Dict[str, Any], filename: str = "statistics_report.txt"
    ) -> Path:
        """Save report to text file.

        Args:
            report: Report dictionary
            filename: Output filename

        Returns:
            Path to output file
        """
        output_file = self.output_dir / filename
        logger.info(f"Saving report to {output_file}...")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("SYSTEMATIC REVIEW STATISTICS REPORT\n")
            f.write("=" * 50 + "\n\n")

            for section, data in report.items():
                f.write(f"\n{section.upper()}\n")
                f.write("-" * 40 + "\n")
                self._write_section(f, data)

        logger.info(f"Report saved to {output_file}")
        return output_file

    @staticmethod
    def _write_section(f, data: Any, indent: int = 0) -> None:
        """Recursively write report section."""
        prefix = "  " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    f.write(f"{prefix}{key}:\n")
                    ReportGenerator._write_section(f, value, indent + 1)
                else:
                    f.write(f"{prefix}{key}: {value}\n")
        else:
            f.write(f"{prefix}{data}\n")

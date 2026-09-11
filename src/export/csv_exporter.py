"""CSV export functionality for coded papers.

Exports papers to CSV format with flattened structure for analysis
in spreadsheet applications (Excel, Google Sheets, etc.).
"""

import csv
from pathlib import Path
from typing import List, Dict, Any
from src.models.paper import Paper
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CSVExporter:
    """Export papers to CSV format."""

    # Column mapping for paper fields
    COLUMNS = [
        "id",
        "title",
        "authors",
        "year",
        "venue",
        "abstract",
        "languages",
        "primary_pillar",
        "tool_type",
        "morphology_focus",
        "morphological_assumption",
        "script_specific_design",
        "transfer_approach",
        "code_available",
        "data_available",
        "source",
        "screening_decision",
    ]

    def __init__(self, output_dir: str = "data/exported"):
        """Initialize CSV exporter.

        Args:
            output_dir: Path to output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"CSV Exporter initialized (output: {self.output_dir})")

    def export(self, papers: List[Paper], filename: str = "papers.csv") -> Path:
        """Export papers to CSV.

        Args:
            papers: List of papers to export
            filename: Output filename

        Returns:
            Path to output CSV file
        """
        output_file = self.output_dir / filename
        logger.info(f"Exporting {len(papers)} papers to CSV...")

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.COLUMNS)
            writer.writeheader()

            for i, paper in enumerate(papers, 1):
                row = self._paper_to_dict(paper)
                writer.writerow(row)

                if i % 10 == 0:
                    logger.debug(f"Exported {i}/{len(papers)} papers")

        logger.info(f"CSV export complete: {output_file}")
        return output_file

    @staticmethod
    def _paper_to_dict(paper: Paper) -> Dict[str, Any]:
        """Convert paper to dictionary for CSV export.

        Args:
            paper: Paper to convert

        Returns:
            Dictionary with all paper fields flattened
        """
        return {
            "id": paper.id,
            "title": paper.title,
            "authors": "; ".join(paper.authors),
            "year": paper.year,
            "venue": paper.venue,
            "abstract": paper.abstract or "",
            "languages": "; ".join(paper.languages) if paper.languages else "",
            "primary_pillar": paper.primary_pillar or "",
            "tool_type": paper.tool_type or "",
            "morphology_focus": "Yes" if paper.morphology_focus else "No",
            "morphological_assumption": paper.morphological_assumption or "",
            "script_specific_design": "Yes" if paper.script_specific_design else "No",
            "transfer_approach": paper.transfer_approach or "",
            "code_available": "Yes" if paper.code_available else "No",
            "data_available": "Yes" if paper.data_available else "No",
            "source": paper.source or "",
            "screening_decision": paper.screening_decision or "",
        }

    def export_by_dimension(self, papers: List[Paper]) -> Dict[str, Path]:
        """Export papers grouped by coding dimension.

        Args:
            papers: List of papers to export

        Returns:
            Dictionary mapping dimension names to export paths
        """
        logger.info("Exporting papers by dimension...")
        outputs = {}

        # By language
        language_papers = self._group_by_language(papers)
        for lang, lang_papers in language_papers.items():
            if lang_papers:
                filename = f"papers_by_language_{lang.replace(' ', '_').lower()}.csv"
                path = self.export(lang_papers, filename)
                outputs[f"language_{lang}"] = path

        # By pillar
        pillar_papers = self._group_by_pillar(papers)
        for pillar, pillar_group in pillar_papers.items():
            if pillar_group:
                filename = (
                    f"papers_by_pillar_{pillar.replace(' ', '_').replace('&', 'and').lower()}.csv"
                )
                path = self.export(pillar_group, filename)
                outputs[f"pillar_{pillar}"] = path

        # By tool type
        tool_papers = self._group_by_tool_type(papers)
        for tool, tool_group in tool_papers.items():
            if tool_group:
                filename = f"papers_by_tooltype_{tool.replace(' ', '_').lower()}.csv"
                path = self.export(tool_group, filename)
                outputs[f"tool_{tool}"] = path

        logger.info(f"Dimension-based export complete: {len(outputs)} files")
        return outputs

    @staticmethod
    def _group_by_language(papers: List[Paper]) -> Dict[str, List[Paper]]:
        """Group papers by language."""
        groups = {}
        for paper in papers:
            for lang in paper.languages:
                if lang not in groups:
                    groups[lang] = []
                groups[lang].append(paper)
        return groups

    @staticmethod
    def _group_by_pillar(papers: List[Paper]) -> Dict[str, List[Paper]]:
        """Group papers by pillar."""
        groups = {}
        for paper in papers:
            if paper.primary_pillar:
                if paper.primary_pillar not in groups:
                    groups[paper.primary_pillar] = []
                groups[paper.primary_pillar].append(paper)
        return groups

    @staticmethod
    def _group_by_tool_type(papers: List[Paper]) -> Dict[str, List[Paper]]:
        """Group papers by tool type."""
        groups = {}
        for paper in papers:
            if paper.tool_type:
                if paper.tool_type not in groups:
                    groups[paper.tool_type] = []
                groups[paper.tool_type].append(paper)
        return groups

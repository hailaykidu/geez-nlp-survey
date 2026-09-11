"""JSON export functionality for coded papers.

Exports papers to JSON format with full structure preservation
for data processing pipelines and downstream analysis.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from src.models.paper import Paper
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class JSONExporter:
    """Export papers to JSON format."""

    def __init__(self, output_dir: str = "data/exported"):
        """Initialize JSON exporter.

        Args:
            output_dir: Path to output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"JSON Exporter initialized (output: {self.output_dir})")

    def export(self, papers: List[Paper], filename: str = "papers.json") -> Path:
        """Export papers to JSON.

        Args:
            papers: List of papers to export
            filename: Output filename

        Returns:
            Path to output JSON file
        """
        output_file = self.output_dir / filename
        logger.info(f"Exporting {len(papers)} papers to JSON...")

        # Convert papers to JSON-serializable dicts
        papers_data = [p.to_json_dict() for p in papers]

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(papers_data, f, indent=2, ensure_ascii=False)

        logger.info(f"JSON export complete: {output_file}")
        return output_file

    def export_with_metadata(
        self,
        papers: List[Paper],
        metadata: Dict[str, Any],
        filename: str = "papers_with_metadata.json",
    ) -> Path:
        """Export papers with metadata.

        Args:
            papers: List of papers to export
            metadata: Dictionary with metadata (count, timestamp, etc.)
            filename: Output filename

        Returns:
            Path to output JSON file
        """
        output_file = self.output_dir / filename
        logger.info(f"Exporting {len(papers)} papers with metadata...")

        papers_data = [p.to_json_dict() for p in papers]

        export_data = {
            "metadata": metadata,
            "papers": papers_data,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"JSON export with metadata complete: {output_file}")
        return output_file

    def export_schema(self) -> Path:
        """Export schema of paper structure.

        Returns:
            Path to schema JSON file
        """
        output_file = self.output_dir / "schema.json"
        logger.info("Exporting paper schema...")

        # Create example schema
        schema = {
            "fields": {
                "id": "string - unique identifier",
                "title": "string - paper title",
                "authors": "list of strings - author names",
                "year": "integer - publication year",
                "venue": "string - publication venue",
                "abstract": "string - paper abstract",
                "languages": "list of strings - target languages",
                "primary_pillar": "string - main research pillar",
                "tool_type": "string - type of contribution",
                "morphology_focus": "boolean - morphology emphasis",
                "morphological_assumption": "string - morphology type",
                "script_specific_design": "boolean - script awareness",
                "transfer_approach": "string - transfer method",
                "code_available": "boolean - code repository available",
                "data_available": "boolean - data/resources available",
                "source": "string - data source",
                "screening_decision": "string - PRISMA screening result",
            },
            "dimensions": {
                "languages": ["Amharic", "Tigrinya", "Classical Ge'ez", "Other"],
                "pillars": [
                    "Tokenization & Normalization",
                    "Lexical & Morphological Analysis",
                    "Text Representation & Embeddings",
                    "Sequence Labeling & Structure Extraction",
                    "Language Models & Deep Learning",
                    "Language Resources & Datasets",
                    "Other NLP",
                ],
                "tool_types": [
                    "Dataset",
                    "Library",
                    "Pipeline",
                    "Algorithm",
                    "Framework",
                    "Corpus",
                    "Tool",
                    "Model",
                    "Other",
                ],
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2)

        logger.info(f"Schema export complete: {output_file}")
        return output_file

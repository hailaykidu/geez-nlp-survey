"""Paper coder for systematic coding across 5 dimensions.

Automatically extracts and codes papers across the 5 research dimensions:
1. Languages (Amharic, Tigrinya, Classical Ge'ez)
2. Primary Pillar (Tokenization, Morphology, Embeddings, Sequence Labeling, etc.)
3. Tool Type (Dataset, Library, Pipeline, Algorithm, etc.)
4. Morphology Focus (Yes/No + Assumption Type)
5. Script-Specific Design (Unicode, Fidel, Abugida, etc.)
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from src.models.paper import Paper
from src.coder.dimensions import (
    Language,
    Pillar,
    MorphologyAssumption,
    TransferApproach,
    LANGUAGE_KEYWORDS,
    PILLAR_KEYWORDS,
    TOOL_TYPE_KEYWORDS,
    MORPHOLOGY_KEYWORDS,
    SCRIPT_KEYWORDS,
    TRANSFER_KEYWORDS,
    CODE_AVAILABLE_KEYWORDS,
    DATA_AVAILABLE_KEYWORDS,
)
from src.coder.validators import CodingValidator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PaperCoder:
    """Extract and code papers across 5 dimensions.

    Uses keyword matching and heuristics to automatically classify papers
    based on their title and abstract across multiple coding dimensions.

    Attributes:
        config_dir: Path to configuration directory
        output_dir: Path to output directory for coded papers
        coded_papers: List of coded papers
    """

    def __init__(self, config_dir: str = "config", output_dir: str = "data/coded"):
        """Initialize paper coder.

        Args:
            config_dir: Path to configuration directory
            output_dir: Path to output directory
        """
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.coded_papers: List[Paper] = []
        logger.info("Paper Coder initialized")

    def code(self, papers: List[Paper]) -> List[Paper]:
        """Code papers across all dimensions.

        Args:
            papers: List of papers to code

        Returns:
            List of coded papers

        """
        logger.info(f"Starting to code {len(papers)} papers...")

        self.coded_papers = []

        for i, paper in enumerate(papers, 1):
            self._code_paper(paper)
            logger.debug(
                f"[{i}/{len(papers)}] Coded: {paper.title[:60]}... " f"({paper.primary_pillar})"
            )

        # Validate batch
        validation = CodingValidator.validate_batch(self.coded_papers)
        logger.info(
            f"Coding validation: {validation['valid']}/{validation['total']} valid "
            f"({validation['valid_rate']*100:.1f}%)"
        )

        # Calculate completeness
        completeness = CodingValidator.get_batch_completeness(self.coded_papers)
        logger.info(
            f"Coding completeness: {completeness['avg_completeness']*100:.1f}% avg, "
            f"{completeness['fully_coded']} fully coded"
        )

        # Save results
        self._save_results()

        logger.info(f"Completed coding {len(self.coded_papers)} papers")

        return self.coded_papers

    def _code_paper(self, paper: Paper) -> None:
        """Code a single paper across all dimensions.

        Args:
            paper: Paper to code
        """
        # Prepare searchable text
        searchable_text = (
            paper.title + " " + paper.abstract + " " + " ".join(paper.authors)
        ).lower()

        # 1. Language coding
        self._code_languages(paper, searchable_text)

        # 2. Primary pillar coding
        self._code_primary_pillar(paper, searchable_text)

        # 3. Tool type coding
        self._code_tool_type(paper, searchable_text)

        # 4. Morphology coding
        self._code_morphology(paper, searchable_text)

        # 5. Script-specific design coding
        self._code_script_design(paper, searchable_text)

        # Reproducibility
        self._code_reproducibility(paper, searchable_text)

        self.coded_papers.append(paper)

    def _code_languages(self, paper: Paper, text: str) -> None:
        """Code target languages."""
        languages_found = []

        for language, keywords in LANGUAGE_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                languages_found.append(language.value)

        # If Ge'ez found, add it
        if "ge'ez" in text or "geez" in text or "ethiopic" in text:
            if Language.CLASSICAL_GEEZ.value not in languages_found:
                languages_found.append(Language.CLASSICAL_GEEZ.value)

        paper.languages = languages_found if languages_found else [Language.OTHER.value]

    def _code_primary_pillar(self, paper: Paper, text: str) -> None:
        """Code primary research pillar."""
        pillar_scores = {}

        for pillar, keywords in PILLAR_KEYWORDS.items():
            score = sum(text.count(kw) for kw in keywords)
            pillar_scores[pillar] = score

        if pillar_scores:
            # Get pillar with highest score
            best_pillar = max(pillar_scores, key=pillar_scores.get)
            if pillar_scores[best_pillar] > 0:
                paper.primary_pillar = best_pillar.value
            else:
                paper.primary_pillar = Pillar.OTHER.value
        else:
            paper.primary_pillar = Pillar.OTHER.value

    def _code_tool_type(self, paper: Paper, text: str) -> None:
        """Code tool type."""
        tool_scores = {}

        for tool_type, keywords in TOOL_TYPE_KEYWORDS.items():
            score = sum(text.count(kw) for kw in keywords)
            tool_scores[tool_type] = score

        if tool_scores:
            best_tool = max(tool_scores, key=tool_scores.get)
            if tool_scores[best_tool] > 0:
                paper.tool_type = best_tool.value

    def _code_morphology(self, paper: Paper, text: str) -> None:
        """Code morphology dimension."""
        # Check if morphology is focus
        morphology_score = sum(text.count(kw) for kw in MORPHOLOGY_KEYWORDS)
        paper.morphology_focus = morphology_score > 0

        if paper.morphology_focus:
            # Detect morphological assumption
            if "agglutinative" in text:
                paper.morphological_assumption = MorphologyAssumption.AGGLUTINATIVE.value
            elif "fusional" in text:
                paper.morphological_assumption = MorphologyAssumption.FUSIONAL.value
            elif "abugida" in text or "syllabic" in text:
                paper.morphological_assumption = MorphologyAssumption.ABUGIDA.value
            elif "unicode" in text or "script" in text:
                paper.morphological_assumption = MorphologyAssumption.SCRIPT_AWARE.value
            else:
                paper.morphological_assumption = MorphologyAssumption.LANGUAGE_AGNOSTIC.value

    def _code_script_design(self, paper: Paper, text: str) -> None:
        """Code script-specific design dimension."""
        # Check if script design is addressed
        script_properties = []
        for prop, keywords in SCRIPT_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                script_properties.append(prop.value)

        paper.script_specific_design = len(script_properties) > 0

        # Code transfer approach
        transfer_scores = {}
        for approach, keywords in TRANSFER_KEYWORDS.items():
            score = sum(text.count(kw) for kw in keywords)
            transfer_scores[approach] = score

        if transfer_scores:
            best_approach = max(transfer_scores, key=transfer_scores.get)
            if transfer_scores[best_approach] > 0:
                paper.transfer_approach = best_approach.value
            else:
                paper.transfer_approach = TransferApproach.MONOLINGUAL.value
        else:
            paper.transfer_approach = TransferApproach.MONOLINGUAL.value

    def _code_reproducibility(self, paper: Paper, text: str) -> None:
        """Code code and data availability."""
        paper.code_available = any(kw in text for kw in CODE_AVAILABLE_KEYWORDS)
        paper.data_available = any(kw in text for kw in DATA_AVAILABLE_KEYWORDS)

    def _save_results(self) -> None:
        """Save coded papers to output files."""
        # Save as JSON
        coded_dir = self.output_dir / "papers"
        coded_dir.mkdir(parents=True, exist_ok=True)

        papers_data = [p.to_json_dict() for p in self.coded_papers]

        papers_file = coded_dir / "papers.json"
        with open(papers_file, "w", encoding="utf-8") as f:
            json.dump(papers_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(self.coded_papers)} coded papers to {papers_file}")

        # Save summary
        self._save_summary()

    def _save_summary(self) -> None:
        """Save coding summary statistics."""
        summary_dir = self.output_dir
        summary_dir.mkdir(parents=True, exist_ok=True)

        # Language distribution
        language_counts = {}
        for paper in self.coded_papers:
            for lang in paper.languages:
                language_counts[lang] = language_counts.get(lang, 0) + 1

        # Pillar distribution
        pillar_counts = {}
        for paper in self.coded_papers:
            if paper.primary_pillar:
                pillar_counts[paper.primary_pillar] = pillar_counts.get(paper.primary_pillar, 0) + 1

        # Tool type distribution
        tool_counts = {}
        for paper in self.coded_papers:
            if paper.tool_type:
                tool_counts[paper.tool_type] = tool_counts.get(paper.tool_type, 0) + 1

        # Morphology stats
        morphology_count = sum(1 for p in self.coded_papers if p.morphology_focus)

        # Script design stats
        script_count = sum(1 for p in self.coded_papers if p.script_specific_design)

        summary = {
            "total_papers": len(self.coded_papers),
            "language_distribution": language_counts,
            "pillar_distribution": pillar_counts,
            "tool_type_distribution": tool_counts,
            "morphology_papers": morphology_count,
            "script_specific_papers": script_count,
            "avg_completeness": CodingValidator.get_batch_completeness(self.coded_papers)[
                "avg_completeness"
            ],
        }

        summary_file = summary_dir / "coding_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Saved coding summary to {summary_file}")

    def get_coding_summary(self) -> Dict[str, Any]:
        """Get summary of coding results.

        Returns:
            Dictionary with coding statistics
        """
        return {
            "total_coded": len(self.coded_papers),
            "languages": list(set(lang for p in self.coded_papers for lang in p.languages)),
            "pillars": list(set(p.primary_pillar for p in self.coded_papers if p.primary_pillar)),
            "tool_types": list(set(p.tool_type for p in self.coded_papers if p.tool_type)),
            "morphology_papers": sum(1 for p in self.coded_papers if p.morphology_focus),
            "script_specific_papers": sum(1 for p in self.coded_papers if p.script_specific_design),
        }

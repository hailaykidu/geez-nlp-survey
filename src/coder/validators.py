"""Validation utilities for paper coding.

Ensures that coded papers have valid values for all 5 dimensions and
provides feedback on coding quality.
"""

from typing import List, Dict, Any, Tuple
from src.models.paper import Paper
from src.coder.dimensions import Language, Pillar, ToolType, TransferApproach


class CodingValidator:
    """Validate paper coding across all dimensions."""

    @staticmethod
    def validate_paper(paper: Paper) -> Tuple[bool, List[str]]:
        """Validate a paper's coding.

        Args:
            paper: Paper to validate

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []

        # Check languages
        if not paper.languages:
            errors.append("No languages assigned")
        else:
            for lang in paper.languages:
                if lang not in [l.value for l in Language]:
                    errors.append(f"Invalid language: {lang}")

        # Check primary pillar
        if not paper.primary_pillar:
            errors.append("No primary pillar assigned")
        elif paper.primary_pillar not in [p.value for p in Pillar]:
            errors.append(f"Invalid primary pillar: {paper.primary_pillar}")

        # Check tool type
        if paper.tool_type:
            if paper.tool_type not in [t.value for t in ToolType]:
                errors.append(f"Invalid tool type: {paper.tool_type}")

        # Check transfer approach
        if paper.transfer_approach:
            if paper.transfer_approach not in [t.value for t in TransferApproach]:
                errors.append(f"Invalid transfer approach: {paper.transfer_approach}")

        # Check morphology consistency
        if paper.morphology_focus and not paper.morphological_assumption:
            errors.append("Morphology focus set but no assumption specified")

        return len(errors) == 0, errors

    @staticmethod
    def validate_batch(papers: List[Paper]) -> Dict[str, Any]:
        """Validate a batch of papers.

        Args:
            papers: List of papers to validate

        Returns:
            Dictionary with validation statistics
        """
        total = len(papers)
        valid_count = 0
        error_count = 0
        errors_by_type = {}

        for paper in papers:
            is_valid, errors = CodingValidator.validate_paper(paper)
            if is_valid:
                valid_count += 1
            else:
                error_count += 1
                for error in errors:
                    error_type = error.split(":")[0]
                    errors_by_type[error_type] = errors_by_type.get(error_type, 0) + 1

        return {
            "total": total,
            "valid": valid_count,
            "invalid": error_count,
            "valid_rate": valid_count / total if total > 0 else 0,
            "errors_by_type": errors_by_type,
        }

    @staticmethod
    def get_coding_completeness(paper: Paper) -> float:
        """Calculate how complete a paper's coding is (0.0 to 1.0).

        Args:
            paper: Paper to evaluate

        Returns:
            Completeness score
        """
        fields_coded = 0
        total_fields = 5

        if paper.languages:
            fields_coded += 1
        if paper.primary_pillar:
            fields_coded += 1
        if paper.tool_type:
            fields_coded += 1
        if paper.morphology_focus or paper.morphological_assumption:
            fields_coded += 1
        if paper.script_specific_design or paper.transfer_approach:
            fields_coded += 1

        return fields_coded / total_fields

    @staticmethod
    def get_batch_completeness(papers: List[Paper]) -> Dict[str, Any]:
        """Calculate completeness statistics for a batch.

        Args:
            papers: List of papers

        Returns:
            Completeness statistics
        """
        if not papers:
            return {
                "avg_completeness": 0.0,
                "fully_coded": 0,
                "partially_coded": 0,
                "incomplete": 0,
            }

        completeness_scores = [
            CodingValidator.get_coding_completeness(p) for p in papers
        ]
        avg_completeness = sum(completeness_scores) / len(completeness_scores)

        fully_coded = sum(1 for s in completeness_scores if s == 1.0)
        incomplete = sum(1 for s in completeness_scores if s == 0.0)
        partially_coded = len(papers) - fully_coded - incomplete

        return {
            "avg_completeness": avg_completeness,
            "fully_coded": fully_coded,
            "partially_coded": partially_coded,
            "incomplete": incomplete,
            "total": len(papers),
        }

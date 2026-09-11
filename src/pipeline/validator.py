"""Pipeline validation and quality assurance.

Validates pipeline inputs, outputs, and data integrity.
"""

from pathlib import Path
from typing import List, Dict, Tuple, Any
from src.models.paper import Paper
from src.coder.validators import CodingValidator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PipelineValidator:
    """Validate systematic review pipeline components and outputs."""

    def __init__(self):
        """Initialize pipeline validator."""
        logger.info("Pipeline Validator initialized")

    def validate_pipeline_inputs(self, papers: List[Paper]) -> Tuple[bool, List[str]]:
        """Validate pipeline input papers.

        Args:
            papers: List of papers to validate

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []

        if not papers:
            errors.append("No papers provided to pipeline")
            return False, errors

        if len(papers) < 5:
            errors.append(f"Too few papers ({len(papers)}); expected minimum 5")

        # Check for duplicates
        paper_ids = [p.id for p in papers]
        if len(paper_ids) != len(set(paper_ids)):
            errors.append("Duplicate paper IDs detected")

        # Check required fields
        for i, paper in enumerate(papers):
            if not paper.title:
                errors.append(f"Paper {i} missing title")
            if not paper.authors:
                errors.append(f"Paper {i} missing authors")
            if not paper.year:
                errors.append(f"Paper {i} missing year")

        is_valid = len(errors) == 0
        logger.info(f"Input validation: {'PASS' if is_valid else 'FAIL'} ({len(papers)} papers)")
        if errors:
            logger.warning(f"  Errors: {len(errors)}")

        return is_valid, errors

    def validate_pipeline_outputs(self, papers: List[Paper]) -> Dict[str, Any]:
        """Validate pipeline output papers.

        Args:
            papers: List of coded papers

        Returns:
            Dictionary with validation results
        """
        logger.info("Validating pipeline outputs...")

        results = {
            "total_papers": len(papers),
            "valid_papers": 0,
            "invalid_papers": 0,
            "validation_rate": 0.0,
            "completeness_avg": 0.0,
            "completeness_by_category": {},
            "errors_by_type": {},
        }

        if not papers:
            return results

        # Validate each paper
        valid_count = 0
        completeness_scores = []

        for paper in papers:
            is_valid, errors = CodingValidator.validate_paper(paper)
            if is_valid:
                valid_count += 1

            completeness = CodingValidator.get_coding_completeness(paper)
            completeness_scores.append(completeness)

            # Track errors
            for error in errors:
                error_type = error.split(":")[0]
                results["errors_by_type"][error_type] = (
                    results["errors_by_type"].get(error_type, 0) + 1
                )

        results["valid_papers"] = valid_count
        results["invalid_papers"] = len(papers) - valid_count
        results["validation_rate"] = valid_count / len(papers) * 100 if papers else 0

        if completeness_scores:
            results["completeness_avg"] = sum(completeness_scores) / len(completeness_scores)

        # Batch completeness
        batch_completeness = CodingValidator.get_batch_completeness(papers)
        results["completeness_by_category"] = {
            "fully_coded": batch_completeness["fully_coded"],
            "partially_coded": batch_completeness["partially_coded"],
            "incomplete": batch_completeness["incomplete"],
        }

        logger.info(
            f"Output validation: {valid_count}/{len(papers)} valid "
            f"({results['validation_rate']:.1f}%)"
        )
        logger.info(f"  Completeness: {results['completeness_avg']:.1%} avg")
        logger.info(f"  Fully coded: {batch_completeness['fully_coded']}")

        return results

    def validate_output_files(self, output_dir: Path) -> Dict[str, bool]:
        """Validate that all expected output files exist.

        Args:
            output_dir: Path to output directory

        Returns:
            Dictionary of file existence checks
        """
        logger.info("Validating output files...")

        checks = {
            "csv_export": (output_dir / "papers.csv").exists(),
            "json_export": (output_dir / "papers.json").exists(),
            "json_schema": (output_dir / "schema.json").exists(),
            "statistics_report": (output_dir / "statistics_report.txt").exists(),
            "language_chart": (output_dir / "chart_language_distribution.png").exists(),
            "pillar_chart": (output_dir / "chart_pillar_distribution.png").exists(),
            "tool_chart": (output_dir / "chart_tool_type_distribution.png").exists(),
            "temporal_chart": (output_dir / "chart_temporal_distribution.png").exists(),
            "morphology_chart": (output_dir / "chart_morphology_focus.png").exists(),
            "reproducibility_chart": (output_dir / "chart_reproducibility.png").exists(),
            "synthesis_report": (output_dir / "synthesis_report.md").exists(),
        }

        missing = [k for k, v in checks.items() if not v]
        if missing:
            logger.warning(f"Missing files: {missing}")
        else:
            logger.info(f"All {len(checks)} expected output files present")

        return checks

    def validate_data_integrity(self, papers: List[Paper]) -> Dict[str, Any]:
        """Validate data integrity across pipeline.

        Args:
            papers: List of papers to validate

        Returns:
            Dictionary with integrity checks
        """
        logger.info("Checking data integrity...")

        checks = {
            "duplicate_ids": len([p.id for p in papers]) == len(set(p.id for p in papers)),
            "all_titled": all(p.title for p in papers),
            "all_authored": all(p.authors for p in papers),
            "all_years_valid": all(p.year and 1900 < p.year < 2100 for p in papers),
            "language_coverage": len(set(lang for p in papers for lang in p.languages)) > 0,
            "pillar_coverage": len(set(p.primary_pillar for p in papers if p.primary_pillar)) > 0,
        }

        issues = [k for k, v in checks.items() if not v]
        if issues:
            logger.warning(f"Data integrity issues: {issues}")
        else:
            logger.info("Data integrity: OK")

        return checks

    def generate_validation_report(self, papers: List[Paper], output_dir: Path) -> Path:
        """Generate comprehensive validation report.

        Args:
            papers: List of papers
            output_dir: Output directory

        Returns:
            Path to validation report
        """
        logger.info("Generating validation report...")

        # Run all validations
        inputs_valid, input_errors = self.validate_pipeline_inputs(papers)
        outputs = self.validate_pipeline_outputs(papers)
        file_checks = self.validate_output_files(output_dir)
        integrity = self.validate_data_integrity(papers)

        # Create report
        report_file = output_dir / "validation_report.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("PIPELINE VALIDATION REPORT\n")
            f.write("=" * 70 + "\n\n")

            f.write("INPUT VALIDATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Status: {'PASS' if inputs_valid else 'FAIL'}\n")
            if input_errors:
                f.write(f"Errors ({len(input_errors)}):\n")
                for error in input_errors:
                    f.write(f"  - {error}\n")
            f.write("\n")

            f.write("OUTPUT VALIDATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Papers: {outputs['total_papers']}\n")
            f.write(f"Valid Papers: {outputs['valid_papers']}/{outputs['total_papers']}\n")
            f.write(f"Validation Rate: {outputs['validation_rate']:.1f}%\n")
            f.write(f"Avg Completeness: {outputs['completeness_avg']:.1%}\n")
            f.write(f"Fully Coded: {outputs['completeness_by_category']['fully_coded']}\n")
            f.write(f"Partially Coded: {outputs['completeness_by_category']['partially_coded']}\n")
            f.write(f"Incomplete: {outputs['completeness_by_category']['incomplete']}\n")
            if outputs["errors_by_type"]:
                f.write(f"Errors by Type:\n")
                for error_type, count in outputs["errors_by_type"].items():
                    f.write(f"  - {error_type}: {count}\n")
            f.write("\n")

            f.write("FILE VALIDATION\n")
            f.write("-" * 70 + "\n")
            for file_name, exists in file_checks.items():
                status = "✓" if exists else "✗"
                f.write(f"  {status} {file_name}\n")
            f.write("\n")

            f.write("DATA INTEGRITY\n")
            f.write("-" * 70 + "\n")
            for check_name, result in integrity.items():
                status = "✓" if result else "✗"
                f.write(f"  {status} {check_name}\n")
            f.write("\n")

            # Overall status
            all_valid = (
                inputs_valid
                and outputs["validation_rate"] >= 80
                and all(file_checks.values())
                and all(integrity.values())
            )
            f.write("=" * 70 + "\n")
            f.write(f"OVERALL STATUS: {'PASS' if all_valid else 'FAIL'}\n")
            f.write("=" * 70 + "\n")

        logger.info(f"Validation report saved: {report_file}")
        return report_file

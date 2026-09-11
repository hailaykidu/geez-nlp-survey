#!/usr/bin/env python3
"""Main CLI entry point for Ge'ez-Script NLP Systematic Review Pipeline.

End-to-end PRISMA systematic review pipeline for Ge'ez-script languages (Amharic, Tigrinya, Ge'ez).
"""

import argparse
import sys
from pathlib import Path
from src.pipeline.orchestrator import SystematicReviewOrchestrator
from src.pipeline.validator import PipelineValidator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ge'ez-Script NLP Tools Systematic Review Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline
  python main.py --run-full-pipeline

  # Validate pipeline outputs
  python main.py --validate-outputs data/pipeline_output

  # Run specific phases
  python main.py --phase search
  python main.py --phase screen
  python main.py --phase code
  python main.py --phase export
  python main.py --phase visualize

  # Generate reports
  python main.py --generate-reports data/pipeline_output

For more information, see README_USAGE.md
        """,
    )

    # Main execution modes
    parser.add_argument(
        "--run-full-pipeline",
        action="store_true",
        help="Run complete PRISMA systematic review pipeline (phases 1-8)",
    )

    parser.add_argument(
        "--phase",
        choices=["search", "screen", "code", "export", "visualize"],
        help="Run specific pipeline phase",
    )

    parser.add_argument(
        "--validate-outputs",
        type=str,
        metavar="DIR",
        help="Validate pipeline outputs in specified directory",
    )

    parser.add_argument(
        "--generate-reports",
        type=str,
        metavar="DIR",
        help="Generate validation and summary reports from outputs",
    )

    # Configuration
    parser.add_argument(
        "--config-dir",
        type=str,
        default="config",
        help="Configuration directory (default: config)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/pipeline_output",
        help="Output directory for results (default: data/pipeline_output)",
    )

    # Logging
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level (default: INFO)",
    )

    # Information
    parser.add_argument(
        "--version",
        action="version",
        version="Ge'ez-Script NLP Survey Pipeline v1.0",
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Display pipeline information and architecture",
    )

    args = parser.parse_args()

    # Display information if requested
    if args.info:
        _display_info()
        return 0

    # Validate arguments
    if not any(
        [
            args.run_full_pipeline,
            args.phase,
            args.validate_outputs,
            args.generate_reports,
        ]
    ):
        parser.print_help()
        return 0

    try:
        # Run full pipeline
        if args.run_full_pipeline:
            return _run_full_pipeline(args)

        # Run specific phase
        if args.phase:
            return _run_phase(args, args.phase)

        # Validate outputs
        if args.validate_outputs:
            return _validate_outputs(args)

        # Generate reports
        if args.generate_reports:
            return _generate_reports(args)

    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}", exc_info=True)
        return 1

    return 0


def _display_info():
    """Display pipeline information."""
    info = """
╔════════════════════════════════════════════════════════════════════════════╗
║        Ge'ez-Script NLP Tools Systematic Review Pipeline (PRISMA)         ║
╚════════════════════════════════════════════════════════════════════════════╝

LANGUAGES COVERED:
  • Amharic (Amharic script)
  • Tigrinya (Ge'ez script)
  • Classical Ge'ez (Ge'ez script)

PIPELINE PHASES:
  Phase 1: Paper Search (Semantic Scholar + ACL Anthology)
  Phase 2: PRISMA Screening (Title/Abstract/Full-text)
  Phase 3: Paper Coding (5 dimensions)
  Phase 4: Data Export (CSV/JSON/Statistics)
  Phase 5: Visualization (6 publication charts)
  Phase 6: Report Synthesis (13-section narrative)
  Phase 7: Validation (Data integrity checks)
  Phase 8: Documentation (User guide + architecture)

CODING DIMENSIONS:
  1. Languages (Amharic, Tigrinya, Classical Ge'ez, Other)
  2. Primary Pillar (7 research areas)
  3. Tool Type (Dataset, Library, Pipeline, Algorithm, etc.)
  4. Morphology (Focus + Assumption type)
  5. Script Design (Unicode, Fidel, Abugida handling)

KEY COMPONENTS:
  • src/searcher/: Paper search (Semantic Scholar, ACL Anthology)
  • src/screener/: PRISMA screening logic
  • src/coder/: Automated 5-dimensional paper coding
  • src/export/: CSV/JSON export + statistics
  • src/visualization/: Charts + synthesis report
  • src/pipeline/: Orchestration + validation
  • tests/unit/: 194+ unit tests (100% coverage)

CONFIGURATION:
  • config/search_config.json: Search keywords and sources
  • config/screening_config.json: Screening criteria
  • config/coding_config.json: Coding dimension mappings

OUTPUT STRUCTURE:
  data/pipeline_output/
  ├── exports/
  │   ├── papers.csv (40-60 papers)
  │   ├── papers.json (full structure)
  │   ├── schema.json (field documentation)
  │   └── statistics_report.txt (summary stats)
  ├── visualizations/
  │   ├── chart_language_distribution.png
  │   ├── chart_pillar_distribution.png
  │   ├── chart_tool_type_distribution.png
  │   ├── chart_temporal_distribution.png
  │   ├── chart_morphology_focus.png
  │   ├── chart_reproducibility.png
  │   └── synthesis_report.md (13-section narrative)
  └── validation/
      └── validation_report.txt (integrity checks)

TEST COVERAGE:
  • 194+ unit tests across all components
  • 100% code coverage for critical paths
  • Integration tests for complete pipeline
  • Validation tests for data integrity

REFERENCES:
  • PRISMA: http://www.prisma-statement.org/
  • Ge'ez Script: https://en.wikipedia.org/wiki/Ge%27ez_script
  • Amharic: https://en.wikipedia.org/wiki/Amharic
  • Tigrinya: https://en.wikipedia.org/wiki/Tigrinya_language

For detailed usage, see README_USAGE.md
    """
    print(info)


def _run_full_pipeline(args):
    """Run complete PRISMA pipeline."""
    logger.info("Starting full PRISMA systematic review pipeline...")
    orchestrator = SystematicReviewOrchestrator(config_dir=args.config_dir)
    results = orchestrator.run_full_pipeline()

    if results["summary"]["status"] == "SUCCESS":
        logger.info("=" * 70)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        logger.info(f"Output directory: {orchestrator.output_dir}")
        logger.info(f"Total papers searched: {results['summary']['total_searched']}")
        logger.info(f"Total papers screened: {results['summary']['total_screened']}")
        logger.info(f"Total papers coded: {results['summary']['total_coded']}")
        return 0
    else:
        logger.error(f"Pipeline failed: {results['summary'].get('error', 'Unknown error')}")
        return 1


def _run_phase(args, phase_name):
    """Run specific pipeline phase."""
    logger.info(f"Running pipeline phase: {phase_name}...")

    phase_methods = {
        "search": "Search (Semantic Scholar + ACL Anthology)",
        "screen": "PRISMA Screening",
        "code": "Paper Coding",
        "export": "Data Export",
        "visualize": "Visualization & Synthesis",
    }

    logger.info(f"Phase: {phase_methods.get(phase_name, 'Unknown')}")
    logger.info("Note: Individual phase execution requires manual setup of input data")
    logger.info("Use --run-full-pipeline for complete end-to-end execution")

    return 0


def _validate_outputs(args):
    """Validate pipeline outputs."""
    output_dir = Path(args.validate_outputs)

    if not output_dir.exists():
        logger.error(f"Output directory not found: {output_dir}")
        return 1

    logger.info(f"Validating pipeline outputs: {output_dir}")

    validator = PipelineValidator()

    # Load papers from JSON if available
    papers_json = output_dir / "papers.json"
    if papers_json.exists():
        import json

        with open(papers_json, "r", encoding="utf-8") as f:
            papers_data = json.load(f)
            # Note: In production, would reconstruct Paper objects
            logger.info(f"Found {len(papers_data)} papers in output")

    # Validate files
    checks = validator.validate_output_files(output_dir)
    present = sum(1 for v in checks.values() if v)
    logger.info(f"Files present: {present}/{len(checks)}")

    return 0


def _generate_reports(args):
    """Generate validation and summary reports."""
    output_dir = Path(args.generate_reports)

    if not output_dir.exists():
        logger.error(f"Output directory not found: {output_dir}")
        return 1

    logger.info(f"Generating reports for: {output_dir}")
    logger.info("Report generation not yet implemented for standalone execution")
    logger.info("Use --run-full-pipeline to generate complete reports")

    return 0


if __name__ == "__main__":
    sys.exit(main())

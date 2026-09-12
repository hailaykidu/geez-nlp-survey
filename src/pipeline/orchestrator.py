"""End-to-end PRISMA systematic review pipeline orchestrator.

Coordinates all phases: search, screening, coding, export, and visualization.
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import json


from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger
from src.searcher.semantic_scholar_searcher import SemanticScholarSearcher
from src.searcher.acl_anthology_searcher import ACLAnthologySearcher
from src.screener.prisma_screener import PRISMAScreener
from src.coder.coder import PaperCoder
from src.export.csv_exporter import CSVExporter
from src.export.json_exporter import JSONExporter
from src.export.report_generator import ReportGenerator
from src.visualization.chart_generator import ChartGenerator
from src.visualization.synthesis_report import SynthesisReportGenerator

logger = setup_logger(__name__)


class SystematicReviewOrchestrator:
    """Orchestrate complete PRISMA systematic review pipeline."""

    def __init__(self, config_dir: str = "config"):
        """Initialize orchestrator.

        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = Path(config_dir)
        self.config_loader = ConfigLoader(config_dir)
        self.output_dir = Path("data/pipeline_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.searched_papers = []
        self.screened_papers = []
        self.coded_papers = []

        logger.info("Systematic Review Orchestrator initialized")

    def run_full_pipeline(self) -> Dict[str, Any]:
        """Run complete systematic review pipeline.

        Returns:
            Dictionary with pipeline results and statistics
        """
        logger.info("=" * 70)
        logger.info("STARTING PRISMA SYSTEMATIC REVIEW PIPELINE")
        logger.info("=" * 70)

        start_time = datetime.now()
        results = {}

        try:
            # Phase 1: Load configuration
            logger.info("\n[PHASE 0] Loading configuration...")
            config = self._load_configuration()
            results["configuration"] = config

            # Phase 2: Search
            logger.info("\n[PHASE 1] Running paper search...")
            results["search"] = self._run_search_phase(config)

            # Phase 3: Screening
            logger.info("\n[PHASE 2] Running PRISMA screening...")
            results["screening"] = self._run_screening_phase(config)

            # Phase 4: Coding
            logger.info("\n[PHASE 3] Running paper coding...")
            results["coding"] = self._run_coding_phase(config)

            # Phase 5: Export
            logger.info("\n[PHASE 4] Exporting data...")
            results["export"] = self._run_export_phase()

            # Phase 6: Visualization
            logger.info("\n[PHASE 5] Generating visualizations...")
            results["visualization"] = self._run_visualization_phase()

            # Phase 7: Summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            results["summary"] = {
                "status": "SUCCESS",
                "timestamp": end_time.isoformat(),
                "duration_seconds": duration,
                "total_searched": len(self.searched_papers),
                "total_screened": len(self.screened_papers),
                "total_coded": len(self.coded_papers),
            }

            self._save_pipeline_report(results)

            logger.info("\n" + "=" * 70)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 70)

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            results["summary"] = {
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

        return results

    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration for all phases.

        Returns:
            Configuration dictionary
        """
        config = self.config_loader.load_all_configs()
        logger.info(f"Loaded configuration from {self.config_dir}")
        logger.info(f"  - Search config: {len(config.get('search', {}))} settings")
        logger.info(f"  - Screening config: {len(config.get('screening', {}))} settings")
        logger.info(f"  - Coding config: {len(config.get('coding', {}))} settings")
        return config

    def _run_search_phase(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run paper search phase.

        Args:
            config: Configuration dictionary

        Returns:
            Search phase results
        """
        search_config = config.get("search", {})
        results = {}

        # Flatten all keywords from all languages
        keywords = []
        search_terms = search_config.get("search_terms", {})
        for language, terms in search_terms.items():
            if isinstance(terms, list):
                keywords.extend(terms)

        logger.info(f"  - Total keywords to search: {len(keywords)}")

        # Semantic Scholar search
        logger.info("  - Searching Semantic Scholar...")
        ss_searcher = SemanticScholarSearcher(config)
        ss_papers = ss_searcher.search(keywords)
        self.searched_papers.extend(ss_papers)
        results["semantic_scholar"] = {
            "papers_found": len(ss_papers),
            "keywords": len(keywords),
        }
        logger.info(f"    Found {len(ss_papers)} papers from Semantic Scholar")

        # ACL Anthology search
        logger.info("  - Searching ACL Anthology...")
        acl_searcher = ACLAnthologySearcher(config)
        acl_papers = acl_searcher.search(keywords)
        self.searched_papers.extend(acl_papers)
        results["acl_anthology"] = {
            "papers_found": len(acl_papers),
            "keywords": len(keywords),
        }
        logger.info(f"    Found {len(acl_papers)} papers from ACL Anthology")

        results["total_searched"] = len(self.searched_papers)
        logger.info(f"  - Total papers found: {len(self.searched_papers)}")

        return results

    def _run_screening_phase(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run PRISMA screening phase.

        Args:
            config: Configuration dictionary

        Returns:
            Screening phase results
        """
        screener = PRISMAScreener()
        included, excluded = screener.screen(self.searched_papers)
        self.screened_papers = included

        screening_stats = screener.get_summary()
        logger.info(f"  - Screened {len(self.searched_papers)} papers")
        logger.info(f"    Included: {screening_stats.get('papers_included', 0)}")
        logger.info(f"    Excluded: {screening_stats.get('papers_excluded', 0)}")

        return {
            "total_screened": len(self.searched_papers),
            "total_included": len(included),
            "total_excluded": len(excluded),
            "statistics": screening_stats,
        }

    def _run_coding_phase(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run paper coding phase.

        Args:
            config: Configuration dictionary

        Returns:
            Coding phase results
        """
        coder = PaperCoder()
        self.coded_papers = coder.code(self.screened_papers)

        coding_summary = coder.get_coding_summary()
        logger.info(f"  - Coded {len(self.coded_papers)} papers")
        logger.info(f"    Languages: {coding_summary.get('languages', [])}")
        logger.info(f"    Pillars: {len(coding_summary.get('pillars', []))} areas")

        return {
            "total_coded": len(self.coded_papers),
            "summary": coding_summary,
        }

    def _run_export_phase(self) -> Dict[str, Any]:
        """Run data export phase.

        Returns:
            Export phase results
        """
        export_dir = self.output_dir / "exports"
        results = {}

        # CSV export
        logger.info("  - Exporting to CSV...")
        csv_exporter = CSVExporter(output_dir=str(export_dir))
        csv_file = csv_exporter.export(self.coded_papers)
        results["csv"] = str(csv_file)
        logger.info(f"    CSV: {csv_file.name}")

        # JSON export
        logger.info("  - Exporting to JSON...")
        json_exporter = JSONExporter(output_dir=str(export_dir))
        json_file = json_exporter.export(self.coded_papers)
        json_schema = json_exporter.export_schema()
        results["json"] = str(json_file)
        results["schema"] = str(json_schema)
        logger.info(f"    JSON: {json_file.name}")

        # Statistics report
        logger.info("  - Generating statistics...")
        report_gen = ReportGenerator(output_dir=str(export_dir))
        report = report_gen.generate_statistics_report(self.coded_papers)
        report_file = report_gen.save_report(report)
        results["statistics"] = str(report_file)
        logger.info(f"    Report: {report_file.name}")

        return results

    def _run_visualization_phase(self) -> Dict[str, Any]:
        """Run visualization phase.

        Returns:
            Visualization phase results
        """
        viz_dir = self.output_dir / "visualizations"
        results = {}

        # Generate charts
        logger.info("  - Generating charts...")
        chart_gen = ChartGenerator(output_dir=str(viz_dir))
        charts = chart_gen.generate_all_charts(self.coded_papers)
        results["charts"] = {name: str(path) for name, path in charts.items()}
        logger.info(f"    Generated {len(charts)} publication-quality charts")

        # Generate synthesis report
        logger.info("  - Generating synthesis report...")
        report_gen = SynthesisReportGenerator(output_dir=str(viz_dir))
        synthesis = report_gen.generate_synthesis_report(self.coded_papers)
        synthesis_file = report_gen.save_synthesis_report(synthesis)
        results["synthesis_report"] = str(synthesis_file)
        logger.info(f"    Synthesis: {synthesis_file.name}")

        return results

    def _save_pipeline_report(self, results: Dict[str, Any]) -> Path:
        """Save complete pipeline report.

        Args:
            results: Pipeline results dictionary

        Returns:
            Path to report file
        """
        report_file = self.output_dir / "pipeline_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Pipeline report saved: {report_file}")
        return report_file

    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics.

        Returns:
            Dictionary with pipeline statistics
        """
        return {
            "searched_papers": len(self.searched_papers),
            "screened_papers": len(self.screened_papers),
            "coded_papers": len(self.coded_papers),
            "screening_rate": (
                len(self.screened_papers) / len(self.searched_papers) * 100
                if self.searched_papers
                else 0
            ),
        }

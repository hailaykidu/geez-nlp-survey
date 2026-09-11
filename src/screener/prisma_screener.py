"""PRISMA-style systematic review screening for Ge'ez-Script NLP papers.

Implements screening logic to apply inclusion/exclusion criteria from PRISMA
methodology to filter papers for the survey.
"""

import json
from pathlib import Path
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from src.models.paper import Paper, ScreeningDecision, ScreeningDecisionCode
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class ScreeningResult:
    """Result of screening a single paper."""

    paper_id: str
    title: str
    included: bool
    reason: str
    criteria_results: Dict[str, bool]


class PRISMAScreener:
    """Apply PRISMA inclusion/exclusion criteria to papers.

    Uses systematic inclusion/exclusion criteria to filter papers based on:
    - Peer-review status
    - Target language (Amharic, Tigrinya, Ge'ez)
    - NLP tool/contribution focus
    - Publication year (2016-2026)
    - Paper availability/scope

    Attributes:
        config_dir: Path to configuration directory
        output_dir: Path to output directory for screened papers
        config: Loaded screening configuration
        included: List of included papers
        excluded: List of excluded papers
        screening_results: Detailed screening results for each paper
    """

    def __init__(self, config_dir: str = "config", output_dir: str = "data/screened"):
        """Initialize PRISMA screener.

        Args:
            config_dir: Path to configuration directory (default: "config")
            output_dir: Path to output directory (default: "data/screened")
        """
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.config = self._load_config()
        self.included: List[Paper] = []
        self.excluded: List[Paper] = []
        self.screening_results: List[ScreeningResult] = []

        logger.info(f"PRISMA Screener initialized with config from {config_dir}")

    def _load_config(self) -> Dict[str, Any]:
        """Load screening configuration from JSON.

        Returns:
            Screening configuration dictionary

        Raises:
            FileNotFoundError: If screening criteria not found
            json.JSONDecodeError: If JSON is invalid
        """
        config_path = self.config_dir / "screening_criteria.json"

        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
                logger.debug(f"Loaded screening config from {config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"Screening config not found: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in screening config: {e}")
            raise

    def screen(self, papers: List[Paper]) -> Tuple[List[Paper], List[Paper]]:
        """Screen papers using PRISMA criteria.

        Applies inclusion/exclusion criteria to each paper and separates them
        into included and excluded groups.

        Args:
            papers: List of Paper objects to screen

        Returns:
            Tuple of (included_papers, excluded_papers)
        """
        logger.info(f"Starting PRISMA screening of {len(papers)} papers...")

        self.included = []
        self.excluded = []
        self.screening_results = []

        for i, paper in enumerate(papers, 1):
            logger.debug(f"[{i}/{len(papers)}] Screening: {paper.title[:60]}...")

            result = self._evaluate_paper(paper)
            self.screening_results.append(result)

            if result.included:
                paper.screened = True
                paper.included = True
                self.included.append(paper)
                logger.debug(f"  ✓ INCLUDED: {result.reason}")
            else:
                paper.screened = True
                paper.included = False
                paper.screening_decision = result.reason
                self.excluded.append(paper)
                logger.debug(f"  ✗ EXCLUDED: {result.reason}")

        # Log summary
        logger.info(
            f"Screening complete: {len(self.included)} included, " f"{len(self.excluded)} excluded"
        )

        # Save results
        self._save_results()

        return self.included, self.excluded

    def _evaluate_paper(self, paper: Paper) -> ScreeningResult:
        """Evaluate a paper against all PRISMA criteria.

        Args:
            paper: Paper to evaluate

        Returns:
            ScreeningResult with inclusion decision and reasoning
        """
        criteria_results = {}

        # Criterion 1: Year range
        year_valid = self._check_year_range(paper)
        criteria_results["year_range"] = year_valid
        if not year_valid:
            return ScreeningResult(
                paper_id=paper.id,
                title=paper.title,
                included=False,
                reason="OUT_OF_DATE",
                criteria_results=criteria_results,
            )

        # Criterion 2: Target language mentioned
        language_valid = self._check_target_language(paper)
        criteria_results["target_language"] = language_valid
        if not language_valid:
            return ScreeningResult(
                paper_id=paper.id,
                title=paper.title,
                included=False,
                reason="NO_GEEZ_SCRIPT_LANGUAGE",
                criteria_results=criteria_results,
            )

        # Criterion 3: NLP focus/foundational tool
        nlp_valid = self._check_nlp_focus(paper)
        criteria_results["nlp_focus"] = nlp_valid
        if not nlp_valid:
            return ScreeningResult(
                paper_id=paper.id,
                title=paper.title,
                included=False,
                reason="NO_FOUNDATIONAL_TOOL",
                criteria_results=criteria_results,
            )

        # Criterion 4: Tool development central (not just application)
        tool_central = self._check_tool_centrality(paper)
        criteria_results["tool_centrality"] = tool_central
        if not tool_central:
            return ScreeningResult(
                paper_id=paper.id,
                title=paper.title,
                included=False,
                reason="DOWNSTREAM_APPLICATION_ONLY",
                criteria_results=criteria_results,
            )

        # All criteria passed
        return ScreeningResult(
            paper_id=paper.id,
            title=paper.title,
            included=True,
            reason="MEETS_ALL_CRITERIA",
            criteria_results=criteria_results,
        )

    def _check_year_range(self, paper: Paper) -> bool:
        """Check if paper is within acceptable year range.

        Args:
            paper: Paper to check

        Returns:
            True if paper year is within range, False otherwise
        """
        filters = self.config.get("filters", {})
        year_min = filters.get("year_min", 2016)
        year_max = filters.get("year_max", 2026)

        if paper.year < year_min or paper.year > year_max:
            logger.debug(f"  Year {paper.year} outside range [{year_min}, {year_max}]")
            return False

        return True

    def _check_target_language(self, paper: Paper) -> bool:
        """Check if paper mentions target language (Amharic, Tigrinya, Ge'ez).

        Args:
            paper: Paper to check

        Returns:
            True if target language mentioned, False otherwise
        """
        # Get keywords from config
        criteria = self.config.get("inclusion_criteria", {})
        language_criteria = criteria.get("target_language_mentioned", {})
        keywords = language_criteria.get("keywords", [])

        if not keywords:
            logger.warning("No target language keywords in config")
            return False

        # Combine title and abstract for searching
        searchable_text = (paper.title + " " + paper.abstract).lower()

        # Check if any keyword is mentioned
        found_keywords = [kw for kw in keywords if kw.lower() in searchable_text]

        if not found_keywords:
            logger.debug(f"  No target language keywords found. Searched for: {keywords[:3]}...")
            return False

        logger.debug(f"  Found target language: {found_keywords}")
        return True

    def _check_nlp_focus(self, paper: Paper) -> bool:
        """Check if paper has NLP tool/dataset/framework focus.

        Args:
            paper: Paper to check

        Returns:
            True if NLP focus detected, False otherwise
        """
        # Keywords indicating NLP tools/contributions
        nlp_keywords = [
            "nlp",
            "morpholog",
            "tokeniz",
            "embedding",
            "ner",
            "parsing",
            "language model",
            "corpus",
            "dataset",
            "tool",
            "tagger",
            "lemmatiz",
            "stemm",
            "pos tag",
            "part-of-speech",
            "syntactic",
            "semantic",
            "word2vec",
            "fasttext",
            "bert",
            "transformer",
            "lstm",
            "rnn",
            "neural",
        ]

        searchable_text = (paper.title + " " + paper.abstract).lower()

        found_keywords = [kw for kw in nlp_keywords if kw in searchable_text]

        if not found_keywords:
            logger.debug(f"  No NLP keywords found")
            return False

        logger.debug(f"  Found NLP focus: {found_keywords}")
        return True

    def _check_tool_centrality(self, paper: Paper) -> bool:
        """Check if tool development/evaluation is central to paper.

        Excludes papers that only apply existing tools to downstream tasks.

        Args:
            paper: Paper to check

        Returns:
            True if tool development is central, False if only application
        """
        searchable_text = (paper.title + " " + paper.abstract).lower()

        # Keywords indicating tool development focus
        development_keywords = [
            "propose",
            "develop",
            "design",
            "present",
            "introduce",
            "build",
            "construct",
            "implement",
            "create",
            "framework",
            "architecture",
            "pipeline",
            "toolkit",
        ]

        # Keywords indicating downstream application only
        application_only_keywords = [
            "machine translation",
            "sentiment analysis",
            "text summarization",
            "question answering",
            "classification",
            "clustering",
            "applied to",
            "using existing",
            "utilize",
            "employ",
        ]

        # Check for development focus
        has_development = any(kw in searchable_text for kw in development_keywords)

        # Check for application-only focus
        has_application_only = any(kw in searchable_text for kw in application_only_keywords)

        # Include if has development OR doesn't explicitly mention application-only
        if has_development or not has_application_only:
            logger.debug(f"  Tool centrality: development-focused or not explicitly application")
            return True

        logger.debug(f"  Tool centrality: application-only (excluded)")
        return False

    def _save_results(self) -> None:
        """Save screening results to JSON files.

        Saves included and excluded papers to separate directories with
        complete paper metadata and screening decisions.
        """
        # Save included papers
        included_dir = self.output_dir / "included"
        included_dir.mkdir(parents=True, exist_ok=True)

        included_data = []
        for paper in self.included:
            data = paper.to_json_dict()
            data["screening_decision"] = "INCLUDED"
            included_data.append(data)

        included_file = included_dir / "papers.json"
        with open(included_file, "w", encoding="utf-8") as f:
            json.dump(included_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(self.included)} included papers to {included_file}")

        # Save excluded papers
        excluded_dir = self.output_dir / "excluded"
        excluded_dir.mkdir(parents=True, exist_ok=True)

        excluded_data = []
        for paper in self.excluded:
            data = paper.to_json_dict()
            excluded_data.append(data)

        excluded_file = excluded_dir / "papers.json"
        with open(excluded_file, "w", encoding="utf-8") as f:
            json.dump(excluded_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(self.excluded)} excluded papers to {excluded_file}")

        # Save summary report
        summary_file = self.output_dir / "screening_summary.json"
        summary = {
            "total_papers": len(self.included) + len(self.excluded),
            "included": len(self.included),
            "excluded": len(self.excluded),
            "inclusion_rate": (
                len(self.included) / (len(self.included) + len(self.excluded))
                if (len(self.included) + len(self.excluded)) > 0
                else 0
            ),
        }

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Saved screening summary to {summary_file}")

    def get_summary(self) -> Dict[str, Any]:
        """Get screening summary statistics.

        Returns:
            Dictionary with screening results summary
        """
        total = len(self.included) + len(self.excluded)
        inclusion_rate = len(self.included) / total if total > 0 else 0

        return {
            "total_papers_screened": total,
            "papers_included": len(self.included),
            "papers_excluded": len(self.excluded),
            "inclusion_rate": inclusion_rate,
            "inclusion_percentage": f"{inclusion_rate * 100:.1f}%",
        }

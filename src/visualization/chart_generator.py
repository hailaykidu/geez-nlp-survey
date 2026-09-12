"""Chart generation for systematic review visualization.

Creates publication-quality charts for research findings using matplotlib.
"""

from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from src.models.paper import Paper
from src.utils.logger import setup_logger

# Use non-interactive backend for server environments
matplotlib.use("Agg")

logger = setup_logger(__name__)


class ChartGenerator:
    """Generate publication-quality charts from survey data."""

    def __init__(self, output_dir: str = "data/visualization"):
        """Initialize chart generator.

        Args:
            output_dir: Path to output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = 300  # Publication quality
        logger.info(f"Chart Generator initialized (output: {self.output_dir})")

    def generate_all_charts(self, papers: List[Paper]) -> Dict[str, Path]:
        """Generate all publication charts.

        Args:
            papers: List of papers to visualize

        Returns:
            Dictionary mapping chart names to file paths
        """
        logger.info(f"Generating charts from {len(papers)} papers...")
        charts = {}

        charts["languages"] = self.chart_language_distribution(papers)
        charts["pillars"] = self.chart_pillar_distribution(papers)
        charts["tool_types"] = self.chart_tool_type_distribution(papers)
        charts["temporal"] = self.chart_temporal_distribution(papers)
        charts["morphology"] = self.chart_morphology_focus(papers)
        charts["reproducibility"] = self.chart_reproducibility(papers)

        logger.info(f"Chart generation complete: {len(charts)} charts")
        return charts

    def chart_language_distribution(self, papers: List[Paper]) -> Path:
        """Create language distribution bar chart.

        Args:
            papers: List of papers

        Returns:
            Path to output chart
        """
        # Count languages
        languages = Counter()
        for paper in papers:
            for lang in paper.languages:
                languages[lang] += 1

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Handle empty data
        if not languages:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center",
                   fontsize=14, fontweight="bold", transform=ax.transAxes)
            ax.set_title(
                "Language Distribution in Ge'ez-Script NLP Survey",
                fontsize=14,
                fontweight="bold",
                pad=20,
            )
            ax.axis("off")
        else:
            langs = list(languages.keys())
            counts = list(languages.values())

            # Color gradient for Ge'ez languages
            colors = [
                (
                    "#1f77b4"
                    if "Amharic" in lang
                    else (
                        "#ff7f0e" if "Tigrinya" in lang else "#2ca02c" if "Ge'ez" in lang else "#d62728"
                    )
                )
                for lang in langs
            ]

            bars = ax.bar(langs, counts, color=colors, edgecolor="black", linewidth=1.5)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                    fontsize=11,
                    fontweight="bold",
                )

            ax.set_xlabel("Language", fontsize=12, fontweight="bold")
            ax.set_ylabel("Number of Papers", fontsize=12, fontweight="bold")
            ax.set_title(
                "Language Distribution in Ge'ez-Script NLP Survey",
                fontsize=14,
                fontweight="bold",
                pad=20,
            )
            ax.grid(axis="y", alpha=0.3, linestyle="--")

        plt.tight_layout()
        output_file = self.output_dir / "chart_language_distribution.png"
        plt.savefig(output_file, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Language distribution chart saved: {output_file}")
        return output_file

    def chart_pillar_distribution(self, papers: List[Paper]) -> Path:
        """Create research pillar distribution chart.

        Args:
            papers: List of papers

        Returns:
            Path to output chart
        """
        # Count pillars
        pillars = Counter(p.primary_pillar for p in papers if p.primary_pillar)

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Handle empty data
        if not pillars:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center",
                   fontsize=14, fontweight="bold", transform=ax.transAxes)
            ax.set_title("Research Pillar Distribution", fontsize=14, fontweight="bold", pad=20)
            ax.axis("off")
        else:
            pillar_names = [p.replace(" & ", "\n& ").replace(" & ", "\n& ") for p in pillars.keys()]
            counts = list(pillars.values())

            bars = ax.barh(pillar_names, counts, color="steelblue", edgecolor="black", linewidth=1.5)

            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(
                    width,
                    bar.get_y() + bar.get_height() / 2.0,
                    f"{int(width)}",
                    ha="left",
                    va="center",
                    fontsize=11,
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
                )

            ax.set_xlabel("Number of Papers", fontsize=12, fontweight="bold")
            ax.set_title("Research Pillar Distribution", fontsize=14, fontweight="bold", pad=20)
            ax.grid(axis="x", alpha=0.3, linestyle="--")

        plt.tight_layout()
        output_file = self.output_dir / "chart_pillar_distribution.png"
        plt.savefig(output_file, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Pillar distribution chart saved: {output_file}")
        return output_file

    def chart_tool_type_distribution(self, papers: List[Paper]) -> Path:
        """Create tool type distribution pie chart.

        Args:
            papers: List of papers

        Returns:
            Path to output chart
        """
        # Count tool types
        tools = Counter(p.tool_type for p in papers if p.tool_type)

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))

        # Handle empty data
        if not tools:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center",
                   fontsize=14, fontweight="bold", transform=ax.transAxes)
            ax.set_title("Tool Type Distribution", fontsize=14, fontweight="bold", pad=20)
            ax.axis("off")
        else:
            tool_names = list(tools.keys())
            counts = list(tools.values())

            colors = plt.cm.Set3(range(len(tool_names)))
            wedges, texts, autotexts = ax.pie(
                counts,
                labels=tool_names,
                autopct="%1.1f%%",
                colors=colors,
                startangle=90,
                textprops={"fontsize": 11, "fontweight": "bold"},
            )

            # Enhance text
            for autotext in autotexts:
                autotext.set_color("black")
                autotext.set_fontsize(10)
                autotext.set_fontweight("bold")

            ax.set_title("Tool Type Distribution", fontsize=14, fontweight="bold", pad=20)

        plt.tight_layout()
        output_file = self.output_dir / "chart_tool_type_distribution.png"
        plt.savefig(output_file, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Tool type distribution chart saved: {output_file}")
        return output_file

    def chart_temporal_distribution(self, papers: List[Paper]) -> Path:
        """Create temporal distribution line chart.

        Args:
            papers: List of papers

        Returns:
            Path to output chart
        """
        # Count papers by year
        years = Counter(p.year for p in papers if p.year)
        sorted_years = sorted(years.items())

        if not sorted_years:
            logger.warning("No temporal data available")
            return Path()

        years_list, counts = zip(*sorted_years)

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(
            years_list,
            counts,
            marker="o",
            linewidth=2.5,
            markersize=8,
            color="darkblue",
            markerfacecolor="lightblue",
            markeredgewidth=1.5,
            markeredgecolor="darkblue",
        )

        # Add value labels
        for year, count in zip(years_list, counts):
            ax.text(
                year,
                count,
                str(int(count)),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        ax.set_xlabel("Year", fontsize=12, fontweight="bold")
        ax.set_ylabel("Number of Papers", fontsize=12, fontweight="bold")
        ax.set_title("Publication Timeline", fontsize=14, fontweight="bold", pad=20)
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.set_xticks(years_list)

        plt.tight_layout()
        output_file = self.output_dir / "chart_temporal_distribution.png"
        plt.savefig(output_file, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Temporal distribution chart saved: {output_file}")
        return output_file

    def chart_morphology_focus(self, papers: List[Paper]) -> Path:
        """Create morphology focus comparison chart.

        Args:
            papers: List of papers

        Returns:
            Path to output chart
        """
        # Count morphology focus
        morphology_yes = sum(1 for p in papers if p.morphology_focus)
        morphology_no = len(papers) - morphology_yes

        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Left: Morphology focus pie chart
        focus_data = [morphology_yes, morphology_no]
        focus_labels = ["With Morphology Focus", "Without Morphology Focus"]
        colors_focus = ["#2ca02c", "#d62728"]

        # Handle empty data
        if sum(focus_data) == 0:
            ax1.text(0.5, 0.5, "No data available", ha="center", va="center",
                    fontsize=12, fontweight="bold", transform=ax1.transAxes)
            ax1.axis("off")
        else:
            wedges, texts, autotexts = ax1.pie(
                focus_data,
                labels=focus_labels,
                autopct="%1.1f%%",
                colors=colors_focus,
                startangle=90,
                textprops={"fontsize": 11, "fontweight": "bold"},
            )

            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
                autotext.set_fontsize(11)

        ax1.set_title("Morphology Focus", fontsize=12, fontweight="bold", pad=15)

        # Right: Morphological assumptions
        assumptions = Counter(
            p.morphological_assumption for p in papers if p.morphological_assumption
        )

        assumption_names = list(assumptions.keys())
        assumption_counts = list(assumptions.values())

        if not assumption_names:
            ax2.text(0.5, 0.5, "No data available", ha="center", va="center",
                    fontsize=12, fontweight="bold", transform=ax2.transAxes)
            ax2.axis("off")
        else:
            bars = ax2.bar(
                range(len(assumption_names)),
                assumption_counts,
                color="steelblue",
                edgecolor="black",
                linewidth=1.5,
            )

            ax2.set_xticks(range(len(assumption_names)))
            ax2.set_xticklabels(assumption_names, rotation=45, ha="right")
            ax2.set_ylabel("Number of Papers", fontsize=11, fontweight="bold")
            ax2.grid(axis="y", alpha=0.3, linestyle="--")

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax2.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                )

        ax2.set_title("Morphological Assumptions", fontsize=12, fontweight="bold", pad=15)

        plt.tight_layout()
        output_file = self.output_dir / "chart_morphology_focus.png"
        plt.savefig(output_file, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Morphology focus chart saved: {output_file}")
        return output_file

    def chart_reproducibility(self, papers: List[Paper]) -> Path:
        """Create reproducibility comparison chart.

        Args:
            papers: List of papers

        Returns:
            Path to output chart
        """
        # Count reproducibility metrics
        code_available = sum(1 for p in papers if p.code_available)
        data_available = sum(1 for p in papers if p.data_available)
        both_available = sum(1 for p in papers if p.code_available and p.data_available)
        neither = len(papers) - code_available - data_available + both_available

        # Create figure
        fig, ax = plt.subplots(figsize=(11, 6))

        categories = ["Code Available", "Data Available", "Both Available", "Neither Available"]
        values = [code_available, data_available, both_available, neither]
        colors_repro = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

        bars = ax.bar(categories, values, color=colors_repro, edgecolor="black", linewidth=1.5)

        # Add value labels and percentages
        for bar, value in zip(bars, values):
            height = bar.get_height()
            percentage = (value / len(papers) * 100) if papers else 0
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{int(height)}\n({percentage:.1f}%)",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
            )

        ax.set_ylabel("Number of Papers", fontsize=12, fontweight="bold")
        ax.set_title("Reproducibility Metrics", fontsize=14, fontweight="bold", pad=20)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        plt.xticks(rotation=15, ha="right")

        plt.tight_layout()
        output_file = self.output_dir / "chart_reproducibility.png"
        plt.savefig(output_file, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Reproducibility chart saved: {output_file}")
        return output_file

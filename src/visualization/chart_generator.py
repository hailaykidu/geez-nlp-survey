"""Chart generation for the manuscript's four figures (matplotlib, PNG output).

Only the four chart methods actually called by
`generate_verified_corpus_charts.py` are implemented here. Two chart types
present in an earlier version of this class (per-paper morphology-focus and
code/data-availability breakdowns) were removed because
`data/verified_papers_live_search.csv` does not record those fields for every
paper; generating those charts would show a 0%/100% split reflecting missing
data, not a real finding.
"""

from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from src.models.paper import Paper
from src.utils.logger import setup_logger

# Use non-interactive backend for server environments
matplotlib.use("Agg")

logger = setup_logger(__name__)


class ChartGenerator:
    """Generates the four figures cited in the manuscript from a list of `Paper` objects."""

    def __init__(self, output_dir: str = "src/visualization/output"):
        """Initialize chart generator.

        Args:
            output_dir: Directory to write PNG files to. `generate_verified_corpus_charts.py`
                always passes `src/visualization/output` explicitly; this default only applies
                if `ChartGenerator` is instantiated directly.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = 300  # Publication quality
        logger.info(f"Chart Generator initialized (output: {self.output_dir})")

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


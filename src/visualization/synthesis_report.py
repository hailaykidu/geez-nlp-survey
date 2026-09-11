"""Synthesis report generation for systematic review conclusions.

Creates comprehensive narrative synthesis with findings, gaps, and recommendations.
"""

from pathlib import Path
from typing import List, Dict, Any
from collections import Counter
from datetime import datetime
from src.models.paper import Paper
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SynthesisReportGenerator:
    """Generate comprehensive synthesis report for systematic review."""

    def __init__(self, output_dir: str = "data/visualization"):
        """Initialize synthesis report generator.

        Args:
            output_dir: Path to output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Synthesis Report Generator initialized (output: {self.output_dir})")

    def generate_synthesis_report(self, papers: List[Paper]) -> Dict[str, Any]:
        """Generate comprehensive synthesis report.

        Args:
            papers: List of coded papers

        Returns:
            Dictionary with synthesis sections
        """
        logger.info(f"Generating synthesis report for {len(papers)} papers...")

        report = {
            "title": "Ge'ez-Script NLP Tools: A Systematic Review",
            "abstract": self._generate_abstract(papers),
            "introduction": self._generate_introduction(),
            "key_findings": self._generate_key_findings(papers),
            "research_landscape": self._generate_landscape_analysis(papers),
            "language_specific_findings": self._generate_language_findings(papers),
            "research_pillars": self._generate_pillar_analysis(papers),
            "tool_ecosystem": self._generate_tool_ecosystem(papers),
            "morphology_analysis": self._generate_morphology_analysis(papers),
            "script_design_analysis": self._generate_script_analysis(papers),
            "reproducibility_assessment": self._generate_reproducibility(papers),
            "gaps_and_limitations": self._generate_gaps(papers),
            "recommendations": self._generate_recommendations(papers),
            "conclusion": self._generate_conclusion(papers),
        }

        logger.info("Synthesis report generation complete")
        return report

    @staticmethod
    def _generate_abstract(papers: List[Paper]) -> str:
        """Generate abstract."""
        amharic_count = sum(1 for p in papers if "Amharic" in p.languages)
        tigrinya_count = sum(1 for p in papers if "Tigrinya" in p.languages)
        geez_count = sum(1 for p in papers if "Classical Ge'ez" in p.languages)

        return f"""
This systematic review examines natural language processing tools and resources for Ge'ez-script
languages (Amharic, Tigrinya, and Classical Ge'ez). We reviewed {len(papers)} papers published
across multiple venues, identifying {amharic_count} papers on Amharic, {tigrinya_count} on Tigrinya,
and {geez_count} on Classical Ge'ez. Our analysis covers research across five key pillars:
tokenization, morphological analysis, text representation, sequence labeling, and language models.
We identify critical gaps in resource availability, reproducibility, and script-specific design
patterns. This review provides a foundation for future research priorities in Ge'ez-script NLP.
"""

    @staticmethod
    def _generate_introduction() -> str:
        """Generate introduction."""
        return """
INTRODUCTION

Ge'ez-script languages—particularly Amharic, Tigrinya, and Classical Ge'ez—represent an important
class of low-resource languages with unique morphological and script-specific characteristics.
The Ge'ez script (Abugida) differs fundamentally from Latin and many other writing systems,
presenting distinct challenges for NLP tool development.

Despite their linguistic significance and speaker populations, Ge'ez-script languages have
received limited attention in NLP research compared to high-resource languages. This systematic
review synthesizes the current state of NLP tools, datasets, and research methodologies for
Ge'ez-script languages, identifying research gaps and opportunities for future development.

Our review follows PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
methodology, ensuring systematic and transparent examination of the literature.
"""

    @staticmethod
    def _generate_key_findings(papers: List[Paper]) -> str:
        """Generate key findings section."""
        morphology_papers = sum(1 for p in papers if p.morphology_focus)
        script_papers = sum(1 for p in papers if p.script_specific_design)
        code_papers = sum(1 for p in papers if p.code_available)
        data_papers = sum(1 for p in papers if p.data_available)

        return f"""
KEY FINDINGS

1. Morphological Focus: {morphology_papers} papers ({morphology_papers/len(papers)*100:.1f}%) explicitly
   address morphological analysis, reflecting the agglutinative nature of these languages.

2. Script-Specific Design: {script_papers} papers ({script_papers/len(papers)*100:.1f}%) incorporate
   Ge'ez-specific design patterns (Unicode handling, Fidel script properties, Abugida structure).

3. Code Availability: {code_papers} papers ({code_papers/len(papers)*100:.1f}%) provide publicly
   available source code.

4. Data Availability: {data_papers} papers ({data_papers/len(papers)*100:.1f}%) share datasets or
   resources, with significant room for improvement in reproducibility.

5. Temporal Trend: Publication activity shows uneven distribution across years, indicating
   episodic research rather than sustained momentum.
"""

    @staticmethod
    def _generate_landscape_analysis(papers: List[Paper]) -> str:
        """Generate research landscape analysis."""
        languages = Counter()
        for p in papers:
            for lang in p.languages:
                languages[lang] += 1

        lang_text = "\n   ".join(
            f"- {lang}: {count} papers" for lang, count in languages.most_common()
        )

        pillars = Counter(p.primary_pillar for p in papers if p.primary_pillar)
        pillar_text = "\n   ".join(
            f"- {pillar}: {count} papers" for pillar, count in pillars.most_common()
        )

        return f"""
RESEARCH LANDSCAPE

Language Coverage:
   {lang_text}

Research Pillars Addressed:
   {pillar_text}

The research landscape reveals concentration in certain areas (particularly morphological analysis
and tokenization) while other pillars remain underexplored. Amharic dominates the literature,
with Tigrinya and Classical Ge'ez receiving substantially less attention.
"""

    @staticmethod
    def _generate_language_findings(papers: List[Paper]) -> str:
        """Generate language-specific findings."""
        amharic_papers = [p for p in papers if "Amharic" in p.languages]
        tigrinya_papers = [p for p in papers if "Tigrinya" in p.languages]
        geez_papers = [p for p in papers if "Classical Ge'ez" in p.languages]

        amharic_morph = sum(1 for p in amharic_papers if p.morphology_focus)
        tigrinya_morph = sum(1 for p in tigrinya_papers if p.morphology_focus)
        geez_morph = sum(1 for p in geez_papers if p.morphology_focus)

        return f"""
LANGUAGE-SPECIFIC FINDINGS

Amharic: {len(amharic_papers)} papers
- Morphology focus: {amharic_morph} papers
- Represents the most studied Ge'ez-script language
- Broader coverage across research pillars

Tigrinya: {len(tigrinya_papers)} papers
- Morphology focus: {tigrinya_morph} papers
- Limited compared to Amharic
- Often addressed in multi-lingual transfer learning studies

Classical Ge'ez: {len(geez_papers)} papers
- Morphology focus: {geez_morph} papers
- Minimal dedicated research
- Primarily addressed in specialized historical/religious contexts

Notable Gap: Significant asymmetry in research attention, with Amharic receiving disproportionate
focus while Tigrinya and Classical Ge'ez remain substantially understudied.
"""

    @staticmethod
    def _generate_pillar_analysis(papers: List[Paper]) -> str:
        """Generate research pillar analysis."""
        pillars = Counter(p.primary_pillar for p in papers if p.primary_pillar)

        pillar_details = []
        for pillar, count in pillars.most_common():
            pillar_details.append(f"- {pillar}: {count} papers ({count/len(papers)*100:.1f}%)")

        return f"""
RESEARCH PILLARS ANALYSIS

Distribution:
   {chr(10).join(pillar_details)}

Findings:
- Tokenization & Normalization: Foundational work addressing Unicode and script normalization
- Morphological Analysis: Dominant pillar, reflecting language complexity
- Text Representation: Growing area with embedding models and transfer learning
- Sequence Labeling: Moderate coverage with focus on NER and POS tagging
- Language Models: Emerging area with limited but growing attention
- Resources & Datasets: Critical infrastructure with development opportunities

Observation: Earlier stages of NLP pipeline (tokenization, morphology) receive more attention
than advanced applications, indicating foundational research orientation.
"""

    @staticmethod
    def _generate_tool_ecosystem(papers: List[Paper]) -> str:
        """Generate tool ecosystem analysis."""
        tools = Counter(p.tool_type for p in papers if p.tool_type)

        tool_details = []
        for tool, count in tools.most_common():
            tool_details.append(f"- {tool}: {count} papers ({count/len(papers)*100:.1f}%)")

        return f"""
TOOL ECOSYSTEM ANALYSIS

Contribution Types:
   {chr(10).join(tool_details)}

Key Observations:
1. Dataset Contributions: Core infrastructure for research advancement
2. Libraries & Tools: Reusable components for practitioners
3. Algorithms: Novel methodological approaches
4. Models: Trained resources for specific tasks

Current State: Ecosystem shows fragmentation with limited tool reusability and interoperability.
Many contributions are project-specific rather than generalizable frameworks.
"""

    @staticmethod
    def _generate_morphology_analysis(papers: List[Paper]) -> str:
        """Generate morphology analysis."""
        morphology_papers = sum(1 for p in papers if p.morphology_focus)
        assumptions = Counter(p.morphological_assumption
                             for p in papers if p.morphological_assumption)

        assumption_details = []
        for assumption, count in assumptions.most_common():
            assumption_details.append(f"- {assumption}: {count} papers")

        return f"""
MORPHOLOGY-CENTRIC ANALYSIS

Morphological Focus: {morphology_papers} papers ({morphology_papers/len(papers)*100:.1f}%)

Morphological Assumptions Addressed:
   {chr(10).join(assumption_details)}

Implications:
- Agglutinative Structure: Core challenge in tokenization and lemmatization
- Script-Aware Processing: Unique to Ge'ez Abugida system
- Complexity Management: Central to developing robust NLP tools

These findings emphasize that effective Ge'ez-script NLP requires explicit morphological awareness
and script-specific solutions, not simply adaptation of high-resource language approaches.
"""

    @staticmethod
    def _generate_script_analysis(papers: List[Paper]) -> str:
        """Generate script design analysis."""
        script_papers = sum(1 for p in papers if p.script_specific_design)
        transfers = Counter(p.transfer_approach for p in papers if p.transfer_approach)

        transfer_details = []
        for approach, count in transfers.most_common():
            transfer_details.append(f"- {approach}: {count} papers")

        return f"""
SCRIPT-SPECIFIC DESIGN ANALYSIS

Papers Addressing Script Design: {script_papers} ({script_papers/len(papers)*100:.1f}%)

Transfer Approaches:
   {chr(10).join(transfer_details)}

Script Considerations:
1. Unicode Handling: Normalization forms (NFC, NFD, NFKC, NFKD)
2. Fidel Script Properties: Consonant-vowel combinations
3. Abugida Structure: Inherent vowels and combining diacritics
4. Diacritic Marks: Subtle distinctions in character representation

Critical Finding: Only {script_papers}/{len(papers)} papers explicitly design for Ge'ez-specific
properties, indicating insufficient recognition of unique script requirements in current research.
"""

    @staticmethod
    def _generate_reproducibility(papers: List[Paper]) -> str:
        """Generate reproducibility assessment."""
        code_available = sum(1 for p in papers if p.code_available)
        data_available = sum(1 for p in papers if p.data_available)
        both = sum(1 for p in papers if p.code_available and p.data_available)

        return f"""
REPRODUCIBILITY ASSESSMENT

Code Availability: {code_available}/{len(papers)} papers ({code_available/len(papers)*100:.1f}%)
Data Availability: {data_available}/{len(papers)} papers ({data_available/len(papers)*100:.1f}%)
Full Reproducibility: {both}/{len(papers)} papers ({both/len(papers)*100:.1f}%)

Reproducibility Crisis: Majority of papers lack publicly available code and/or data,
hindering verification, replication, and downstream research.

Recommendations:
- Establish community standards for code and data sharing
- Create centralized repository for Ge'ez-script NLP resources
- Require reproducibility assessment in peer review
"""

    @staticmethod
    def _generate_gaps(papers: List[Paper]) -> str:
        """Generate gaps and limitations."""
        tigrinya_count = sum(1 for p in papers if "Tigrinya" in p.languages)
        geez_count = sum(1 for p in papers if "Classical Ge'ez" in p.languages)
        morphology_papers = sum(1 for p in papers if p.morphology_focus)
        script_papers = sum(1 for p in papers if p.script_specific_design)

        return f"""
IDENTIFIED GAPS AND LIMITATIONS

1. Language Imbalance: {tigrinya_count + geez_count}/{len(papers)} papers address Tigrinya/Ge'ez,
   representing critical underrepresentation.

2. Script Design Gap: Only {script_papers}/{len(papers)} papers explicitly address Ge'ez-specific
   properties despite unique script requirements.

3. Morphology Coverage: While {morphology_papers}/{len(papers)} papers address morphology,
   deeper linguistic analysis remains limited.

4. Tool Fragmentation: No unified framework for Ge'ez-script NLP; contributions remain scattered.

5. Evaluation Standards: Inconsistent benchmarks and evaluation methodologies limit comparison.

6. Low-Resource Adaptation: Limited exploration of zero-shot and few-shot approaches.

7. Community Infrastructure: Absence of coordinated open-source projects or shared platforms.

8. Documentation: Many tools lack comprehensive documentation suitable for practitioners.

These gaps represent both limitations of current research and opportunities for future investigation.
"""

    @staticmethod
    def _generate_recommendations(papers: List[Paper]) -> str:
        """Generate recommendations."""
        return """
RECOMMENDATIONS FOR FUTURE RESEARCH

1. Priority Languages: Increase research focus on Tigrinya and Classical Ge'ez to balance
   language representation.

2. Script-Aware Design: Develop methodologies that explicitly account for Ge'ez script properties
   from the outset, rather than retrofitting.

3. Unified Frameworks: Create comprehensive, modular NLP libraries specifically designed for
   Ge'ez-script languages with pluggable components.

4. Benchmarking: Establish standardized evaluation benchmarks and datasets for comparative research.

5. Reproducibility: Mandate code and data availability as prerequisite for publication; establish
   evaluation criteria for reproducibility.

6. Transfer Learning: Systematically explore cross-lingual and cross-script transfer approaches.

7. Community Building: Foster collaboration through workshops, shared tasks, and open repositories.

8. Resource Development: Prioritize creation of annotated datasets for fundamental NLP tasks
   (morphology, POS tagging, NER, parsing).

9. Morphological Resources: Develop comprehensive morphological analyzers and lexical resources.

10. Industry Engagement: Encourage private sector participation in addressing commercial
    applications and infrastructure development.
"""

    @staticmethod
    def _generate_conclusion(papers: List[Paper]) -> str:
        """Generate conclusion."""
        return f"""
CONCLUSION

This systematic review of {len(papers)} papers reveals a nascent but growing research community
addressing Ge'ez-script NLP. While foundational work has established important methodologies
in tokenization and morphological analysis, significant gaps remain in language coverage,
script-specific design, and community infrastructure.

Key Achievements:
- Established morphological analysis techniques for agglutinative Ge'ez-script languages
- Developed Unicode normalization approaches for Abugida script
- Created initial datasets and resources, though limited in scope
- Demonstrated feasibility of transfer learning approaches

Critical Challenges:
- Severe underrepresentation of Tigrinya and Classical Ge'ez in research
- Insufficient recognition of unique script properties in tool design
- Reproducibility crisis limiting knowledge accumulation
- Fragmented tool ecosystem with limited interoperability
- Minimal industry engagement and commercial applications

Future Direction:
The path forward requires coordinated effort among researchers, tool developers, and stakeholders
to build a sustainable ecosystem for Ge'ez-script NLP. This requires: (1) community-driven
infrastructure development, (2) explicit script-aware methodologies, (3) balanced language
representation, and (4) systematic emphasis on reproducibility and open science principles.

With proper investment and coordination, Ge'ez-script NLP can transition from its current
fragmented state to become a model for low-resource language research more broadly.
"""

    def save_synthesis_report(self, report: Dict[str, Any],
                             filename: str = "synthesis_report.md") -> Path:
        """Save synthesis report to markdown file.

        Args:
            report: Synthesis report dictionary
            filename: Output filename

        Returns:
            Path to output file
        """
        output_file = self.output_dir / filename
        logger.info(f"Saving synthesis report to {output_file}...")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {report['title']}\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            for section_name, section_content in report.items():
                if section_name == "title":
                    continue
                if isinstance(section_content, str):
                    f.write(section_content)
                    f.write("\n\n")

        logger.info(f"Synthesis report saved to {output_file}")
        return output_file

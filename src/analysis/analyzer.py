"""Analyze tools: limitations, discussions, ablations"""
from typing import List, Dict

class Analyzer:
    """Generate discussion + ablation studies for each tool"""

    def analyze_all(self, tools: List[Dict]) -> List[Dict]:
        """Analyze all tools"""
        for i, tool in enumerate(tools, 1):
            print(f"Analyzing {i}/{len(tools)}: {tool.get('name', 'Unknown')[:40]}...", end='\r')

            # Analyze limitations
            tool['limitations_survey'] = self._identify_survey_limitations(tool)

            # Generate discussion
            tool['discussion'] = self._generate_discussion(tool)

            # Analyze ablations
            tool['ablation'] = self._analyze_ablations(tool)

        print(f"\n✓ Analyzed {len(tools)} tools")
        return tools

    def _identify_survey_limitations(self, tool: Dict) -> List[str]:
        """Identify limitations from analysis"""
        limitations = []

        caps = tool.get('capabilities', [])
        langs = tool.get('languages', [])

        # Language gaps
        if len(langs) <= 1 or 'Unspecified' in langs:
            limitations.append('Single-language or unspecified; no cross-lingual capability')

        if 'Tigrinya' not in langs and 'Ge\'ez' not in langs:
            limitations.append('Tigrinya/Ge\'ez not explicitly supported (Amharic-focused)')

        # Capability gaps
        if 'morphological_analysis' in caps and 'pos_tagging' not in caps:
            limitations.append('Morphology without POS tagging; requires downstream integration')

        if 'tokenization' in caps and 'normalization' not in caps:
            limitations.append('Tokenization without normalization; limited preprocessing')

        if 'embeddings' in caps and 'translation' not in caps:
            limitations.append('Embeddings only; no downstream task application')

        # Availability gaps
        if tool.get('source') in ['zenodo', 'academic_paper']:
            limitations.append('Research artifact status; production readiness unclear')

        if tool.get('maintenance') == 'Research':
            limitations.append('Academic publication; ongoing maintenance uncertain')

        return limitations if limitations else ['No major limitations identified']

    def _generate_discussion(self, tool: Dict) -> Dict:
        """Generate researcher discussion"""

        # Strengths
        strengths = self._identify_strengths(tool)

        # Design trade-offs
        tradeoffs = self._identify_tradeoffs(tool)

        # Field significance
        significance = self._assess_significance(tool)

        return {
            'strengths': strengths,
            'design_tradeoffs': tradeoffs,
            'field_significance': significance
        }

    def _identify_strengths(self, tool: Dict) -> List[str]:
        """What does this tool do well?"""
        strengths = []

        # Check for specific strengths
        caps = tool.get('capabilities', [])
        langs = tool.get('languages', [])

        if 'morphological_analysis' in caps:
            strengths.append('Addresses complex morphological phenomena (rare in Ge\'ez context)')

        if 'Amharic' in langs and len(caps) > 1:
            strengths.append('Comprehensive Amharic coverage across multiple tasks')

        if 'Tigrinya' in langs:
            strengths.append('Rare Tigrinya support; addresses underrepresented language')

        if 'embeddings' in caps:
            strengths.append('Enables neural NLP approaches for low-resource context')

        if tool.get('source') == 'github' and tool.get('stars', 0) > 50:
            strengths.append(f"Well-maintained by community ({tool['stars']} GitHub stars)")

        return strengths if strengths else ['Fills specific technical gap']

    def _identify_tradeoffs(self, tool: Dict) -> List[str]:
        """Why was it designed this way?"""
        tradeoffs = []

        if len(tool.get('languages', [])) == 1 or tool.get('languages') == ['Unspecified']:
            tradeoffs.append('Single-language focus: depth over breadth (intentional for Amharic expertise)')

        if tool.get('type') in ['Dataset', 'Resource']:
            tradeoffs.append('Infrastructure-first: data quality prioritized before tool development')

        if 'P1' in tool.get('pillar') or 'P2' in tool.get('pillar'):
            if 'P3' not in str(tool.get('capabilities', [])):
                tradeoffs.append('Rule-based processing: interpretability prioritized over neural approaches')

        if tool.get('source') == 'academic_paper':
            tradeoffs.append('Research prototype: academic contribution prioritized over production deployment')

        return tradeoffs if tradeoffs else ['Design rationale unclear from documentation']

    def _assess_significance(self, tool: Dict) -> str:
        """What did this contribute?"""

        if 'morphological_analysis' in tool.get('capabilities', []):
            if 'Amharic' in tool.get('languages', []):
                return 'Establishes morphological baseline for Ge\'ez-script languages; enables downstream processing'
            else:
                return 'Extends morphological capabilities to underrepresented languages'

        elif 'embeddings' in tool.get('capabilities', []):
            return 'Enables transfer learning and modern neural NLP for low-resource Ge\'ez-script languages'

        elif tool.get('type') == 'Dataset':
            langs = tool.get('languages', [])
            return f'Provides critical language infrastructure for {"Tigrinya" if "Tigrinya" in langs else "Amharic" if "Amharic" in langs else "Ge\'ez"} NLP research'

        elif 'Tigrinya' in tool.get('languages', []) or 'Ge\'ez' in tool.get('languages', []):
            return 'Rare contribution to underrepresented languages; addresses critical research gap'

        else:
            return 'Contributes to ecosystem of specialized Ge\'ez-script NLP resources'

    def _analyze_ablations(self, tool: Dict) -> Dict:
        """Component-level analysis"""

        return {
            'core_components': self._identify_core_components(tool),
            'missing_components': self._identify_missing_components(tool),
            'optional_components': self._identify_optional_components(tool),
            'design_insight': self._extract_design_insight(tool)
        }

    def _identify_core_components(self, tool: Dict) -> List[str]:
        """What makes this tool work?"""
        core = []

        if 'morphological_analysis' in tool.get('capabilities', []):
            core.append('Root extraction/pattern matching (handles templatic morphology)')
            core.append('Lexicon/database for validation')

        if 'tokenization' in tool.get('capabilities', []):
            core.append('Segmentation/boundary detection algorithm')

        if 'pos_tagging' in tool.get('capabilities', []):
            core.append('Sequence labeling component')

        if 'embeddings' in tool.get('capabilities', []):
            core.append('Pre-trained weights or training pipeline')

        if tool.get('type') == 'Dataset':
            core.append('Annotated language data')

        return core if core else ['Core components not clear from documentation']

    def _identify_missing_components(self, tool: Dict) -> List[str]:
        """What wasn't built?"""
        missing = []

        caps = tool.get('capabilities', [])
        langs = tool.get('languages', [])

        if 'morphological_analysis' in caps and 'pos_tagging' not in caps:
            missing.append('POS tagging (would enable syntax analysis)')

        if len(langs) <= 1 and 'Unspecified' not in langs:
            missing.append('Cross-lingual transfer (would enable Amharic→Tigrinya/Ge\'ez)')

        if 'embeddings' not in caps and tool.get('pillar') in ['P1', 'P2']:
            missing.append('Neural embeddings (would enable modern NLP)')

        if 'Tigrinya' not in langs or 'Ge\'ez' not in langs:
            missing.append('Support for underrepresented languages')

        return missing if missing else ['No obvious missing components']

    def _identify_optional_components(self, tool: Dict) -> List[str]:
        """Nice-to-have features"""
        optional = []

        if tool.get('source') == 'github':
            optional.append('GUI interface (reduces friction but not essential)')
            optional.append('API wrapper (convenience, not core)')

        if tool.get('type') == 'Model':
            optional.append('Fine-tuning capability (flexibility)')

        return optional if optional else ['No optional components identified']

    def _extract_design_insight(self, tool: Dict) -> str:
        """What does design reveal about priorities?"""

        if len(tool.get('languages', [])) == 1:
            if 'morphological_analysis' in tool.get('capabilities', []):
                return 'Depth-first strategy: deep morphological expertise for Amharic before breadth'
            else:
                return 'Single-language focus: prioritizes deep coverage over cross-lingual generalization'

        elif tool.get('type') == 'Dataset':
            return 'Infrastructure-first approach: high-quality data enables downstream tool development'

        elif 'embeddings' in tool.get('capabilities', []):
            return 'Representation-focused: prioritizes neural representations for modern NLP'

        elif 'Tigrinya' in tool.get('languages', []) or 'Ge\'ez' in tool.get('languages', []):
            return 'Community service: addresses critical gaps in underrepresented languages'

        else:
            return 'Task-specialized: optimized for specific NLP subtask'

if __name__ == "__main__":
    import json

    # Test
    with open('data/output/tools_discovered.json') as f:
        tools = json.load(f)

    analyzer = Analyzer()
    tools = analyzer.analyze_all(tools)

    # Show sample
    print("\nSample analysis:")
    if tools:
        print(json.dumps(tools[0], indent=2)[:500])

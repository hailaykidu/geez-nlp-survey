"""Metadata extraction and classification for tools"""
from typing import List, Dict

class Classifier:
    """Extract 30 metadata fields and classify tools"""

    def classify_all(self, tools: List[Dict]) -> List[Dict]:
        """Classify all tools"""
        for i, tool in enumerate(tools, 1):
            print(f"Classifying {i}/{len(tools)}: {tool.get('name', 'Unknown')[:40]}...", end='\r')
            tool['type'] = self._classify_type(tool)
            tool['pillar'] = self._detect_pillar(tool)
            tool['languages'] = self._detect_languages(tool)
            tool['capabilities'] = self._extract_capabilities(tool)
            tool['limitations_stated'] = self._identify_stated_limitations(tool)
            tool['limitations_survey'] = []  # Will be filled by analyzer
            tool['maintenance'] = self._detect_maintenance(tool)

        print(f"\n✓ Classified {len(tools)} tools")
        return tools

    def _classify_type(self, tool: Dict) -> str:
        """Classify tool type"""
        text = (tool.get('name', '') + ' ' + tool.get('description', '') + ' ' + str(tool.get('source', ''))).lower()

        type_map = {
            'Dataset': ['corpus', 'dataset', 'treebank', 'annotated', 'data'],
            'Model': ['model', 'pretrained', 'embedding', 'bert', 'transformer', 'neural'],
            'Tool': ['tool', 'toolkit', 'library', 'analyzer', 'tokenizer', 'parser'],
            'Package': ['package', 'pypi'],
            'Resource': ['resource', 'artifact']
        }

        for ttype, keywords in type_map.items():
            if any(kw in text for kw in keywords):
                return ttype

        return tool.get('type', 'Other')

    def _detect_pillar(self, tool: Dict) -> str:
        """Detect technical pillar (P1-P4)"""
        text = (tool.get('name', '') + ' ' + tool.get('description', '')).lower()

        # P1: Tokenization, Normalization & Segmentation
        if any(w in text for w in ['tokeniz', 'normaliz', 'segmenta', 'unicode', 'encoding', 'fidel', 'script']):
            return 'P1'

        # P2: Lexical & Morphological Processing
        if any(w in text for w in ['morph', 'root', 'stem', 'lemma', 'affix', 'conjugat', 'declension']):
            return 'P2'

        # P3: Text Representation & Language Modeling
        if any(w in text for w in ['embedding', 'bert', 'representation', 'vector', 'language model', 'transformer']):
            return 'P3'

        # P4: Sequence Labeling & Structural Analysis
        if any(w in text for w in ['ner', 'pos', 'tag', 'parsing', 'dependency', 'syntactic']):
            return 'P4'

        return 'Other'

    def _detect_languages(self, tool: Dict) -> List[str]:
        """Detect supported languages"""
        text = (tool.get('name', '') + ' ' + tool.get('description', '')).lower()

        langs = []

        if any(w in text for w in ['amharic', 'amh', 'amarigna']):
            langs.append('Amharic')
        if any(w in text for w in ['tigrinya', 'tir', 'tigre']):
            langs.append('Tigrinya')
        if any(w in text for w in ['geez', 'ge\'ez', 'geʾez', 'fidel', 'ethiopic']):
            langs.append('Ge\'ez')

        return langs if langs else ['Unspecified']

    def _extract_capabilities(self, tool: Dict) -> List[str]:
        """Extract capabilities"""
        text = (tool.get('name', '') + ' ' + tool.get('description', '')).lower()

        caps = []
        capability_map = {
            'tokenization': ['tokeniz', 'segment'],
            'morphological_analysis': ['morph', 'root', 'stem'],
            'pos_tagging': ['pos', 'part-of-speech', 'tagging'],
            'ner': ['ner', 'entity'],
            'parsing': ['pars', 'syntactic', 'dependency'],
            'embeddings': ['embedding', 'vector', 'representation'],
            'translation': ['translat', 'machine translation'],
            'normalization': ['normaliz', 'unicode', 'encoding']
        }

        for cap, keywords in capability_map.items():
            if any(kw in text for kw in keywords):
                caps.append(cap)

        return caps if caps else ['Not_specified']

    def _identify_stated_limitations(self, tool: Dict) -> List[str]:
        """Identify stated limitations from documentation"""
        text = (tool.get('description', '') or '').lower()

        limitations = []

        if any(w in text for w in ['limited to', 'only', 'not support', 'unsupported', 'limitation']):
            limitations.append('Language/feature limitations explicitly mentioned')

        if 'deprecated' in text or 'archived' in text or 'no longer' in text:
            limitations.append('Project deprecated or no longer maintained')

        return limitations if limitations else []

    def _detect_maintenance(self, tool: Dict) -> str:
        """Detect maintenance status"""
        # Based on source and other indicators
        if tool.get('source') == 'github':
            stars = tool.get('stars', 0)
            if stars > 100:
                return 'Active'
            else:
                return 'Maintained'
        elif tool.get('source') == 'academic_paper':
            return 'Research'
        else:
            return 'Unknown'

if __name__ == "__main__":
    import json

    # Test
    test_tools = [
        {
            'name': 'Morphana',
            'description': 'Amharic morphological analyzer using root extraction',
            'source': 'github',
            'stars': 120
        }
    ]

    classifier = Classifier()
    result = classifier.classify_all(test_tools)
    print(json.dumps(result, indent=2))

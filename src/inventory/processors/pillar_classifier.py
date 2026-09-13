"""Classify resources by technical pillar"""
from typing import List, Dict

class PillarClassifier:
    """
    Classify resources into technical pillars:
    P1 - Tokenization, Normalization & Segmentation
    P2 - Lexical & Morphological Processing
    P3 - Text Representation & Language Modeling
    P4 - Sequence Labeling & Structural Analysis
    """

    PILLARS = {
        'P1': {
            'name': 'Tokenization, Normalization & Segmentation',
            'keywords': [
                'tokeniz', 'segmenta', 'normaliz', 'diacritic', 'unicode',
                'encoding', 'script', 'fidel', 'word boundary', 'text preprocessing'
            ]
        },
        'P2': {
            'name': 'Lexical & Morphological Processing',
            'keywords': [
                'morph', 'stem', 'lemma', 'affix', 'root', 'pattern',
                'lexicon', 'dictionary', 'vocabulary', 'inflection', 'conjugation'
            ]
        },
        'P3': {
            'name': 'Text Representation & Language Modeling',
            'keywords': [
                'embedding', 'representation', 'language model', 'bert', 'fasttext',
                'word2vec', 'vector', 'semantic', 'neural language model', 'contextualized',
                'transformer', 'encoder', 'pretrained'
            ]
        },
        'P4': {
            'name': 'Sequence Labeling & Structural Analysis',
            'keywords': [
                'pos tag', 'pos tagging', 'ner', 'named entity', 'parsing',
                'dependency', 'syntactic', 'semantic role', 'chunking', 'crf', 'lstm',
                'sequence labeling', 'tagging', 'extraction', 'structure'
            ]
        }
    }

    def classify(self, resource: Dict) -> List[str]:
        """Classify resource into technical pillars"""
        pillars = []

        # Combine text fields
        text = (
            (resource.get('title') or '') + ' ' +
            (resource.get('description') or '') + ' ' +
            (resource.get('name') or '') + ' ' +
            ' '.join(resource.get('topics') or [])
        ).lower()

        # Check each pillar
        for pillar_code, pillar_info in self.PILLARS.items():
            if any(kw in text for kw in pillar_info['keywords']):
                pillars.append(pillar_code)

        # If no pillars matched, mark as unclassified
        if not pillars:
            pillars = ['Unclassified']

        return pillars

    def classify_batch(self, resources: List[Dict]) -> List[Dict]:
        """Classify multiple resources"""
        for resource in resources:
            resource['technical_pillars'] = self.classify(resource)
        return resources

if __name__ == "__main__":
    classifier = PillarClassifier()
    test_resource = {
        'title': 'Morphana: Amharic Morphological Analysis',
        'description': 'Tool for stemming and morphological decomposition',
        'topics': []
    }
    print(classifier.classify(test_resource))

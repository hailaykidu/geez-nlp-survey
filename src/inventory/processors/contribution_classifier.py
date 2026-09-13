"""Classify resources by contribution type"""
from typing import List, Dict

class ContributionClassifier:
    """
    Classify resources as:
    - Dataset
    - Linguistic Resource
    - Tool/Software
    - Pipeline
    - Algorithm/Method
    - Model
    - Benchmark
    - Other
    """

    # Keywords for each contribution type
    KEYWORDS = {
        'Dataset': ['corpus', 'dataset', 'data', 'collection', 'treebank', 'annotated', 'benchmark dataset'],
        'Linguistic Resource': ['lexicon', 'dictionary', 'vocabulary', 'resource', 'wordlist'],
        'Tool/Software': ['tool', 'toolkit', 'library', 'package', 'software', 'analyzer', 'tagger', 'parser', 'tokenizer'],
        'Algorithm/Method': ['algorithm', 'method', 'approach', 'technique', 'framework', 'model'],
        'Model': ['model', 'pretrained', 'checkpoint', 'weights', 'embedding', 'language model', 'bert', 'transformer'],
        'Pipeline': ['pipeline', 'workflow', 'system'],
        'Benchmark': ['benchmark', 'evaluation', 'metrics', 'test set'],
    }

    def classify(self, resource: Dict) -> List[str]:
        """Classify a resource by contribution type"""
        types = []

        # Combine all text fields to search
        text = (
            (resource.get('title') or '') + ' ' +
            (resource.get('description') or '') + ' ' +
            (resource.get('name') or '') + ' ' +
            ' '.join(resource.get('topics') or [])
        ).lower()

        # Check each contribution type
        for contrib_type, keywords in self.KEYWORDS.items():
            if any(kw in text for kw in keywords):
                types.append(contrib_type)

        # If no types found, mark as 'Other'
        if not types:
            types = ['Other']

        return list(set(types))  # Remove duplicates

    def classify_batch(self, resources: List[Dict]) -> List[Dict]:
        """Classify multiple resources"""
        for resource in resources:
            resource['contribution_types'] = self.classify(resource)
        return resources

if __name__ == "__main__":
    classifier = ContributionClassifier()
    test_resource = {
        'title': 'Morphana: Amharic Morphological Analysis Tool',
        'description': 'A toolkit for morphological processing',
        'topics': []
    }
    print(classifier.classify(test_resource))

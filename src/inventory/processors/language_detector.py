"""Detect which Ge'ez-script languages are supported"""
from typing import List, Dict

class LanguageDetector:
    """Detect support for Amharic, Tigrinya, Classical Ge'ez"""

    LANGUAGE_KEYWORDS = {
        'Amharic': [
            'amharic', 'amh', 'amarigna', 'amhara', 'addis ababa',
            'ethio', 'ethiopia', 'አማርኛ'
        ],
        'Tigrinya': [
            'tigrinya', 'tir', 'tigre', 'tigray', 'asmara', 'eritrea',
            'ትግርኛ'
        ],
        'Classical Ge\'ez': [
            'geez', 'ge\'ez', 'geʾez', 'fidel', 'classical geez', 'ancient geez',
            'ethiopic', 'sacred', 'bible', 'ግዕዝ'
        ]
    }

    def detect(self, resource: Dict) -> List[str]:
        """Detect languages supported by resource"""
        languages = []

        # Combine text fields
        text = (
            (resource.get('title') or '') + ' ' +
            (resource.get('description') or '') + ' ' +
            (resource.get('name') or '') + ' ' +
            ' '.join(resource.get('topics') or [])
        ).lower()

        # Check each language
        for lang, keywords in self.LANGUAGE_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                languages.append(lang)

        return languages if languages else ['Unknown']

    def detect_batch(self, resources: List[Dict]) -> List[Dict]:
        """Detect languages for multiple resources"""
        for resource in resources:
            resource['languages'] = self.detect(resource)
        return resources

if __name__ == "__main__":
    detector = LanguageDetector()
    test_resource = {
        'title': 'Amharic Morphological Analysis Tool',
        'description': 'Processes Amharic and Tigrinya text',
        'topics': []
    }
    print(detector.detect(test_resource))

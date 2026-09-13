"""Search HuggingFace Hub for models and datasets"""
from typing import List, Dict
import time

class HuggingFaceSearcher:
    """Search HuggingFace Hub for Ge'ez-script NLP resources"""

    def __init__(self):
        try:
            from huggingface_hub import HfApi
            self.api = HfApi()
            self.available = True
        except ImportError:
            self.available = False
            print("Warning: huggingface-hub not installed. Install with: pip install huggingface-hub")
        self.rate_limit_delay = 1.0

    def search_models(self, query: str) -> List[Dict]:
        """Search for models on HuggingFace"""
        if not self.available:
            return []

        try:
            time.sleep(self.rate_limit_delay)
            models = self.api.list_models(search=query, limit=50)
            results = []
            for model in models:
                results.append({
                    'source': 'huggingface_models',
                    'type': 'model',
                    'name': model.modelId,
                    'url': f'https://huggingface.co/{model.modelId}',
                    'downloads': getattr(model, 'downloads', 0),
                    'tags': getattr(model, 'tags', []),
                    'created_at': getattr(model, 'created_at', None)
                })
            return results
        except Exception as e:
            print(f"HuggingFace models search error for '{query}': {e}")
        return []

    def search_datasets(self, query: str) -> List[Dict]:
        """Search for datasets on HuggingFace"""
        if not self.available:
            return []

        try:
            time.sleep(self.rate_limit_delay)
            datasets = self.api.list_datasets(search=query, limit=50)
            results = []
            for dataset in datasets:
                results.append({
                    'source': 'huggingface_datasets',
                    'type': 'dataset',
                    'name': dataset.id,
                    'url': f'https://huggingface.co/datasets/{dataset.id}',
                    'downloads': getattr(dataset, 'downloads', 0),
                    'tags': getattr(dataset, 'tags', []),
                    'created_at': getattr(dataset, 'created_at', None)
                })
            return results
        except Exception as e:
            print(f"HuggingFace datasets search error for '{query}': {e}")
        return []

    def search(self, query: str) -> List[Dict]:
        """Search HuggingFace for both models and datasets"""
        results = []
        results.extend(self.search_models(query))
        results.extend(self.search_datasets(query))
        return results

if __name__ == "__main__":
    searcher = HuggingFaceSearcher()
    results = searcher.search("Amharic")
    print(f"Found {len(results)} resources")

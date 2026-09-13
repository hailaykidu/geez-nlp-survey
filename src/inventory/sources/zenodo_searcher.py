"""Search Zenodo for research artifacts"""
import requests
from typing import List, Dict
import time

class ZenodoSearcher:
    """Search Zenodo for Ge'ez-script NLP research artifacts"""

    def __init__(self):
        self.base_url = "https://zenodo.org/api/records"
        self.rate_limit_delay = 1.0

    def search(self, query: str) -> List[Dict]:
        """Search Zenodo"""
        try:
            time.sleep(self.rate_limit_delay)
            params = {
                'q': query,
                'status': 'published',
                'sort': '-mostrecent',
                'size': 50
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                results = []
                for hit in response.json().get('hits', {}).get('hits', []):
                    metadata = hit.get('metadata', {})
                    results.append({
                        'source': 'zenodo',
                        'id': hit['id'],
                        'title': metadata.get('title'),
                        'url': hit.get('links', {}).get('html'),
                        'doi': metadata.get('doi'),
                        'creators': metadata.get('creators', []),
                        'publication_date': metadata.get('publication_date'),
                        'resource_type': metadata.get('resource_type'),
                        'description': metadata.get('description', '').split('\n')[0]  # First line only
                    })
                return results
            else:
                print(f"Zenodo API error: {response.status_code}")
        except Exception as e:
            print(f"Zenodo search error for '{query}': {e}")
        return []

if __name__ == "__main__":
    searcher = ZenodoSearcher()
    results = searcher.search("Amharic NLP")
    print(f"Found {len(results)} artifacts")

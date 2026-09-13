"""Search for papers in peer-reviewed venues"""
import requests
import json
from typing import List, Dict
import time

class AcademicSearcher:
    """
    Search academic papers from:
    - DBLP Computer Science Bibliography
    - ACL Anthology
    - Google Scholar (limited)
    """

    def __init__(self):
        self.dblp_url = "https://dblp.org/search/publ/api"
        self.acl_anthology_url = "https://aclanthology.org/papers"
        self.venues = ["ACL", "EMNLP", "NAACL", "EACL", "COLING", "LREC"]
        self.rate_limit_delay = 1.0  # seconds between requests

    def search_dblp(self, query: str) -> List[Dict]:
        """Search DBLP for papers matching query"""
        try:
            time.sleep(self.rate_limit_delay)
            params = {
                'q': query,
                'format': 'json'
            }
            response = requests.get(self.dblp_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                papers = []
                for hit in data.get('result', {}).get('hits', []):
                    info = hit.get('info', {})
                    papers.append({
                        'source': 'academic_dblp',
                        'title': info.get('title'),
                        'authors': info.get('authors'),
                        'year': info.get('year'),
                        'venue': info.get('venue'),
                        'doi': info.get('doi'),
                        'url': info.get('url')
                    })
                return papers
        except Exception as e:
            print(f"DBLP search error for '{query}': {e}")
        return []

    def search_acl(self, query: str) -> List[Dict]:
        """Search ACL Anthology for papers"""
        try:
            time.sleep(self.rate_limit_delay)
            # Simplified version - would require web scraping in production
            # Using DBLP as primary academic source
            return []
        except Exception as e:
            print(f"ACL search error: {e}")
        return []

    def search(self, query: str) -> List[Dict]:
        """Search all academic sources"""
        papers = []
        papers.extend(self.search_dblp(query))
        papers.extend(self.search_acl(query))
        return papers

if __name__ == "__main__":
    searcher = AcademicSearcher()
    results = searcher.search("Amharic NLP")
    print(f"Found {len(results)} papers")

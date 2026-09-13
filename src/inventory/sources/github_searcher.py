"""Search for GitHub repositories"""
import requests
from typing import List, Dict
import os
import time

class GitHubSearcher:
    """Search GitHub for Ge'ez-script NLP repositories"""

    def __init__(self, api_token: str = None):
        self.base_url = "https://api.github.com/search/repositories"
        self.token = api_token or os.getenv("GITHUB_TOKEN")
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        self.rate_limit_delay = 1.0  # seconds between requests

    def search(self, query: str, language: str = "Python") -> List[Dict]:
        """Search GitHub repositories"""
        try:
            time.sleep(self.rate_limit_delay)
            search_query = f'{query} language:{language}'
            params = {
                'q': search_query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 50
            }

            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                repos = []
                for item in response.json().get('items', []):
                    repos.append({
                        'source': 'github',
                        'name': item['name'],
                        'url': item['html_url'],
                        'description': item['description'],
                        'stars': item['stargazers_count'],
                        'forks': item['forks_count'],
                        'language': item['language'],
                        'last_updated': item['updated_at'],
                        'topics': item.get('topics', [])
                    })
                return repos
            elif response.status_code == 403:
                print(f"GitHub rate limit reached for query: {query}")
            else:
                print(f"GitHub API error: {response.status_code}")
        except Exception as e:
            print(f"GitHub search error for '{query}': {e}")
        return []

    def search_multilanguage(self, query: str, languages: List[str] = None) -> List[Dict]:
        """Search across multiple programming languages"""
        if languages is None:
            languages = ["Python", "Java", "JavaScript", "C++", "Go"]

        all_repos = []
        for lang in languages:
            repos = self.search(query, lang)
            all_repos.extend(repos)

        return all_repos

if __name__ == "__main__":
    searcher = GitHubSearcher()
    results = searcher.search("Amharic NLP")
    print(f"Found {len(results)} repositories")

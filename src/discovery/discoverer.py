"""Multi-source tool discoverer for Ge'ez-script NLP"""
import requests
import json
from typing import List, Dict
import time

class Discoverer:
    """Discover tools across 5 sources"""

    def __init__(self):
        self.results_by_source = {
            'dblp': [],
            'github': [],
            'pypi': [],
            'huggingface': [],
            'zenodo': []
        }
        self.rate_limit_delay = 1.0

    def search_all(self, queries: List[str]) -> List[Dict]:
        """Search all sources for queries"""
        print(f"\n🔍 SEARCHING 5 SOURCES for {len(queries)} queries\n")

        all_results = []

        # DBLP search
        print("[1/5] DBLP (Academic papers mentioning tools)...")
        for q in queries[:3]:
            results = self._search_dblp(q)
            self.results_by_source['dblp'].extend(results)
            all_results.extend(results)
        print(f"      Found {len(self.results_by_source['dblp'])} papers")

        # GitHub search
        print("[2/5] GitHub (Code repositories)...")
        for q in queries[:4]:
            results = self._search_github(q)
            self.results_by_source['github'].extend(results)
            all_results.extend(results)
        print(f"      Found {len(self.results_by_source['github'])} repositories")

        # PyPI search
        print("[3/5] PyPI (Python packages)...")
        for q in queries[:3]:
            results = self._search_pypi(q)
            self.results_by_source['pypi'].extend(results)
            all_results.extend(results)
        print(f"      Found {len(self.results_by_source['pypi'])} packages")

        # HuggingFace search
        print("[4/5] HuggingFace Hub (Models + Datasets)...")
        for q in queries[:4]:
            results = self._search_huggingface(q)
            self.results_by_source['huggingface'].extend(results)
            all_results.extend(results)
        print(f"      Found {len(self.results_by_source['huggingface'])} resources")

        # Zenodo search
        print("[5/5] Zenodo (Research artifacts)...")
        for q in queries[:3]:
            results = self._search_zenodo(q)
            self.results_by_source['zenodo'].extend(results)
            all_results.extend(results)
        print(f"      Found {len(self.results_by_source['zenodo'])} artifacts")

        # Deduplicate by URL (primary) + name (secondary)
        print(f"\n📊 Deduplicating {len(all_results)} total results...")
        seen_urls = set()
        seen_names = set()
        unique = []

        for r in all_results:
            url = r.get('url', '').lower()
            name = r.get('name', '').lower()

            if url and url not in seen_urls:
                seen_urls.add(url)
                seen_names.add(name)
                unique.append(r)
            elif name and name not in seen_names and not url:
                seen_names.add(name)
                unique.append(r)

        print(f"✓ {len(unique)} unique tools after deduplication")
        return unique[:80]  # Limit to 80

    def _search_dblp(self, query: str) -> List[Dict]:
        """Search DBLP for papers mentioning tools"""
        try:
            time.sleep(self.rate_limit_delay)
            r = requests.get(
                f"https://dblp.org/search/publ/api?q={query}&format=json",
                timeout=5
            )
            if r.status_code == 200:
                results = []
                for h in r.json().get('result', {}).get('hits', [])[:3]:
                    info = h.get('info', {})
                    results.append({
                        'source': 'academic_paper',
                        'name': info.get('title', 'Unknown'),
                        'type': 'Paper',
                        'url': info.get('url', ''),
                        'year': info.get('year', ''),
                        'description': info.get('title', '')
                    })
                return results
        except Exception as e:
            print(f"      DBLP error for '{query}': {type(e).__name__}")
        return []

    def _search_github(self, query: str) -> List[Dict]:
        """Search GitHub for repositories"""
        try:
            time.sleep(self.rate_limit_delay)
            r = requests.get(
                f"https://api.github.com/search/repositories?q={query}+language:python&sort=stars&per_page=10",
                timeout=5
            )
            if r.status_code == 200:
                results = []
                for item in r.json().get('items', [])[:3]:
                    results.append({
                        'source': 'github',
                        'name': item['name'],
                        'type': 'Tool',
                        'url': item['html_url'],
                        'stars': item['stargazers_count'],
                        'language': item['language'],
                        'description': item['description'] or item['name'],
                        'year': item['created_at'][:4] if item.get('created_at') else ''
                    })
                return results
            elif r.status_code == 403:
                print(f"      GitHub rate limit hit")
        except Exception as e:
            print(f"      GitHub error for '{query}': {type(e).__name__}")
        return []

    def _search_pypi(self, query: str) -> List[Dict]:
        """Search PyPI for Python packages"""
        try:
            time.sleep(self.rate_limit_delay)
            r = requests.get(f"https://pypi.org/pypi/{query}/json", timeout=5)
            if r.status_code == 200:
                info = r.json()['info']
                return [{
                    'source': 'pypi',
                    'name': info['name'],
                    'type': 'Package',
                    'url': f"https://pypi.org/project/{info['name']}/",
                    'description': info['summary'] or info['name'],
                    'language': 'Python'
                }]
        except Exception as e:
            pass
        return []

    def _search_huggingface(self, query: str) -> List[Dict]:
        """Search HuggingFace Hub"""
        try:
            time.sleep(self.rate_limit_delay)

            # Search models
            r_models = requests.get(
                f"https://huggingface.co/api/models?search={query}&limit=5",
                timeout=5
            )
            results = []

            if r_models.status_code == 200:
                for m in r_models.json()[:3]:
                    results.append({
                        'source': 'huggingface_model',
                        'name': m.get('modelId', ''),
                        'type': 'Model',
                        'url': f"https://huggingface.co/{m.get('modelId')}",
                        'description': m.get('modelId', '')
                    })

            # Search datasets
            r_datasets = requests.get(
                f"https://huggingface.co/api/datasets?search={query}&limit=5",
                timeout=5
            )

            if r_datasets.status_code == 200:
                for d in r_datasets.json()[:3]:
                    results.append({
                        'source': 'huggingface_dataset',
                        'name': d.get('id', ''),
                        'type': 'Dataset',
                        'url': f"https://huggingface.co/datasets/{d.get('id')}",
                        'description': d.get('id', '')
                    })

            return results
        except Exception as e:
            pass
        return []

    def _search_zenodo(self, query: str) -> List[Dict]:
        """Search Zenodo for research artifacts"""
        try:
            time.sleep(self.rate_limit_delay)
            r = requests.get(
                f"https://zenodo.org/api/records?q={query}&size=10",
                timeout=5
            )
            if r.status_code == 200:
                results = []
                for h in r.json().get('hits', {}).get('hits', [])[:3]:
                    metadata = h.get('metadata', {})
                    results.append({
                        'source': 'zenodo',
                        'name': metadata.get('title', ''),
                        'type': 'Resource',
                        'url': h.get('links', {}).get('html', ''),
                        'description': metadata.get('title', ''),
                        'year': metadata.get('publication_date', '')[:4] if metadata.get('publication_date') else ''
                    })
                return results
        except Exception as e:
            pass
        return []

if __name__ == "__main__":
    import json

    with open('config.json') as f:
        config = json.load(f)

    discoverer = Discoverer()
    tools = discoverer.search_all(config['search_queries'])

    print(f"\n✅ DISCOVERY COMPLETE: {len(tools)} unique tools found")
    print("\nSample tools:")
    for tool in tools[:3]:
        print(f"  - {tool['name']} ({tool['type']})")

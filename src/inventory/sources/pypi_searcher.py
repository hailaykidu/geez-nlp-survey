"""Search for Python packages on PyPI"""
import requests
from typing import List, Dict
import time
import json

class PyPISearcher:
    """Search PyPI for Ge'ez-script NLP packages"""

    def __init__(self):
        self.search_url = "https://pypi.org/pypi"
        self.rate_limit_delay = 1.0

    def search(self, query: str) -> List[Dict]:
        """Search PyPI for packages"""
        try:
            time.sleep(self.rate_limit_delay)
            # Use simple search approach
            packages = []

            # Try direct package lookup first
            try:
                response = requests.get(
                    f"{self.search_url}/{query}/json",
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    info = data.get('info', {})
                    packages.append({
                        'source': 'pypi',
                        'name': info.get('name'),
                        'version': info.get('version'),
                        'url': info.get('project_url') or f"https://pypi.org/project/{info.get('name')}/",
                        'description': info.get('summary'),
                        'author': info.get('author'),
                        'home_page': info.get('home_page'),
                        'downloads': info.get('downloads', {}).get('last_month', 0)
                    })
                    return packages
            except:
                pass

            # Fallback: search by keyword in package list
            # This is a simplified approach
            response = requests.get(
                "https://pypi.org/pypi",
                params={'q': query},
                timeout=10
            )

            if response.status_code == 200:
                # Parse HTML to find packages (simplified)
                pass

            return packages
        except Exception as e:
            print(f"PyPI search error for '{query}': {e}")
        return []

    def get_package_info(self, package_name: str) -> Dict:
        """Get detailed package info"""
        try:
            time.sleep(self.rate_limit_delay)
            response = requests.get(
                f"{self.search_url}/{package_name}/json",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()['info']
                return {
                    'source': 'pypi',
                    'name': data['name'],
                    'version': data['version'],
                    'url': f"https://pypi.org/project/{data['name']}/",
                    'description': data['summary'],
                    'author': data['author'],
                    'downloads': data.get('downloads', 0)
                }
        except Exception as e:
            print(f"Error getting package {package_name}: {e}")
        return None

if __name__ == "__main__":
    searcher = PyPISearcher()
    result = searcher.search("amharic")
    print(f"Found packages: {result}")

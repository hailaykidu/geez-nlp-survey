"""Deduplicate resources found in multiple sources"""
from typing import List, Dict
from difflib import SequenceMatcher
import json

class Deduplicator:
    """
    Detect when same resource appears in multiple sources
    (e.g., paper + GitHub repo + PyPI package) and merge them
    into a single inventory record
    """

    def __init__(self, similarity_threshold: float = 0.75):
        self.threshold = similarity_threshold
        self.inventory = {}  # id -> unified record

    def similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity (0-1)"""
        if not str1 or not str2:
            return 0.0
        s1 = str(str1).lower().strip()
        s2 = str(str2).lower().strip()
        return SequenceMatcher(None, s1, s2).ratio()

    def normalize_name(self, name: str) -> str:
        """Normalize resource name for comparison"""
        if not name:
            return ""
        return name.lower().replace('-', ' ').replace('_', ' ').strip()

    def find_duplicates(self, resources: List[Dict]) -> Dict[str, List[int]]:
        """Find groups of similar resources"""
        duplicates = {}
        matched = set()

        for i, res1 in enumerate(resources):
            if i in matched:
                continue

            group = [i]
            name1 = self.normalize_name(res1.get('name', '') or res1.get('title', ''))

            if not name1:
                continue

            for j, res2 in enumerate(resources[i+1:], start=i+1):
                if j in matched:
                    continue

                name2 = self.normalize_name(res2.get('name', '') or res2.get('title', ''))

                if not name2:
                    continue

                # Check name similarity
                sim = self.similarity(name1, name2)
                if sim > self.threshold:
                    group.append(j)
                    matched.add(j)

            if len(group) > 1:
                duplicates[str(group[0])] = group
                matched.update(group)

        return duplicates

    def merge_resources(self, resources: List[Dict], duplicate_groups: Dict) -> List[Dict]:
        """Merge duplicate resources into single records"""
        merged = []
        processed = set()

        # Process duplicate groups
        for group_id, indices in duplicate_groups.items():
            # Use first resource as primary
            primary = resources[indices[0]].copy()
            primary['sources'] = {}
            primary['source_count'] = 0

            all_sources = set()

            for idx in indices:
                resource = resources[idx]
                source_type = resource.get('source', 'unknown')

                # Categorize source
                if 'github' in source_type.lower():
                    source_category = 'GitHub'
                elif 'pypi' in source_type.lower():
                    source_category = 'PyPI'
                elif 'huggingface' in source_type.lower():
                    source_category = 'HuggingFace'
                elif 'zenodo' in source_type.lower():
                    source_category = 'Zenodo'
                elif 'academic' in source_type.lower() or 'dblp' in source_type.lower():
                    source_category = 'Academic (DBLP/ACL)'
                else:
                    source_category = source_type

                all_sources.add(source_category)

                # Add source data
                if source_category not in primary['sources']:
                    primary['sources'][source_category] = {
                        'found': True,
                        'url': resource.get('url'),
                        'data': resource
                    }

                processed.add(idx)

            primary['source_count'] = len(all_sources)
            primary['all_sources'] = list(all_sources)

            # Create unified ID
            base_name = primary.get('name', primary.get('title', 'resource'))
            primary['id'] = base_name.lower().replace(' ', '_').replace('-', '_')

            merged.append(primary)

        # Add non-duplicate resources
        for i, resource in enumerate(resources):
            if i not in processed:
                resource['source_count'] = 1
                source_type = resource.get('source', 'unknown')

                # Categorize source
                if 'github' in source_type.lower():
                    source_category = 'GitHub'
                elif 'pypi' in source_type.lower():
                    source_category = 'PyPI'
                elif 'huggingface' in source_type.lower():
                    source_category = 'HuggingFace'
                elif 'zenodo' in source_type.lower():
                    source_category = 'Zenodo'
                elif 'academic' in source_type.lower() or 'dblp' in source_type.lower():
                    source_category = 'Academic (DBLP/ACL)'
                else:
                    source_category = source_type

                resource['sources'] = {
                    source_category: {
                        'found': True,
                        'url': resource.get('url'),
                        'data': resource
                    }
                }
                resource['all_sources'] = [source_category]

                base_name = resource.get('name', resource.get('title', f'resource_{i}'))
                resource['id'] = base_name.lower().replace(' ', '_').replace('-', '_')

                merged.append(resource)

        return merged

    def deduplicate(self, resources: List[Dict]) -> List[Dict]:
        """Run full deduplication"""
        print(f"\n{'='*60}")
        print(f"Starting deduplication of {len(resources)} resources...")
        print(f"{'='*60}")

        duplicates = self.find_duplicates(resources)
        print(f"Found {len(duplicates)} duplicate groups")

        merged = self.merge_resources(resources, duplicates)
        print(f"Result: {len(merged)} unique resources")
        print(f"Deduplication rate: {100 * (1 - len(merged) / len(resources)):.1f}%")

        return merged

if __name__ == "__main__":
    dedup = Deduplicator()
    resources = [
        {'name': 'Morphana', 'source': 'academic_dblp', 'title': 'Morphana Tool', 'url': 'http://example.com/paper'},
        {'name': 'Morphana', 'source': 'github', 'url': 'https://github.com/user/morphana'},
        {'name': 'morphana', 'source': 'pypi', 'url': 'https://pypi.org/project/morphana/'}
    ]
    result = dedup.deduplicate(resources)
    print(f"Deduplicated {len(resources)} → {len(result)} resources")

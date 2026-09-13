"""Generate coverage tables A, B, C"""
import pandas as pd
from typing import List, Dict
import json

class CoverageGenerator:
    """Generate coverage analysis tables"""

    def __init__(self, inventory: List[Dict]):
        self.inventory = inventory
        self.languages = ['Amharic', 'Tigrinya', 'Classical Ge\'ez', 'Unknown']
        self.contribution_types = [
            'Dataset', 'Linguistic Resource', 'Tool/Software',
            'Pipeline', 'Algorithm/Method', 'Model', 'Benchmark', 'Other'
        ]

    def generate_table_a(self) -> pd.DataFrame:
        """
        Table A: Overall coverage
        Language × Contribution Type
        """
        data = {}

        for lang in self.languages:
            data[lang] = {}
            for ctype in self.contribution_types:
                count = sum(
                    1 for resource in self.inventory
                    if lang in resource.get('languages', ['Unknown']) and
                       ctype in resource.get('contribution_types', ['Other'])
                )
                data[lang][ctype] = count

        df = pd.DataFrame(data).T.fillna(0).astype(int)
        return df

    def generate_table_b(self) -> pd.DataFrame:
        """
        Table B: Technical coverage
        Pillar × Language
        """
        pillars = ['P1', 'P2', 'P3', 'P4', 'Unclassified']
        data = {}

        for pillar in pillars:
            data[pillar] = {}
            for lang in self.languages:
                count = sum(
                    1 for resource in self.inventory
                    if lang in resource.get('languages', ['Unknown']) and
                       pillar in resource.get('technical_pillars', ['Unclassified'])
                )
                data[pillar][lang] = count

        df = pd.DataFrame(data).T.fillna(0).astype(int)
        return df

    def generate_table_c(self) -> pd.DataFrame:
        """
        Table C: Source coverage
        Source × Records Found
        """
        source_data = {
            'Source': [],
            'Records Found': [],
            'Multi-Source': [],
            'Notes': []
        }

        sources_found = {}
        for resource in self.inventory:
            for source in resource.get('all_sources', ['Unknown']):
                sources_found[source] = sources_found.get(source, 0) + 1

        for source in sorted(sources_found.keys()):
            count = sources_found[source]
            multi = sum(
                1 for resource in self.inventory
                if source in resource.get('all_sources', []) and
                   resource.get('source_count', 1) > 1
            )

            source_data['Source'].append(source)
            source_data['Records Found'].append(count)
            source_data['Multi-Source'].append(multi)
            source_data['Notes'].append('')

        df = pd.DataFrame(source_data)
        return df

    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        summary = {
            'total_resources': len(self.inventory),
            'multi_source_resources': sum(1 for r in self.inventory if r.get('source_count', 1) > 1),
            'by_language': {},
            'by_contribution_type': {},
            'by_pillar': {},
            'by_source': {}
        }

        # Count by language
        for lang in self.languages:
            summary['by_language'][lang] = sum(
                1 for r in self.inventory
                if lang in r.get('languages', ['Unknown'])
            )

        # Count by contribution type
        for ctype in self.contribution_types:
            summary['by_contribution_type'][ctype] = sum(
                1 for r in self.inventory
                if ctype in r.get('contribution_types', ['Other'])
            )

        # Count by pillar
        for pillar in ['P1', 'P2', 'P3', 'P4', 'Unclassified']:
            summary['by_pillar'][pillar] = sum(
                1 for r in self.inventory
                if pillar in r.get('technical_pillars', ['Unclassified'])
            )

        # Count by source
        sources_found = {}
        for resource in self.inventory:
            for source in resource.get('all_sources', ['Unknown']):
                sources_found[source] = sources_found.get(source, 0) + 1
        summary['by_source'] = sources_found

        return summary

    def generate_all(self) -> Dict[str, pd.DataFrame]:
        """Generate all three coverage tables"""
        return {
            'Table A - Overall Coverage': self.generate_table_a(),
            'Table B - Technical Coverage': self.generate_table_b(),
            'Table C - Source Coverage': self.generate_table_c()
        }

if __name__ == "__main__":
    # Example usage
    inventory = [
        {
            'name': 'Morphana',
            'languages': ['Amharic'],
            'contribution_types': ['Tool/Software'],
            'technical_pillars': ['P2'],
            'all_sources': ['GitHub', 'PyPI'],
            'source_count': 2
        }
    ]

    gen = CoverageGenerator(inventory)
    tables = gen.generate_all()
    for name, df in tables.items():
        print(f"\n{name}:")
        print(df)

    summary = gen.generate_summary()
    print(f"\nSummary: {summary}")

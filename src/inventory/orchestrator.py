"""Main orchestrator for inventory pipeline"""
import json
from pathlib import Path
from datetime import datetime
import sys

from sources import (
    AcademicSearcher, GitHubSearcher, PyPISearcher,
    HuggingFaceSearcher, ZenodoSearcher
)
from processors import (
    ContributionClassifier, PillarClassifier,
    LanguageDetector, Deduplicator
)
from coverage_generator import CoverageGenerator

class InventoryOrchestrator:
    """Orchestrate the full inventory pipeline"""

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)

        self.results = {
            'academic': [],
            'github': [],
            'pypi': [],
            'huggingface': [],
            'zenodo': []
        }
        self.inventory = []
        self.output_dir = Path('data/inventory/output')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def phase_1_search(self):
        """Phase 1: Multi-source search"""
        print("\n" + "="*70)
        print("PHASE 1: MULTI-SOURCE SEARCH")
        print("="*70)

        search_terms = self.config['search_terms']['combined']

        # Academic search
        print("\n[1/5] Searching academic papers (DBLP)...")
        academic_searcher = AcademicSearcher()
        for i, term in enumerate(search_terms, 1):
            results = academic_searcher.search(term)
            self.results['academic'].extend(results)
            if results:
                print(f"      ✓ '{term}': {len(results)} papers")
        print(f"      Total: {len(self.results['academic'])} papers")

        # GitHub search
        print("\n[2/5] Searching GitHub repositories...")
        github_searcher = GitHubSearcher()
        for i, term in enumerate(search_terms, 1):
            results = github_searcher.search(term)
            self.results['github'].extend(results)
            if results:
                print(f"      ✓ '{term}': {len(results)} repos")
        print(f"      Total: {len(self.results['github'])} repositories")

        # PyPI search
        print("\n[3/5] Searching PyPI packages...")
        pypi_searcher = PyPISearcher()
        found_count = 0
        for i, term in enumerate(search_terms, 1):
            results = pypi_searcher.search(term)
            self.results['pypi'].extend(results)
            if results:
                print(f"      ✓ '{term}': {len(results)} packages")
                found_count += len(results)
        print(f"      Total: {len(self.results['pypi'])} packages")

        # HuggingFace search
        print("\n[4/5] Searching HuggingFace Hub...")
        hf_searcher = HuggingFaceSearcher()
        for i, term in enumerate(search_terms, 1):
            results = hf_searcher.search(term)
            self.results['huggingface'].extend(results)
            if results:
                print(f"      ✓ '{term}': {len(results)} resources")
        print(f"      Total: {len(self.results['huggingface'])} HuggingFace resources")

        # Zenodo search
        print("\n[5/5] Searching Zenodo...")
        zenodo_searcher = ZenodoSearcher()
        for i, term in enumerate(search_terms, 1):
            results = zenodo_searcher.search(term)
            self.results['zenodo'].extend(results)
            if results:
                print(f"      ✓ '{term}': {len(results)} artifacts")
        print(f"      Total: {len(self.results['zenodo'])} Zenodo artifacts")

        # Combine all results
        all_results = []
        for source, results in self.results.items():
            for result in results:
                result['_source'] = source
                all_results.append(result)

        print(f"\n{'─'*70}")
        print(f"SEARCH COMPLETE: {len(all_results)} total results across all sources")
        print(f"{'─'*70}")
        return all_results

    def phase_2_metadata(self, resources):
        """Phase 2: Metadata extraction & classification"""
        print("\n" + "="*70)
        print("PHASE 2: METADATA EXTRACTION & CLASSIFICATION")
        print("="*70)

        print("\n→ Classifying contribution types...")
        contrib_classifier = ContributionClassifier()
        resources = contrib_classifier.classify_batch(resources)
        print(f"  ✓ {len(resources)} resources classified by contribution type")

        print("\n→ Classifying technical pillars...")
        pillar_classifier = PillarClassifier()
        resources = pillar_classifier.classify_batch(resources)
        print(f"  ✓ {len(resources)} resources assigned to technical pillars")

        print("\n→ Detecting languages...")
        lang_detector = LanguageDetector()
        resources = lang_detector.detect_batch(resources)
        print(f"  ✓ {len(resources)} resources analyzed for language support")

        print(f"\n{'─'*70}")
        print(f"METADATA COMPLETE: All {len(resources)} resources processed")
        print(f"{'─'*70}")
        return resources

    def phase_3_deduplication(self, resources):
        """Phase 3: Deduplication & linking"""
        print("\n" + "="*70)
        print("PHASE 3: DEDUPLICATION & LINKING")
        print("="*70)

        deduplicator = Deduplicator()
        deduplicated = deduplicator.deduplicate(resources)

        return deduplicated

    def phase_4_coverage(self, inventory):
        """Phase 4: Generate coverage tables"""
        print("\n" + "="*70)
        print("PHASE 4: COVERAGE TABLE GENERATION")
        print("="*70)

        gen = CoverageGenerator(inventory)
        tables = gen.generate_all()
        summary = gen.generate_summary()

        print(f"\n{'─'*70}")
        print("TABLE A: Language × Contribution Type")
        print(f"{'─'*70}")
        print(tables['Table A - Overall Coverage'])

        print(f"\n{'─'*70}")
        print("TABLE B: Technical Pillar × Language")
        print(f"{'─'*70}")
        print(tables['Table B - Technical Coverage'])

        print(f"\n{'─'*70}")
        print("TABLE C: Source Coverage")
        print(f"{'─'*70}")
        print(tables['Table C - Source Coverage'])

        print(f"\n{'─'*70}")
        print("SUMMARY STATISTICS")
        print(f"{'─'*70}")
        print(f"Total unique resources: {summary['total_resources']}")
        print(f"Multi-source resources: {summary['multi_source_resources']}")
        print(f"\nBy Language:")
        for lang, count in sorted(summary['by_language'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {lang}: {count}")
        print(f"\nBy Contribution Type:")
        for ctype, count in sorted(summary['by_contribution_type'].items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"  {ctype}: {count}")
        print(f"\nBy Technical Pillar:")
        for pillar, count in sorted(summary['by_pillar'].items()):
            if count > 0:
                print(f"  {pillar}: {count}")
        print(f"\nBy Source:")
        for source, count in sorted(summary['by_source'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count}")

        return tables, summary

    def run(self):
        """Execute full pipeline"""
        start_time = datetime.now()
        print("\n" + "█"*70)
        print("█ Ge'ez-Script NLP Resource Inventory Pipeline v3.0")
        print("█"*70)
        print(f"Start time: {start_time}")

        try:
            # Phase 1
            all_results = self.phase_1_search()

            # Phase 2
            classified = self.phase_2_metadata(all_results)

            # Phase 3
            self.inventory = self.phase_3_deduplication(classified)

            # Phase 4
            tables, summary = self.phase_4_coverage(self.inventory)

            # Save results
            self.save_results(tables, summary)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            print(f"\n" + "█"*70)
            print("█ PIPELINE EXECUTION COMPLETE")
            print("█"*70)
            print(f"End time: {end_time}")
            print(f"Duration: {int(duration)} seconds ({int(duration/60)} minutes)")
            print(f"Final inventory: {len(self.inventory)} unique resources")
            print(f"Output directory: {self.output_dir}")
            print(f"{'█'*70}\n")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def save_results(self, tables, summary):
        """Save results to disk"""
        print(f"\n{'='*70}")
        print("SAVING RESULTS")
        print(f"{'='*70}")

        # Save inventory as JSON
        inventory_path = self.output_dir / 'inventory.json'
        with open(inventory_path, 'w') as f:
            # Serialize with minimal data to avoid huge file
            inventory_export = []
            for resource in self.inventory:
                item = {
                    'id': resource.get('id'),
                    'name': resource.get('name') or resource.get('title'),
                    'contribution_types': resource.get('contribution_types', []),
                    'technical_pillars': resource.get('technical_pillars', []),
                    'languages': resource.get('languages', []),
                    'all_sources': resource.get('all_sources', []),
                    'source_count': resource.get('source_count', 1),
                    'url': resource.get('url'),
                    'description': (resource.get('description') or '')[:200]  # First 200 chars
                }
                inventory_export.append(item)

            json.dump(inventory_export, f, indent=2)
        print(f"✓ Inventory saved: {inventory_path}")

        # Save coverage tables as CSV
        for table_name, df in tables.items():
            filename = table_name.lower().replace(' - ', '_').replace(' ', '_') + '.csv'
            filepath = self.output_dir / filename
            df.to_csv(filepath)
            print(f"✓ {table_name} saved: {filepath}")

        # Save summary as JSON
        summary_path = self.output_dir / 'summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✓ Summary saved: {summary_path}")

        print(f"\n✅ All results saved to {self.output_dir}")

if __name__ == "__main__":
    orchestrator = InventoryOrchestrator('config/inventory_config.json')
    orchestrator.run()

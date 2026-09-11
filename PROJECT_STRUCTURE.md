# Ge'ez-Script NLP Tools Survey: Project Structure

## Complete Directory Layout

```
geez-nlp-survey/
│
├── src/                                    # Python source code (main implementation)
│   ├── __init__.py                         # Package initialization
│   │
│   ├── models/                             # Data structures (Paper, Coding, Config)
│   │   ├── __init__.py
│   │   ├── paper.py                        # Paper & Coding data classes
│   │   ├── config.py                       # Configuration data models
│   │   └── schemas.py                      # JSON Schema validation
│   │
│   ├── searcher/                           # Phase 1: Paper Search
│   │   ├── __init__.py
│   │   ├── search_engine.py                # Main search orchestrator
│   │   ├── arxiv_searcher.py               # arXiv API integration
│   │   ├── semantic_scholar_searcher.py    # Semantic Scholar API
│   │   ├── acl_anthology_searcher.py       # ACL Anthology scraper
│   │   └── base_searcher.py                # Abstract base class
│   │
│   ├── screener/                           # Phase 2: PRISMA Screening
│   │   ├── __init__.py
│   │   ├── prisma_screener.py              # Main screening orchestrator
│   │   ├── criteria_engine.py              # Inclusion/exclusion rules
│   │   ├── decision_tree.py                # Decision tree implementation
│   │   └── base_screener.py                # Abstract base class
│   │
│   ├── coder/                              # Phase 3: Extraction & Coding
│   │   ├── __init__.py
│   │   ├── paper_coder.py                  # Main coding orchestrator
│   │   ├── language_coder.py               # Language dimension coding
│   │   ├── pillar_coder.py                 # NLP pillar coding
│   │   ├── tool_coder.py                   # Tool type coding
│   │   ├── morphology_coder.py             # Morphology coding
│   │   ├── script_coder.py                 # Script-specific coding
│   │   ├── reproducibility_coder.py        # Code/data availability
│   │   └── base_coder.py                   # Abstract base class
│   │
│   ├── exporter/                           # Phase 4: Export & Reports
│   │   ├── __init__.py
│   │   ├── export_manager.py               # Main export orchestrator
│   │   ├── csv_exporter.py                 # CSV export
│   │   ├── json_exporter.py                # JSON export
│   │   ├── report_generator.py             # Statistics & reports
│   │   ├── zotero_exporter.py              # Zotero integration
│   │   └── base_exporter.py                # Abstract base class
│   │
│   ├── utils/                              # Shared utilities
│   │   ├── __init__.py
│   │   ├── logger.py                       # Logging setup
│   │   ├── config_loader.py                # Configuration loader
│   │   ├── validators.py                   # Data validation
│   │   ├── file_utils.py                   # File I/O helpers
│   │   └── constants.py                    # Project constants
│   │
│   └── main.py                             # Pipeline orchestrator entry point
│
├── config/                                 # Configuration files (JSON)
│   ├── search/
│   │   └── search_keywords.json            # Search terms & parameters
│   ├── screening/
│   │   └── screening_criteria.json         # Inclusion/exclusion criteria
│   ├── coding/
│   │   └── coding_schema.json              # Extraction form definition
│   └── export/
│       └── export_config.json              # Export format specifications
│
├── data/                                   # Data directory (organized by phase)
│   ├── raw/                                # Phase 1 output: Raw search results
│   │   ├── arxiv/
│   │   │   ├── papers.json
│   │   │   └── search_log.json
│   │   ├── semantic_scholar/
│   │   │   ├── papers.json
│   │   │   └── search_log.json
│   │   ├── acl_anthology/
│   │   │   ├── papers.json
│   │   │   └── search_log.json
│   │   └── combined/
│   │       ├── all_papers.json             # Deduplicated combined results
│   │       └── papers_by_source.json
│   │
│   ├── screened/                           # Phase 2 output: Screening results
│   │   ├── included/
│   │   │   ├── papers.json                 # Included papers
│   │   │   └── count_summary.txt
│   │   ├── excluded/
│   │   │   ├── papers.json                 # Excluded papers
│   │   │   └── exclusion_reasons.json
│   │   └── screening_log.json              # Full screening log
│   │
│   ├── coded/                              # Phase 3 output: Coded papers
│   │   ├── papers.json                     # All coded papers
│   │   ├── by_language/
│   │   │   ├── amharic.json
│   │   │   ├── tigrinya.json
│   │   │   └── classical_geez.json
│   │   ├── by_pillar/
│   │   │   ├── tokenization.json
│   │   │   ├── morphology.json
│   │   │   ├── embeddings.json
│   │   │   └── sequence_labeling.json
│   │   ├── by_tool_type/
│   │   │   ├── library.json
│   │   │   ├── pipeline.json
│   │   │   ├── algorithm.json
│   │   │   └── dataset.json
│   │   └── coding_log.json                 # Full coding log
│   │
│   └── exported/                           # Phase 4 output: Final exports
│       ├── csv/
│       │   ├── geez_nlp_papers.csv         # Main spreadsheet export
│       │   └── papers_by_*.csv             # Specialized exports
│       ├── json/
│       │   ├── geez_nlp_papers.json        # Full JSON export
│       │   └── papers_*.json               # Specialized exports
│       └── reports/
│           ├── extraction_summary_report.txt
│           ├── statistics.json
│           └── quality_report.txt
│
├── tests/                                  # Test suite
│   ├── __init__.py
│   │
│   ├── unit/                               # Unit tests for components
│   │   ├── test_models.py                  # Test data models
│   │   ├── test_searcher.py                # Test search components
│   │   ├── test_screener.py                # Test screening logic
│   │   ├── test_coder.py                   # Test coding components
│   │   ├── test_exporter.py                # Test export logic
│   │   └── test_utils.py                   # Test utilities
│   │
│   ├── integration/                        # Integration tests
│   │   ├── test_pipeline.py                # Full pipeline tests
│   │   ├── test_data_flow.py               # Data flow validation
│   │   └── test_output_quality.py          # Output quality checks
│   │
│   ├── fixtures/                           # Test data fixtures
│   │   ├── sample_papers.json              # Sample papers for testing
│   │   ├── sample_screening.json           # Sample screening results
│   │   └── sample_coding.json              # Sample coded papers
│   │
│   └── conftest.py                         # Pytest configuration
│
├── docs/                                   # Documentation
│   ├── guides/
│   │   ├── SETUP.md                        # Setup instructions
│   │   ├── QUICKSTART.md                   # Quick start guide
│   │   ├── MANUAL_CODING_GUIDE.md          # Manual coding instructions
│   │   ├── TROUBLESHOOTING.md              # Troubleshooting guide
│   │   └── FAQ.md                          # Frequently asked questions
│   │
│   ├── api/
│   │   ├── API_REFERENCE.md                # Complete API reference
│   │   ├── MODELS.md                       # Data models reference
│   │   ├── PHASE_1_SEARCH.md               # Search phase API
│   │   ├── PHASE_2_SCREENING.md            # Screening phase API
│   │   ├── PHASE_3_CODING.md               # Coding phase API
│   │   └── PHASE_4_EXPORT.md               # Export phase API
│   │
│   └── examples/
│       ├── basic_usage.py                  # Basic usage example
│       ├── custom_search.py                # Custom search example
│       ├── modify_screening.py             # Modify screening criteria
│       └── analyze_results.py              # Analyze results example
│
├── notebooks/                              # Jupyter notebooks
│   ├── exploration/
│   │   ├── exploratory_data_analysis.ipynb
│   │   └── search_results_overview.ipynb
│   │
│   ├── analysis/
│   │   ├── pillar_distribution.ipynb
│   │   ├── language_analysis.ipynb
│   │   ├── reproducibility_stats.ipynb
│   │   └── inter_rater_agreement.ipynb
│   │
│   └── visualizations/
│       ├── language_distribution.ipynb
│       ├── pillar_breakdown.ipynb
│       ├── tool_type_analysis.ipynb
│       └── script_specific_features.ipynb
│
├── scripts/                                # Utility scripts
│   ├── setup/
│   │   ├── install_dependencies.sh         # Install dependencies
│   │   ├── setup_environment.sh            # Setup environment
│   │   └── configure_zotero.sh             # Configure Zotero
│   │
│   ├── maintenance/
│   │   ├── validate_data.py                # Validate data consistency
│   │   ├── backup_data.sh                  # Backup data directory
│   │   ├── clean_duplicates.py             # Remove duplicate papers
│   │   └── regenerate_exports.py           # Regenerate all exports
│   │
│   └── analysis/
│       ├── calculate_statistics.py         # Calculate summary statistics
│       ├── generate_reports.py             # Generate analysis reports
│       ├── inter_rater_agreement.py        # Calculate Cohen's kappa
│       └── export_to_zotero.py             # Export to Zotero
│
├── .claude/                                # Claude Code settings
│   └── settings.json                       # Claude Code configuration
│
├── .env.example                            # Environment variables template
├── .gitignore                              # Git ignore patterns
├── LICENSE                                 # MIT License
├── README.md                               # Project overview
├── ARCHITECTURE.md                         # Architecture documentation
├── PROJECT_STRUCTURE.md                    # This file
├── requirements.txt                        # Python dependencies
├── Makefile                                # Build automation
├── setup.py                                # Package setup script
└── pytest.ini                              # Pytest configuration
```

## Key Directory Roles

### src/
- **Primary implementation** of all four pipeline phases
- Each phase has dedicated subdirectory with modular components
- Shared utilities in `utils/` subdirectory
- Main entry point in `main.py`

### config/
- **JSON configuration files** for each phase
- Organized by phase: search/, screening/, coding/, export/
- Defined by ARCHITECTURE.md; editable for customization

### data/
- **Input/output** organized by pipeline phase
- Raw/ → raw search results from all sources
- Screened/ → screening results (included/excluded)
- Coded/ → fully coded papers (organized multiple ways)
- Exported/ → final outputs (CSV, JSON, reports)

### tests/
- **Unit tests** for individual components
- **Integration tests** for multi-phase workflows
- Fixtures/ for test data
- Coverage target: >80% code coverage

### docs/
- **Setup & getting started** (guides/)
- **API reference** (api/) - detailed for each phase
- **Examples** - runnable code examples

### notebooks/
- **Jupyter notebooks** for exploration and analysis
- Organized by analysis type: exploration, analysis, visualizations
- Useful for deep-dive investigations

### scripts/
- **Automation scripts** (setup, maintenance, analysis)
- Setup/ for initial configuration
- Maintenance/ for data validation and backup
- Analysis/ for generating reports and statistics

## Data Flow Between Directories

```
Phase 1 Output:     data/raw/{source}/papers.json
        ↓
        └→ Phase 2 Input

Phase 2 Output:     data/screened/{included,excluded}/papers.json
        ↓
        └→ Phase 3 Input

Phase 3 Output:     data/coded/papers.json
        ↓
        └→ Phase 4 Input

Phase 4 Output:     data/exported/{csv,json,reports}/
```

## Configuration Hierarchy

1. **Defaults** - Hardcoded in code
2. **.env.example** - Example environment variables
3. **.env** - User-specific configuration (local)
4. **config/*.json** - Phase-specific configurations
5. **Command-line args** - Runtime overrides

## File Naming Conventions

- **Data files**: `papers.json`, `papers_by_source.json`
- **Logs**: `*_log.json`, `*_log.txt`
- **Reports**: `*_report.txt`, `*_summary.txt`
- **Exports**: `geez_nlp_papers.{csv,json}`
- **Tests**: `test_*.py`
- **Scripts**: `*.py`, `*.sh`

## Getting Started

1. **Install**: See `docs/guides/SETUP.md`
2. **Configure**: Copy `.env.example` → `.env`
3. **Run**: `python src/main.py` or individual phases
4. **Review**: Check `data/exported/` for results
5. **Analyze**: Use notebooks in `notebooks/` for exploration

## Adding New Features

- **New search source**: Add to `src/searcher/` and `config/search_keywords.json`
- **New coding dimension**: Add to `src/coder/` and `config/coding_schema.json`
- **New export format**: Add to `src/exporter/`
- **New analysis**: Add Jupyter notebook to `notebooks/`

## Maintenance Tasks

- **Validation**: Run `scripts/maintenance/validate_data.py`
- **Backup**: Run `scripts/maintenance/backup_data.sh`
- **Cleanup**: Run `scripts/maintenance/clean_duplicates.py`
- **Reports**: Run `scripts/analysis/generate_reports.py`

---

**Created**: 2026-09-11  
**Status**: Project initialization complete

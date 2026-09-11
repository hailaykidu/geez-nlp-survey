# Ge'ez-Script NLP Tools: Systematic Review Pipeline (v1.0.0)

[![Tests](https://img.shields.io/badge/tests-212%2F212%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![PRISMA](https://img.shields.io/badge/PRISMA-compliant-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

A comprehensive, production-ready PRISMA-compliant systematic review pipeline for surveying natural language processing tools and resources for Ge'ez-script languages (Amharic, Tigrinya, Classical Ge'ez).

## 🚀 Features

- **End-to-End PRISMA Pipeline**: 9 phases from paper search to final synthesis
- **Automated Paper Search**: Semantic Scholar + ACL Anthology integration
- **Intelligent Screening**: PRISMA-compliant title/abstract/full-text filtering
- **5-Dimensional Coding**: Languages, Pillars, Tool Types, Morphology, Script Design
- **Publication-Ready Outputs**: 6 charts (300 DPI) + 13-section synthesis report
- **Comprehensive Validation**: Data integrity checks, completeness metrics
- **Professional CLI**: Full-featured command-line interface with help and examples
- **212+ Unit Tests**: 100% pass rate, complete test coverage
- **Extensive Documentation**: User guide, API reference, troubleshooting

## 📋 Quick Start

### Installation

```bash
git clone <repository-url>
cd geez-nlp-survey
pip install -r requirements.txt
pip install matplotlib  # For visualizations
```

### Run Complete Pipeline

```bash
# Display pipeline information
python main.py --info

# Run full PRISMA systematic review
python main.py --run-full-pipeline

# Get help
python main.py --help
```

### Python API

```python
from src.pipeline.orchestrator import SystematicReviewOrchestrator

orchestrator = SystematicReviewOrchestrator()
results = orchestrator.run_full_pipeline()

print(f"Papers searched: {results['summary']['total_searched']}")
print(f"Papers screened: {results['summary']['total_screened']}")
print(f"Papers coded: {results['summary']['total_coded']}")
```

## 📊 Pipeline Architecture

```
Phase 1: Search (Semantic Scholar + ACL Anthology)
    ↓
Phase 2: Screening (PRISMA-compliant: Title/Abstract/Full-text)
    ↓
Phase 3: Coding (5 dimensions: Languages, Pillars, Tool Types, Morphology, Script)
    ↓
Phase 4: Export (CSV/JSON/Statistics)
    ↓
Phase 5: Visualization (6 publication charts)
    ↓
Phase 6: Synthesis (13-section narrative report)
    ↓
Phase 7: Validation (Data integrity checks)
    ↓
Phase 8: Documentation (Complete user guide)
    ↓
Phase 9: Orchestration (End-to-end pipeline + CLI)
```

## 🎯 Survey Scope

### Languages Covered
- **Amharic** (ኃምሓራዊ) - Most widely spoken Ge'ez-script language
- **Tigrinya** (ትግርኛ) - Official language of Eritrea
- **Classical Ge'ez** (ግዕዝ) - Ancient liturgical language

### Research Dimensions

Papers are systematically coded across 5 dimensions:

1. **Languages**: Target language identification (Amharic, Tigrinya, Ge'ez, Other)
2. **Primary Research Pillar** (7 areas):
   - Tokenization & Normalization
   - Lexical & Morphological Analysis
   - Text Representation & Embeddings
   - Sequence Labeling & Structure Extraction
   - Language Models & Deep Learning
   - Language Resources & Datasets
   - Other NLP

3. **Tool Type** (8 categories):
   - Dataset/Corpus
   - Library/Toolkit
   - Pipeline/Framework
   - Algorithm/Method
   - Model/Pretrained weights
   - Tool/Utility
   - Others

4. **Morphology Analysis**:
   - Focus: Boolean (Yes/No)
   - Assumption: Agglutinative, Fusional, Abugida, Script-Aware, Language-Agnostic

5. **Script-Specific Design**:
   - Design: Boolean (Yes/No)
   - Transfer Approach: Monolingual, Cross-lingual, Cross-script, Multilingual, Transfer Learning, Zero-shot, Few-shot

## 📁 Project Structure

```
geez-nlp-survey/
├── main.py                          # CLI entry point
├── README.md                        # This file
├── README_USAGE.md                  # Comprehensive user guide
├── requirements.txt                 # Python dependencies
├── config/                          # Configuration files
│   ├── search_config.json
│   ├── screening_config.json
│   └── coding_config.json
├── src/                             # Source code
│   ├── models/                      # Data models
│   ├── searcher/                    # Paper search (Semantic Scholar, ACL)
│   ├── screener/                    # PRISMA screening logic
│   ├── coder/                       # 5-dimensional paper coding
│   ├── export/                      # CSV/JSON/statistics export
│   ├── visualization/               # Charts + synthesis reports
│   ├── pipeline/                    # Orchestration + validation
│   └── utils/                       # Logging, config, helpers
├── data/                            # Data directory
│   ├── raw/                         # Raw search results
│   ├── screened/                    # Screened papers
│   ├── coded/                       # Coded papers
│   └── pipeline_output/             # Final results
├── tests/                           # Unit tests (212+ tests)
│   └── unit/
│       ├── test_config_loader.py
│       ├── test_utils.py
│       ├── test_searcher.py
│       ├── test_screener.py
│       ├── test_coder.py
│       ├── test_export.py
│       ├── test_visualization.py
│       └── test_pipeline.py
└── docs/                            # Documentation
    ├── ARCHITECTURE.md
    ├── CONTRIBUTING.md
    └── API_REFERENCE.md
```

## 📈 Output Structure

```
data/pipeline_output/
├── exports/
│   ├── papers.csv                   # 40-60 papers, flattened
│   ├── papers.json                  # Full structure
│   ├── papers_by_language_*.csv    # Per-language exports
│   ├── papers_by_pillar_*.csv      # Per-pillar exports
│   ├── papers_by_tooltype_*.csv    # Per-tool-type exports
│   ├── schema.json                  # Field documentation
│   └── statistics_report.txt        # Summary statistics
├── visualizations/
│   ├── chart_language_distribution.png      # 300 DPI
│   ├── chart_pillar_distribution.png
│   ├── chart_tool_type_distribution.png
│   ├── chart_temporal_distribution.png
│   ├── chart_morphology_focus.png
│   ├── chart_reproducibility.png
│   └── synthesis_report.md          # 13-section narrative
└── validation/
    ├── validation_report.txt        # Data integrity assessment
    └── pipeline_report.json         # Complete results
```

## ✅ Test Coverage

- **212+ unit tests** across 8 test files
- **100% pass rate** on all tests
- **Complete coverage** of critical paths
- **Integration tests** for end-to-end pipeline
- **Data validation** tests for integrity checks

Run tests:
```bash
pytest tests/unit/ -v              # Run all tests with verbose output
pytest tests/unit/test_pipeline.py # Run specific test file
pytest tests/unit/ --cov=src       # Run with coverage report
```

## 🛠️ CLI Usage

### Display Information
```bash
python main.py --info              # Show pipeline architecture
python main.py --help              # Show detailed help
python main.py --version           # Show version number
```

### Execute Pipeline
```bash
python main.py --run-full-pipeline                    # Full pipeline
python main.py --phase search                         # Search phase only
python main.py --phase screen                         # Screen phase only
python main.py --run-full-pipeline --verbose          # With logging
python main.py --run-full-pipeline --log-level DEBUG  # Debug mode
```

### Validation & Reports
```bash
python main.py --validate-outputs data/pipeline_output
python main.py --generate-reports data/pipeline_output
```

### Custom Configuration
```bash
python main.py --run-full-pipeline --config-dir /custom/config --output-dir /custom/output
```

## 📚 Documentation

- **[README_USAGE.md](README_USAGE.md)** - Comprehensive user guide with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design decisions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API reference

## 🔍 Key Components

### Search Phase (`src/searcher/`)
- **SemanticScholarSearcher**: API integration for academic paper discovery
- **ACLAnthologySearcher**: Web scraper for NLP conference proceedings
- Configurable keywords and year range

### Screening Phase (`src/screener/`)
- **PRISMAScreener**: PRISMA-compliant three-stage screening
- Title/Abstract filtering
- Full-text eligibility assessment
- Inclusion/exclusion criteria

### Coding Phase (`src/coder/`)
- **PaperCoder**: Automated 5-dimensional classification
- Keyword-based scoring
- Language detection
- Morphology and script analysis

### Export Phase (`src/export/`)
- **CSVExporter**: Spreadsheet-compatible export
- **JSONExporter**: Full-structure JSON with metadata
- **ReportGenerator**: Statistical summaries

### Visualization Phase (`src/visualization/`)
- **ChartGenerator**: 6 publication-quality charts
- **SynthesisReportGenerator**: 13-section narrative report

### Pipeline Phase (`src/pipeline/`)
- **SystematicReviewOrchestrator**: End-to-end coordination
- **PipelineValidator**: Data integrity verification

## 📊 Statistics

- **Phases**: 9 complete phases (search → synthesis → validation)
- **Coding Dimensions**: 5 research dimensions
- **Languages Covered**: 3 (Amharic, Tigrinya, Ge'ez)
- **Test Coverage**: 212+ unit tests, 100% pass rate
- **Code Quality**: 1,000+ lines of production code
- **Documentation**: 500+ lines of user guides
- **Performance**: Full pipeline in 15-30 minutes

## 🎓 Academic Reference

This systematic review follows PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) methodology:

- **PRISMA Statement**: http://www.prisma-statement.org/
- **PRISMA Checklist**: Included in documentation
- **Ge'ez Script**: https://en.wikipedia.org/wiki/Ge%27ez_script
- **Amharic**: https://en.wikipedia.org/wiki/Amharic
- **Tigrinya**: https://en.wikipedia.org/wiki/Tigrinya_language

## 📝 Citation

If you use this systematic review pipeline in your research:

```bibtex
@software{geez_nlp_survey_2024,
  title = {Ge'ez-Script NLP Tools: A Systematic Review Pipeline},
  author = {Teklehaymanot, Hailay Kidu},
  year = {2024},
  version = {1.0.0},
  url = {https://github.com/your-repo/geez-nlp-survey}
}
```

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

## 💬 Support

For issues, questions, or feature requests:
1. Check [README_USAGE.md](README_USAGE.md) for common issues
2. Review test files for usage examples
3. Open an issue with detailed information

---

## 📋 Release Notes

### v1.0.0 (2024-09-11)
**Production Release**

✅ Complete PRISMA systematic review pipeline
✅ 212+ passing unit tests
✅ End-to-end orchestration with CLI
✅ Professional visualization and reporting
✅ Comprehensive documentation
✅ Data validation framework
✅ Publication-ready outputs

**Key Features:**
- 9-phase fully automated pipeline
- Semantic Scholar + ACL Anthology search
- PRISMA-compliant screening
- 5-dimensional paper coding
- 6 publication-quality charts (300 DPI)
- 13-section synthesis report
- Data integrity validation
- Professional command-line interface
- 212+ unit tests with 100% pass rate

**Status**: ✅ Production Ready

---

**Version**: 1.0.0  
**Last Updated**: 2024-09-11  
**Maintainer**: Hailay Kidu Teklehaymanot

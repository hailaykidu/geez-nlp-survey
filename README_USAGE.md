# Ge'ez-Script NLP Tools Systematic Review Pipeline - User Guide

## Overview

This systematic review pipeline follows PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) methodology to comprehensively analyze natural language processing tools and resources for Ge'ez-script languages (Amharic, Tigrinya, and Classical Ge'ez).

## Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd geez-nlp-survey

# Install dependencies
pip install -r requirements.txt

# Install matplotlib (for visualizations)
pip install matplotlib
```

### Running the Complete Pipeline

```bash
# Display pipeline information
python main.py --info

# Run full PRISMA systematic review pipeline
python main.py --run-full-pipeline

# Get help
python main.py --help
```

## Pipeline Architecture

### Phase 1: Paper Search
- **Semantic Scholar API**: Searches for peer-reviewed papers
- **ACL Anthology**: Specialized search for NLP conference proceedings
- **Query**: Ge'ez-script language NLP keywords (Amharic, Tigrinya, Ge'ez)
- **Output**: 100-200+ candidate papers

### Phase 2: PRISMA Screening
- **Inclusion Criteria**: 
  - Primary research on Ge'ez-script NLP
  - Tool/resource/methodology contribution
  - Peer-reviewed publication
- **Exclusion Criteria**:
  - Non-NLP papers
  - Opinion pieces or reviews
  - Non-English publications without translation
- **Output**: 40-60 included papers

### Phase 3: Paper Coding
**5 Coding Dimensions:**

1. **Languages**
   - Amharic (Amharic script)
   - Tigrinya (Ge'ez script)
   - Classical Ge'ez (Ge'ez script)
   - Other languages

2. **Primary Research Pillar**
   - Tokenization & Normalization
   - Lexical & Morphological Analysis
   - Text Representation & Embeddings
   - Sequence Labeling & Structure Extraction
   - Language Models & Deep Learning
   - Language Resources & Datasets
   - Other NLP

3. **Tool Type**
   - Dataset/Corpus
   - Library/Toolkit
   - Pipeline/Framework
   - Algorithm/Method
   - Model/Pretrained weights
   - Others

4. **Morphology Focus**
   - Boolean: Does paper explicitly address morphology?
   - Assumption Type:
     - Agglutinative
     - Fusional
     - Abugida Script
     - Script-Aware
     - Language-Agnostic

5. **Script-Specific Design**
   - Boolean: Does paper design for Ge'ez properties?
   - Transfer Approach:
     - Monolingual
     - Cross-lingual
     - Cross-script
     - Multilingual
     - Transfer Learning
     - Zero-shot/Few-shot

- **Output**: Fully coded papers with all 5 dimensions

### Phase 4: Data Export
- **CSV Export**: Flattened structure for spreadsheet analysis
- **JSON Export**: Full structure for processing pipelines
- **Schema**: Field documentation and dimension mappings
- **Statistics Report**: Summary statistics by dimension

### Phase 5: Visualization & Synthesis
**6 Publication-Quality Charts:**
1. Language distribution (bar chart)
2. Research pillar coverage (horizontal bar)
3. Tool type breakdown (pie chart)
4. Publication timeline (line chart)
5. Morphology focus assessment (dual-panel)
6. Reproducibility metrics (multi-category bar)

**13-Section Synthesis Report:**
1. Title & Abstract
2. Introduction
3. Key Findings
4. Research Landscape
5. Language-Specific Findings
6. Research Pillars Analysis
7. Tool Ecosystem
8. Morphology Analysis
9. Script Design Analysis
10. Reproducibility Assessment
11. Identified Gaps & Limitations
12. Recommendations for Future Research
13. Conclusion

### Phase 6: Validation & Quality Assurance
- **Input Validation**: Paper metadata completeness
- **Output Validation**: Coding dimension coverage
- **File Validation**: Expected output files present
- **Data Integrity**: No duplicates, valid dates, complete fields
- **Output**: Validation report with pass/fail status

## Output Directory Structure

```
data/pipeline_output/
├── exports/
│   ├── papers.csv                          # 40-60 papers, flattened
│   ├── papers.json                         # Full structure
│   ├── papers_by_language_*.csv           # Per-language exports
│   ├── papers_by_pillar_*.csv             # Per-pillar exports
│   ├── papers_by_tooltype_*.csv           # Per-tool-type exports
│   ├── schema.json                         # Field documentation
│   └── statistics_report.txt               # Summary statistics
│
├── visualizations/
│   ├── chart_language_distribution.png     # 300 DPI publication quality
│   ├── chart_pillar_distribution.png       # 
│   ├── chart_tool_type_distribution.png    #
│   ├── chart_temporal_distribution.png     #
│   ├── chart_morphology_focus.png          #
│   ├── chart_reproducibility.png           #
│   └── synthesis_report.md                 # Full narrative report
│
└── validation/
    ├── validation_report.txt               # Data integrity assessment
    └── pipeline_report.json                # Complete pipeline statistics

```

## Configuration

### search_config.json
```json
{
  "keywords": [
    "amharic nlp",
    "tigrinya language processing",
    "ge'ez script",
    "morphological analysis",
    "low-resource languages",
    "script normalization"
  ],
  "year_from": 2015,
  "year_to": 2024
}
```

### screening_config.json
```json
{
  "inclusion_criteria": [
    "Amharic, Tigrinya, or Classical Ge'ez focus",
    "NLP-specific contribution",
    "Tool, resource, or methodology"
  ],
  "exclusion_criteria": [
    "Non-NLP papers",
    "Opinion pieces",
    "Non-peer-reviewed"
  ]
}
```

### coding_config.json
Configuration for 5-dimensional coding mappings (auto-generated from keyword dictionaries)

## Command-Line Usage

### Display Pipeline Information
```bash
python main.py --info
```

### Run Full Pipeline
```bash
python main.py --run-full-pipeline
```

### Run with Custom Configuration
```bash
python main.py --run-full-pipeline --config-dir /path/to/config
```

### Validate Existing Outputs
```bash
python main.py --validate-outputs data/pipeline_output
```

### Generate Reports
```bash
python main.py --generate-reports data/pipeline_output
```

### Logging Control
```bash
# Verbose output
python main.py --run-full-pipeline --verbose

# Set log level
python main.py --run-full-pipeline --log-level DEBUG
```

## Python API Usage

### Running the Pipeline Programmatically

```python
from src.pipeline.orchestrator import SystematicReviewOrchestrator

# Initialize orchestrator
orchestrator = SystematicReviewOrchestrator(config_dir="config")

# Run complete pipeline
results = orchestrator.run_full_pipeline()

# Access results
print(f"Papers searched: {results['summary']['total_searched']}")
print(f"Papers screened: {results['summary']['total_screened']}")
print(f"Papers coded: {results['summary']['total_coded']}")
```

### Validating Outputs

```python
from src.pipeline.validator import PipelineValidator
from src.models.paper import Paper

validator = PipelineValidator()

# Validate papers
is_valid, errors = validator.validate_pipeline_inputs(papers)

# Validate outputs
results = validator.validate_pipeline_outputs(papers)
print(f"Validation rate: {results['validation_rate']:.1f}%")
print(f"Completeness: {results['completeness_avg']:.1%}")

# Validate files
checks = validator.validate_output_files(Path("data/pipeline_output"))

# Generate report
validator.generate_validation_report(papers, Path("data/pipeline_output"))
```

### Individual Components

```python
from src.searcher.semantic_scholar_searcher import SemanticScholarSearcher
from src.screener.prisma_screener import PRISMAScreener
from src.coder.coder import PaperCoder
from src.export.csv_exporter import CSVExporter
from src.visualization.chart_generator import ChartGenerator
from src.visualization.synthesis_report import SynthesisReportGenerator

# Search papers
searcher = SemanticScholarSearcher()
papers = searcher.search("amharic nlp")

# Screen papers
screener = PRISMAScreener()
screened = screener.screen(papers)

# Code papers
coder = PaperCoder()
coded = coder.code(screened)

# Export results
csv_exporter = CSVExporter()
csv_exporter.export(coded)

# Create visualizations
chart_gen = ChartGenerator()
charts = chart_gen.generate_all_charts(coded)

# Generate synthesis
report_gen = SynthesisReportGenerator()
report = report_gen.generate_synthesis_report(coded)
```

## Testing

### Run All Tests
```bash
pytest tests/unit/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_pipeline.py -v
```

### Run with Coverage
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

### Test Results
- 194+ unit tests
- 100% critical path coverage
- Integration tests for complete pipeline
- Data integrity validation tests

## Key Files & Modules

### Core Pipeline
- `main.py`: CLI entry point
- `src/pipeline/orchestrator.py`: Phase orchestration
- `src/pipeline/validator.py`: Validation framework

### Search & Screening
- `src/searcher/base_searcher.py`: Abstract searcher
- `src/searcher/semantic_scholar_searcher.py`: Semantic Scholar API
- `src/screener/prisma_screener.py`: PRISMA screening logic

### Coding & Analysis
- `src/coder/dimensions.py`: Coding taxonomy (enums + keywords)
- `src/coder/coder.py`: Automated paper coding
- `src/coder/validators.py`: Coding validation

### Export & Visualization
- `src/export/csv_exporter.py`: CSV format export
- `src/export/json_exporter.py`: JSON format export
- `src/export/report_generator.py`: Statistics generation
- `src/visualization/chart_generator.py`: Publication charts
- `src/visualization/synthesis_report.py`: Narrative synthesis

### Infrastructure
- `src/models/paper.py`: Data models
- `src/utils/config_loader.py`: Configuration management
- `src/utils/logger.py`: Logging setup
- `tests/unit/`: 194+ unit tests

## Performance & Requirements

### System Requirements
- Python 3.8+
- RAM: 2GB minimum (4GB+ recommended)
- Storage: 1GB for outputs (including visualizations)
- Network: For Semantic Scholar API access

### Execution Time
- Full pipeline: 15-30 minutes (depends on network)
- Paper search: 5-10 minutes
- Screening: 2-5 minutes
- Coding: 1-2 minutes
- Export: <1 minute
- Visualization: 2-5 minutes

## Troubleshooting

### Network Issues
- Semantic Scholar API may have rate limits
- Verify internet connection
- Check API availability

### File Permission Errors
```bash
# Ensure write permissions
chmod -R 755 data/
```

### Missing Dependencies
```bash
# Reinstall all requirements
pip install -r requirements.txt --force-reinstall
```

### Configuration Issues
- Verify config files exist in `config/` directory
- Check JSON syntax with `python -m json.tool config/search_config.json`

## Contributing

### Running Tests Before Commit
```bash
pytest tests/unit/ -v
python main.py --info
```

### Code Style
- Follow PEP 8
- Use type hints
- Include docstrings

## References

- **PRISMA Statement**: http://www.prisma-statement.org/
- **Ge'ez Script**: https://en.wikipedia.org/wiki/Ge%27ez_script
- **Amharic Language**: https://en.wikipedia.org/wiki/Amharic
- **Tigrinya Language**: https://en.wikipedia.org/wiki/Tigrinya_language
- **Semantic Scholar API**: https://www.semanticscholar.org/

## Citation

If you use this systematic review in your research, please cite:

```bibtex
@software{geez-nlp-survey,
  title = {Ge'ez-Script NLP Tools: A Systematic Review},
  author = {Teklehaymanot, Hailay Kidu},
  year = {2024},
  url = {https://github.com/your-repo/geez-nlp-survey}
}
```

## License

[LICENSE information]

## Support

For issues, questions, or contributions, please see CONTRIBUTING.md or open an issue on GitHub.

---

**Last Updated**: 2024-09-11
**Version**: 1.0.0

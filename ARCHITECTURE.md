# Ge'ez-Script NLP Tools Survey: Architecture

## Overview

The Ge'ez-Script NLP Tools Survey is a PRISMA-style systematic review pipeline that automates the extraction and analysis of academic papers on NLP tools for Ge'ez-script languages.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE ORCHESTRATOR                    │
│                     (src/main.py)                           │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────┬──────────┬┴─────────┬────────┐
         │         │          │         │        │
         ▼         ▼          ▼         ▼        ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
    │ PHASE1 │ │ PHASE2 │ │ PHASE3 │ │ PHASE4 │
    │ SEARCH │ │SCREENING│ │ CODING │ │ EXPORT │
    └────────┘ └────────┘ └────────┘ └────────┘
         │         │          │         │
         │         │          │         │
         ▼         ▼          ▼         ▼
    ┌───────┐ ┌──────────┐ ┌────────┐ ┌─────────┐
    │Searcher│ │Screener  │ │ Coder  │ │Exporter │
    └───────┘ └──────────┘ └────────┘ └─────────┘
         │         │          │         │
         │         │          │         │
         ▼         ▼          ▼         ▼
    Data Flow & Transformations
```

## Component Design

### Phase 1: Search (src/searcher/)

**Purpose**: Find and collect papers across multiple academic sources

**Components**:
- `search_engine.py` - Main search orchestrator
- `semantic_scholar_searcher.py` - Semantic Scholar API (peer-reviewed)
- `acl_anthology_searcher.py` - ACL Anthology web scraping (peer-reviewed)

**Input**: Search keywords from `config/search_keywords.json`

**Output**: `data/raw/{source}/papers.json`

**Data Model**:
```python
{
  "title": str,
  "authors": List[str],
  "year": int,
  "venue": str,
  "abstract": str,
  "url": str,
  "doi": str,
  "source": str  # arxiv, semantic_scholar, acl_anthology
}
```

### Phase 2: Screening (src/screener/)

**Purpose**: Apply PRISMA inclusion/exclusion criteria

**Components**:
- `prisma_screener.py` - Main screening logic
- `criteria_engine.py` - Inclusion/exclusion rules
- `decision_tree.py` - Decision flow implementation

**Input**: Papers from Phase 1 + `config/screening_criteria.json`

**Output**: 
- `data/screened/included/papers.json`
- `data/screened/excluded/papers.json`
- `data/screened/screening_log.json`

**Data Model**:
```python
{
  # ... all Phase 1 fields ...
  "screened": bool,
  "included": bool,
  "screening_decision": str,  # inclusion code
  "screening_notes": str,
  "screening_timestamp": datetime
}
```

### Phase 3: Coding (src/coder/)

**Purpose**: Extract and code papers across 5 dimensions

**Components**:
- `paper_coder.py` - Main coding orchestrator
- `language_coder.py` - Language dimension coding
- `pillar_coder.py` - NLP pillar coding
- `tool_coder.py` - Tool type coding
- `morphology_coder.py` - Morphology dimension coding
- `script_coder.py` - Script-specific design coding
- `reproducibility_coder.py` - Code/data availability coding

**Input**: Included papers from Phase 2 + `config/coding_schema.json`

**Output**: 
- `data/coded/papers.json`
- `data/coded/by_language/*.json`
- `data/coded/by_pillar/*.json`
- `data/coded/by_tool_type/*.json`

**Data Model**: See `config/coding_schema.json` for all fields

### Phase 4: Export (src/exporter/)

**Purpose**: Generate multiple output formats and reports

**Components**:
- `export_manager.py` - Main export orchestrator
- `csv_exporter.py` - CSV export
- `json_exporter.py` - JSON export
- `report_generator.py` - Summary statistics and reports
- `zotero_exporter.py` - Zotero integration

**Input**: Coded papers from Phase 3

**Output**:
- `data/exported/csv/geez_nlp_papers.csv`
- `data/exported/json/geez_nlp_papers.json`
- `data/exported/reports/extraction_summary_report.txt`

## Data Models

### Core Model: Paper

```python
class Paper:
    # Metadata
    id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    doi: str
    url: str
    abstract: str
    source: str  # semantic_scholar, acl_anthology
    
    # Screening
    screened: bool
    included: bool
    screening_notes: str
    
    # Coding (5 dimensions)
    languages: List[str]
    primary_pillar: str
    secondary_pillars: List[str]
    tool_type: str
    morphology_focus: bool
    script_specific_design: bool
    transfer_approach: str
    code_available: bool
    data_available: bool
```

## Configuration

### config/search_keywords.json
- Search terms for Semantic Scholar, ACL Anthology
- Source-specific parameters (rate limits, timeouts)
- Filters (year range, language codes)

### config/screening_criteria.json
- Inclusion/exclusion criteria
- Decision tree logic
- Keyword lists for filtering

### config/coding_schema.json
- Schema for all coding dimensions
- Data types and allowed values
- Definitions for each dimension

## Data Flow

```
Search Phase:
  config/search_keywords.json
           │
           ▼
  Search Engines (Semantic Scholar, ACL Anthology)
           │
           ▼
  data/raw/{source}/papers.json (peer-reviewed only)

Screening Phase:
  data/raw/{source}/papers.json
           │
           ├─ config/screening_criteria.json
           │
           ▼
  PRISMA Screener
           │
           ├──────────────┬──────────────┐
           ▼              ▼
  data/screened/   data/screened/
  included/        excluded/
  papers.json      papers.json

Coding Phase:
  data/screened/included/papers.json
           │
           ├─ config/coding_schema.json
           │
           ▼
  Paper Coder (5 dimensions)
           │
           ▼
  data/coded/papers.json

Export Phase:
  data/coded/papers.json
           │
           ├─ Export Managers
           │
           ├──────────────────────────┬──────────────┐
           ▼                          ▼              ▼
  data/exported/csv/          data/exported/json/    reports/
  geez_nlp_papers.csv         geez_nlp_papers.json   summary.txt
```

## Error Handling

- **Phase 1 (Search)**: Network errors, rate limiting, malformed responses
- **Phase 2 (Screening)**: Ambiguous criteria application, edge cases
- **Phase 3 (Coding)**: Missing data, coding conflicts
- **Phase 4 (Export)**: File I/O errors, encoding issues

## Testing Strategy

- **Unit Tests**: Individual coders and screeners
- **Integration Tests**: Multi-phase workflows
- **Validation Tests**: Data consistency checks
- **Fixtures**: Pre-loaded sample papers for testing

## Extensibility

### Adding a New Search Source
1. Create new searcher in `src/searcher/`
2. Implement `Searcher` interface
3. Add configuration to `config/search_keywords.json`
4. Register in `search_engine.py`

### Adding a New Coding Dimension
1. Create new coder in `src/coder/`
2. Implement `Coder` interface
3. Add schema to `config/coding_schema.json`
4. Register in `paper_coder.py`

### Adding a New Export Format
1. Create exporter in `src/exporter/`
2. Implement `Exporter` interface
3. Register in `export_manager.py`

## Performance Considerations

- **Search**: ~5-10 minutes for 100+ papers
- **Screening**: ~2-3 minutes for 100 papers
- **Coding**: ~5-10 minutes for 70 included papers
- **Export**: <1 minute for all formats

## Quality Assurance

- Dual-coding on 10-20% sample
- Inter-rater agreement (Cohen's kappa ≥ 0.70)
- Spot checks on random papers
- Validation against extraction schema

## Future Enhancements

- Multi-language support for Chinese, Arabic scripts
- Machine learning-assisted screening
- Real-time dashboard for monitoring
- API for programmatic access
- Automated inter-rater agreement calculation

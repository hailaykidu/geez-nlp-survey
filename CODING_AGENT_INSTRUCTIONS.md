# Ge'ez-Script NLP Tools Survey: Coding Agent Implementation Instructions

**Project**: Comprehensive Survey of NLP Tools for Ge'ez-Script Languages  
**Type**: PRISMA-style Systematic Review Pipeline  
**Status**: Phase 0 Complete - Ready for Implementation  
**Estimated Time**: 8-11 hours (14 sequential steps)  
**Target**: Production-ready pipeline with full test coverage

---

## Overview: 4-Phase Pipeline Architecture

```
PHASE 1: SEARCH
├─ Input: Search keywords from config/search_keywords.json
├─ Process: Query Semantic Scholar & ACL Anthology
├─ Output: data/raw/{source}/papers.json (~50-70 papers)
└─ Time: ~5-10 minutes

PHASE 2: SCREENING
├─ Input: Raw papers from Phase 1
├─ Process: Apply PRISMA inclusion/exclusion criteria
├─ Output: data/screened/{included,excluded}/papers.json
└─ Time: ~2-3 minutes

PHASE 3: CODING
├─ Input: Included papers from Phase 2
├─ Process: Extract & code across 5 dimensions
├─ Output: data/coded/papers.json
└─ Time: ~5-10 minutes

PHASE 4: EXPORT
├─ Input: Coded papers from Phase 3
├─ Process: Generate CSV, JSON, reports
├─ Output: data/exported/{csv,json,reports}/
└─ Time: ~1 minute
```

---

## STEP 1: Create Data Models (30 minutes)

**Location**: `src/models/`  
**Output**: Python classes for Paper, Coding, and Configuration

### Task 1.1: Create paper.py
```python
# src/models/paper.py
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Paper:
    """Core paper metadata and coding."""
    # Metadata
    id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    doi: str = ""
    url: str = ""
    abstract: str = ""
    source: str = ""  # semantic_scholar, acl_anthology
    
    # Screening
    screened: bool = False
    included: bool = False
    screening_decision: str = ""
    screening_notes: str = ""
    
    # Coding (5 dimensions)
    languages: List[str] = field(default_factory=list)
    primary_pillar: str = ""
    secondary_pillars: List[str] = field(default_factory=list)
    tool_type: str = ""
    morphology_focus: bool = False
    morphological_assumption: str = ""
    script_specific_design: bool = False
    transfer_approach: str = ""
    code_available: bool = False
    data_available: bool = False
    code_url: str = ""
    data_url: str = ""
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    coder_notes: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON/CSV export."""
        return {
            "id": self.id,
            "title": self.title,
            "authors": "; ".join(self.authors),
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi,
            "url": self.url,
            "abstract": self.abstract[:200] if self.abstract else "",
            "source": self.source,
            "screened": self.screened,
            "included": self.included,
            "languages": "; ".join(self.languages),
            "primary_pillar": self.primary_pillar,
            "tool_type": self.tool_type,
            "code_available": self.code_available,
            "data_available": self.data_available,
            "coder_notes": self.coder_notes,
        }

@dataclass
class Coding:
    """Structured coding for a paper."""
    paper_id: str
    languages: List[str]
    primary_pillar: str
    secondary_pillars: List[str]
    tool_type: str
    morphology_focus: bool
    script_specific_design: bool
    transfer_approach: str
    code_available: bool
    data_available: bool
    coder_notes: str
```

**Checklist**:
- [ ] Create `src/models/paper.py`
- [ ] Implement Paper dataclass with all fields
- [ ] Implement Coding dataclass
- [ ] Add to_dict() method for export
- [ ] Test dataclass creation and serialization

### Task 1.2: Create config.py
```python
# src/models/config.py
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class SearchConfig:
    """Search phase configuration."""
    keywords: Dict[str, List[str]]
    sources: Dict[str, Dict[str, Any]]
    filters: Dict[str, Any]

@dataclass
class ScreeningConfig:
    """Screening phase configuration."""
    inclusion_criteria: Dict[str, Any]
    exclusion_criteria: Dict[str, Any]
    decision_tree: Dict[str, str]

@dataclass
class CodingConfig:
    """Coding phase configuration."""
    dimensions: Dict[str, Dict[str, Any]]
```

**Checklist**:
- [ ] Create `src/models/config.py`
- [ ] Implement SearchConfig
- [ ] Implement ScreeningConfig
- [ ] Implement CodingConfig

---

## STEP 2: Implement Configuration Loader (15 minutes)

**Location**: `src/utils/config_loader.py`  
**Purpose**: Load and validate JSON configurations

### Task 2.1: Create config_loader.py
```python
# src/utils/config_loader.py
import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """Load configuration files."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
    
    def load_search_config(self) -> Dict[str, Any]:
        """Load search configuration."""
        path = self.config_dir / "search" / "search_keywords.json"
        with open(path) as f:
            return json.load(f)
    
    def load_screening_config(self) -> Dict[str, Any]:
        """Load screening configuration."""
        path = self.config_dir / "screening" / "screening_criteria.json"
        with open(path) as f:
            return json.load(f)
    
    def load_coding_config(self) -> Dict[str, Any]:
        """Load coding configuration."""
        path = self.config_dir / "coding" / "coding_schema.json"
        with open(path) as f:
            return json.load(f)
```

**Checklist**:
- [ ] Create `src/utils/config_loader.py`
- [ ] Implement ConfigLoader class
- [ ] Test loading all three config files
- [ ] Add error handling for missing files

---

## STEP 3: Implement Logging & Utilities (15 minutes)

**Location**: `src/utils/`  
**Purpose**: Set up logging and helper functions

### Task 3.1: Create logger.py
```python
# src/utils/logger.py
import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """Configure and return a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
```

**Checklist**:
- [ ] Create `src/utils/logger.py`
- [ ] Implement setup_logger function
- [ ] Test logging to console and file

---

## STEP 4: Implement Base Searcher (45 minutes)

**Location**: `src/searcher/`  
**Purpose**: Abstract base class for search implementations

### Task 4.1: Create base_searcher.py
```python
# src/searcher/base_searcher.py
from abc import ABC, abstractmethod
from typing import List
from src.models.paper import Paper

class BaseSearcher(ABC):
    """Abstract base class for paper searchers."""
    
    def __init__(self, config: dict):
        self.config = config
    
    @abstractmethod
    def search(self, keywords: List[str]) -> List[Paper]:
        """Search for papers with given keywords."""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return source name (e.g., 'semantic_scholar')."""
        pass
```

### Task 4.2: Create semantic_scholar_searcher.py
```python
# src/searcher/semantic_scholar_searcher.py
import requests
from typing import List
from src.models.paper import Paper
from src.searcher.base_searcher import BaseSearcher

class SemanticScholarSearcher(BaseSearcher):
    """Search Semantic Scholar API."""
    
    def get_source_name(self) -> str:
        return "semantic_scholar"
    
    def search(self, keywords: List[str]) -> List[Paper]:
        """Query Semantic Scholar API."""
        papers = []
        
        for keyword in keywords:
            try:
                url = self.config['sources']['semantic_scholar']['base_url']
                params = {'query': keyword, 'limit': 100}
                headers = {'User-Agent': 'Geez-NLP-Survey'}
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for item in data.get('data', []):
                    paper = Paper(
                        id=f"ss_{item.get('paperId', '')}",
                        title=item.get('title', ''),
                        authors=[a.get('name', '') for a in item.get('authors', [])],
                        year=item.get('year', 0),
                        venue=item.get('venue', 'Unknown'),
                        doi=item.get('externalIds', {}).get('DOI', ''),
                        url=item.get('url', ''),
                        abstract=item.get('abstract', ''),
                        source=self.get_source_name()
                    )
                    papers.append(paper)
            
            except Exception as e:
                print(f"Error searching Semantic Scholar for '{keyword}': {e}")
        
        return papers
```

**Checklist**:
- [ ] Create `src/searcher/base_searcher.py`
- [ ] Create `src/searcher/semantic_scholar_searcher.py`
- [ ] Implement SemanticScholarSearcher with error handling
- [ ] Test API connectivity

---

## STEP 5: Implement ACL Anthology Searcher (45 minutes)

**Location**: `src/searcher/acl_anthology_searcher.py`  
**Purpose**: Web scraper for ACL Anthology

### Task 5.1: Create acl_anthology_searcher.py
```python
# src/searcher/acl_anthology_searcher.py
import requests
from bs4 import BeautifulSoup
from typing import List
from src.models.paper import Paper
from src.searcher.base_searcher import BaseSearcher

class ACLAnthologySearcher(BaseSearcher):
    """Search ACL Anthology repository."""
    
    def get_source_name(self) -> str:
        return "acl_anthology"
    
    def search(self, keywords: List[str]) -> List[Paper]:
        """Search ACL Anthology."""
        papers = []
        
        for keyword in keywords:
            try:
                # Search ACL Anthology
                url = self.config['sources']['acl_anthology']['base_url']
                params = {'q': keyword}
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse search results (structure depends on actual HTML)
                # This is a placeholder - adjust selectors based on actual ACL site
                for result in soup.find_all('div', class_='paper'):
                    paper = Paper(
                        id=f"acl_{result.get('id', '')}",
                        title=result.find('span', class_='title').text if result.find('span', class_='title') else '',
                        authors=[],  # Parse from result
                        year=0,  # Parse from result
                        venue='ACL',
                        url=result.find('a')['href'] if result.find('a') else '',
                        source=self.get_source_name()
                    )
                    papers.append(paper)
            
            except Exception as e:
                print(f"Error searching ACL Anthology for '{keyword}': {e}")
        
        return papers
```

**Checklist**:
- [ ] Create `src/searcher/acl_anthology_searcher.py`
- [ ] Implement ACLAnthologySearcher
- [ ] Add BeautifulSoup parsing logic
- [ ] Test web scraping

---

## STEP 6: Implement Search Orchestrator (30 minutes)

**Location**: `src/searcher/search_engine.py`  
**Purpose**: Coordinate searches across all sources

### Task 6.1: Create search_engine.py
```python
# src/searcher/search_engine.py
import json
from typing import List
from pathlib import Path
from src.models.paper import Paper
from src.searcher.semantic_scholar_searcher import SemanticScholarSearcher
from src.searcher.acl_anthology_searcher import ACLAnthologySearcher
from src.utils.logger import setup_logger

class SearchEngine:
    """Orchestrate paper search across multiple sources."""
    
    def __init__(self, config_dir: str = "config", output_dir: str = "data/raw"):
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logger(__name__)
        self.config = self._load_config()
        self.papers = []
    
    def _load_config(self) -> dict:
        """Load search configuration."""
        with open(self.config_dir / "search" / "search_keywords.json") as f:
            return json.load(f)
    
    def search(self) -> List[Paper]:
        """Execute search across all enabled sources."""
        self.logger.info("Starting paper search...")
        
        keywords = []
        for category, terms in self.config['search_terms'].items():
            keywords.extend(terms)
        
        # Semantic Scholar search
        if self.config['sources']['semantic_scholar'].get('enabled', True):
            self.logger.info("Searching Semantic Scholar...")
            searcher = SemanticScholarSearcher(self.config)
            ss_papers = searcher.search(keywords)
            self.papers.extend(ss_papers)
            self.logger.info(f"Found {len(ss_papers)} papers from Semantic Scholar")
            self._save_papers(ss_papers, "semantic_scholar")
        
        # ACL Anthology search
        if self.config['sources']['acl_anthology'].get('enabled', True):
            self.logger.info("Searching ACL Anthology...")
            searcher = ACLAnthologySearcher(self.config)
            acl_papers = searcher.search(keywords)
            self.papers.extend(acl_papers)
            self.logger.info(f"Found {len(acl_papers)} papers from ACL Anthology")
            self._save_papers(acl_papers, "acl_anthology")
        
        # Deduplicate
        self._deduplicate()
        
        self.logger.info(f"Total unique papers: {len(self.papers)}")
        self._save_papers(self.papers, "combined/all_papers")
        
        return self.papers
    
    def _deduplicate(self):
        """Remove duplicate papers by title."""
        unique = {}
        for paper in self.papers:
            if paper.title not in unique:
                unique[paper.title] = paper
        self.papers = list(unique.values())
    
    def _save_papers(self, papers: List[Paper], subdir: str):
        """Save papers to JSON."""
        output_path = self.output_dir / subdir
        output_path.mkdir(parents=True, exist_ok=True)
        
        json_file = output_path / "papers.json"
        data = [paper.__dict__ for paper in papers]
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        self.logger.info(f"Saved papers to {json_file}")
```

**Checklist**:
- [ ] Create `src/searcher/search_engine.py`
- [ ] Implement SearchEngine orchestrator
- [ ] Add deduplication logic
- [ ] Add paper saving to JSON

---

## STEP 7: Implement PRISMA Screener (45 minutes)

**Location**: `src/screener/`  
**Purpose**: Apply inclusion/exclusion criteria

### Task 7.1: Create prisma_screener.py
```python
# src/screener/prisma_screener.py
import json
from pathlib import Path
from typing import List, Tuple
from src.models.paper import Paper
from src.utils.logger import setup_logger

class PRISMAScreener:
    """Apply PRISMA screening criteria."""
    
    def __init__(self, config_dir: str = "config", output_dir: str = "data/screened"):
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logger(__name__)
        self.config = self._load_config()
        self.included = []
        self.excluded = []
    
    def _load_config(self) -> dict:
        """Load screening configuration."""
        with open(self.config_dir / "screening" / "screening_criteria.json") as f:
            return json.load(f)
    
    def screen(self, papers: List[Paper]) -> Tuple[List[Paper], List[Paper]]:
        """Screen papers using PRISMA criteria."""
        self.logger.info(f"Screening {len(papers)} papers...")
        
        for i, paper in enumerate(papers, 1):
            if self._should_include(paper):
                paper.screened = True
                paper.included = True
                self.included.append(paper)
                self.logger.debug(f"{i}. INCLUDED: {paper.title[:60]}")
            else:
                paper.screened = True
                paper.included = False
                self.excluded.append(paper)
                self.logger.debug(f"{i}. EXCLUDED: {paper.title[:60]}")
        
        self.logger.info(f"Included: {len(self.included)}, Excluded: {len(self.excluded)}")
        
        self._save_results()
        
        return self.included, self.excluded
    
    def _should_include(self, paper: Paper) -> bool:
        """Evaluate paper against screening criteria."""
        # Check year range
        if paper.year < self.config['filters']['year_min'] or paper.year > self.config['filters']['year_max']:
            return False
        
        # Check for target language mentions
        text = (paper.title + " " + paper.abstract).lower()
        keywords = self.config['inclusion_criteria']['target_language_mentioned']['keywords']
        if not any(kw.lower() in text for kw in keywords):
            return False
        
        # Check for NLP focus
        nlp_keywords = ["nlp", "morpholog", "tokeniz", "embedding", "ner", "parsing", "language model", "corpus", "dataset", "tool"]
        if not any(kw in text for kw in nlp_keywords):
            return False
        
        return True
    
    def _save_results(self):
        """Save screening results."""
        # Save included
        included_dir = self.output_dir / "included"
        included_dir.mkdir(parents=True, exist_ok=True)
        
        included_data = [p.__dict__ for p in self.included]
        with open(included_dir / "papers.json", 'w') as f:
            json.dump(included_data, f, indent=2, default=str)
        
        # Save excluded
        excluded_dir = self.output_dir / "excluded"
        excluded_dir.mkdir(parents=True, exist_ok=True)
        
        excluded_data = [p.__dict__ for p in self.excluded]
        with open(excluded_dir / "papers.json", 'w') as f:
            json.dump(excluded_data, f, indent=2, default=str)
        
        self.logger.info(f"Saved screening results to {self.output_dir}")
```

**Checklist**:
- [ ] Create `src/screener/prisma_screener.py`
- [ ] Implement PRISMAScreener
- [ ] Add inclusion/exclusion logic
- [ ] Save included and excluded papers

---

## STEP 8: Implement Paper Coder (60 minutes)

**Location**: `src/coder/`  
**Purpose**: Extract and code papers across 5 dimensions

### Task 8.1: Create paper_coder.py
```python
# src/coder/paper_coder.py
import json
from pathlib import Path
from typing import List
from src.models.paper import Paper
from src.utils.logger import setup_logger

class PaperCoder:
    """Extract and code papers across 5 dimensions."""
    
    def __init__(self, config_dir: str = "config", output_dir: str = "data/coded"):
        self.config_dir = Path(config_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logger(__name__)
        self.config = self._load_config()
        self.papers = []
    
    def _load_config(self) -> dict:
        """Load coding configuration."""
        with open(self.config_dir / "coding" / "coding_schema.json") as f:
            return json.load(f)
    
    def code(self, papers: List[Paper]) -> List[Paper]:
        """Code papers across all dimensions."""
        self.logger.info(f"Coding {len(papers)} papers...")
        
        for i, paper in enumerate(papers, 1):
            self._code_paper(paper)
            self.logger.debug(f"{i}. CODED: {paper.title[:60]} ({paper.primary_pillar})")
        
        self._save_papers()
        self.logger.info(f"Coded {len(papers)} papers")
        
        return papers
    
    def _code_paper(self, paper: Paper):
        """Code a single paper across all dimensions."""
        text = (paper.title + " " + paper.abstract).lower()
        
        # Language coding
        if "amharic" in text:
            paper.languages.append("Amharic")
        if "tigrinya" in text:
            paper.languages.append("Tigrinya")
        if "ge'ez" in text or "geez" in text or "ethiopic" in text:
            paper.languages.append("Classical Ge'ez")
        if not paper.languages:
            paper.languages.append("Other")
        
        # Primary pillar coding
        pillar_keywords = {
            "Tokenization & Normalization": ["tokeniz", "segmentation", "unicode normalization", "fidel"],
            "Lexical & Morphological Analysis": ["morpholog", "root", "lemm", "stemm", "pos tag"],
            "Text Representation & Embeddings": ["embedding", "word2vec", "fasttext", "bert", "xlm"],
            "Sequence Labeling & Structure Extraction": ["ner", "named entity", "parsing", "chunking"]
        }
        
        pillar_scores = {pillar: sum(text.count(kw) for kw in keywords) 
                        for pillar, keywords in pillar_keywords.items()}
        
        if pillar_scores:
            paper.primary_pillar = max(pillar_scores, key=pillar_scores.get)
        
        # Tool type coding
        if "corpus" in text or "dataset" in text:
            paper.tool_type = "Dataset"
        elif "library" in text or "toolkit" in text:
            paper.tool_type = "Library"
        elif "pipeline" in text or "framework" in text:
            paper.tool_type = "Pipeline"
        elif "algorithm" in text or "method" in text:
            paper.tool_type = "Algorithm"
        
        # Morphology coding
        if "morpholog" in text or "root" in text:
            paper.morphology_focus = True
        
        # Script-specific design coding
        if "unicode" in text or "fidel" in text or "normalization" in text:
            paper.script_specific_design = True
        
        # Transfer approach
        if "cross-lingual" in text:
            paper.transfer_approach = "Cross-lingual"
        elif "cross-script" in text:
            paper.transfer_approach = "Cross-script"
        else:
            paper.transfer_approach = "Monolingual"
        
        # Reproducibility
        if "github" in text or "code available" in text:
            paper.code_available = True
        if "dataset" in text or "data available" in text:
            paper.data_available = True
    
    def _save_papers(self):
        """Save coded papers."""
        papers_data = [p.__dict__ for p in self.papers]
        
        with open(self.output_dir / "papers.json", 'w') as f:
            json.dump(papers_data, f, indent=2, default=str)
        
        self.logger.info(f"Saved coded papers to {self.output_dir}")
```

**Checklist**:
- [ ] Create `src/coder/paper_coder.py`
- [ ] Implement PaperCoder
- [ ] Add coding logic for all 5 dimensions
- [ ] Save coded papers

---

## STEP 9: Implement Exporters (45 minutes)

**Location**: `src/exporter/`  
**Purpose**: Generate CSV, JSON, and summary reports

### Task 9.1: Create export_manager.py
```python
# src/exporter/export_manager.py
import csv
import json
from pathlib import Path
from typing import List
import pandas as pd
from src.models.paper import Paper
from src.utils.logger import setup_logger

class ExportManager:
    """Export coded papers to multiple formats."""
    
    def __init__(self, output_dir: str = "data/exported"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logger(__name__)
    
    def export(self, papers: List[Paper]):
        """Export papers to all formats."""
        self.logger.info("Exporting papers...")
        
        self._export_csv(papers)
        self._export_json(papers)
        self._generate_report(papers)
        
        self.logger.info("Export complete")
    
    def _export_csv(self, papers: List[Paper]):
        """Export to CSV."""
        csv_dir = self.output_dir / "csv"
        csv_dir.mkdir(parents=True, exist_ok=True)
        
        csv_file = csv_dir / "geez_nlp_papers.csv"
        
        if papers:
            df = pd.DataFrame([p.to_dict() for p in papers])
            df.to_csv(csv_file, index=False, encoding='utf-8')
            self.logger.info(f"Exported CSV: {csv_file}")
    
    def _export_json(self, papers: List[Paper]):
        """Export to JSON."""
        json_dir = self.output_dir / "json"
        json_dir.mkdir(parents=True, exist_ok=True)
        
        json_file = json_dir / "geez_nlp_papers.json"
        
        data = [p.__dict__ for p in papers]
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
        
        self.logger.info(f"Exported JSON: {json_file}")
    
    def _generate_report(self, papers: List[Paper]):
        """Generate summary report."""
        report_dir = self.output_dir / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / "extraction_summary_report.txt"
        
        # Aggregate statistics
        language_counts = {}
        pillar_counts = {}
        tool_type_counts = {}
        
        for paper in papers:
            for lang in paper.languages:
                language_counts[lang] = language_counts.get(lang, 0) + 1
            
            if paper.primary_pillar:
                pillar_counts[paper.primary_pillar] = pillar_counts.get(paper.primary_pillar, 0) + 1
            
            if paper.tool_type:
                tool_type_counts[paper.tool_type] = tool_type_counts.get(paper.tool_type, 0) + 1
        
        # Generate report
        report = []
        report.append("="*70)
        report.append("Ge'ez-Script NLP Tools Survey: Extraction Summary Report")
        report.append("="*70)
        report.append(f"\nTOTAL PAPERS EXTRACTED: {len(papers)}\n")
        
        report.append("--- LANGUAGE DISTRIBUTION ---")
        for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(papers)) * 100
            report.append(f"  {lang:20s}: {count:3d} ({pct:5.1f}%)")
        
        report.append("\n--- PRIMARY PILLAR DISTRIBUTION ---")
        for pillar, count in sorted(pillar_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(papers)) * 100
            report.append(f"  {pillar:20s}: {count:3d} ({pct:5.1f}%)")
        
        report.append("\n--- TOOL TYPE DISTRIBUTION ---")
        for tool_type, count in sorted(tool_type_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(papers)) * 100
            report.append(f"  {tool_type:20s}: {count:3d} ({pct:5.1f}%)")
        
        # Write report
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))
        
        print("\n".join(report))
        self.logger.info(f"Exported report: {report_file}")
```

**Checklist**:
- [ ] Create `src/exporter/export_manager.py`
- [ ] Implement CSV export
- [ ] Implement JSON export
- [ ] Implement report generation
- [ ] Test all export formats

---

## STEP 10: Implement Pipeline Orchestrator (30 minutes)

**Location**: `src/main.py`  
**Purpose**: Coordinate all 4 phases

### Task 10.1: Create main.py
```python
# src/main.py
import argparse
import sys
from pathlib import Path
from src.searcher.search_engine import SearchEngine
from src.screener.prisma_screener import PRISMAScreener
from src.coder.paper_coder import PaperCoder
from src.exporter.export_manager import ExportManager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Run complete pipeline or individual phases."""
    parser = argparse.ArgumentParser(description='Ge'ez-Script NLP Survey Pipeline')
    parser.add_argument('--phase', choices=['search', 'screen', 'code', 'export', 'all'],
                       default='all', help='Pipeline phase to run')
    
    args = parser.parse_args()
    
    logger.info(f"Starting pipeline (phase: {args.phase})")
    
    # PHASE 1: SEARCH
    if args.phase in ['all', 'search']:
        logger.info("="*70)
        logger.info("PHASE 1: SEARCH")
        logger.info("="*70)
        
        searcher = SearchEngine()
        papers = searcher.search()
        logger.info(f"Found {len(papers)} papers")
    
    else:
        # Load papers from previous search
        import json
        papers_file = Path("data/raw/combined/all_papers.json")
        if papers_file.exists():
            with open(papers_file) as f:
                papers_data = json.load(f)
            papers = [type('Paper', (), p)() for p in papers_data]
        else:
            logger.error("No papers found. Run with --phase search first.")
            sys.exit(1)
    
    # PHASE 2: SCREENING
    if args.phase in ['all', 'screen']:
        logger.info("="*70)
        logger.info("PHASE 2: SCREENING")
        logger.info("="*70)
        
        screener = PRISMAScreener()
        included, excluded = screener.screen(papers)
        logger.info(f"Included: {len(included)}, Excluded: {len(excluded)}")
        
        papers = included
    
    else:
        # Load included papers
        import json
        papers_file = Path("data/screened/included/papers.json")
        if papers_file.exists():
            with open(papers_file) as f:
                papers_data = json.load(f)
            papers = [type('Paper', (), p)() for p in papers_data]
    
    # PHASE 3: CODING
    if args.phase in ['all', 'code']:
        logger.info("="*70)
        logger.info("PHASE 3: CODING")
        logger.info("="*70)
        
        coder = PaperCoder()
        coder.papers = papers
        papers = coder.code(papers)
        logger.info(f"Coded {len(papers)} papers")
    
    # PHASE 4: EXPORT
    if args.phase in ['all', 'export']:
        logger.info("="*70)
        logger.info("PHASE 4: EXPORT")
        logger.info("="*70)
        
        exporter = ExportManager()
        exporter.export(papers)
    
    logger.info("="*70)
    logger.info("PIPELINE COMPLETE")
    logger.info("="*70)

if __name__ == "__main__":
    main()
```

**Checklist**:
- [ ] Create `src/main.py`
- [ ] Implement argument parsing
- [ ] Coordinate all 4 phases
- [ ] Add error handling

---

## STEP 11: Write Unit Tests (60 minutes)

**Location**: `tests/unit/`  
**Purpose**: Test individual components

### Task 11.1: Create test_models.py
```python
# tests/unit/test_models.py
import pytest
from src.models.paper import Paper

def test_paper_creation():
    """Test Paper creation."""
    paper = Paper(
        id="test_1",
        title="Test Paper",
        authors=["Author 1", "Author 2"],
        year=2023,
        venue="ACL",
        source="semantic_scholar"
    )
    
    assert paper.id == "test_1"
    assert paper.title == "Test Paper"
    assert len(paper.authors) == 2
    assert paper.year == 2023

def test_paper_to_dict():
    """Test Paper.to_dict()."""
    paper = Paper(
        id="test_1",
        title="Test Paper",
        authors=["Author 1"],
        year=2023,
        venue="ACL",
        languages=["Amharic"],
        primary_pillar="Morphology",
        tool_type="Library"
    )
    
    d = paper.to_dict()
    assert d['title'] == "Test Paper"
    assert d['languages'] == "Amharic"
```

### Task 11.2: Create test_screener.py
```python
# tests/unit/test_screener.py
import pytest
from src.models.paper import Paper
from src.screener.prisma_screener import PRISMAScreener

def test_screening_included():
    """Test screening of included paper."""
    screener = PRISMAScreener()
    
    paper = Paper(
        id="test_1",
        title="Amharic NLP Tool",
        abstract="We present a morphological analyzer for Amharic",
        year=2023,
        venue="ACL",
        source="semantic_scholar"
    )
    
    assert screener._should_include(paper) == True

def test_screening_excluded():
    """Test screening of excluded paper."""
    screener = PRISMAScreener()
    
    paper = Paper(
        id="test_2",
        title="English NLP Tool",
        abstract="We present a tool for English",
        year=2023,
        venue="ACL",
        source="semantic_scholar"
    )
    
    assert screener._should_include(paper) == False
```

**Checklist**:
- [ ] Create `tests/unit/test_models.py`
- [ ] Create `tests/unit/test_screener.py`
- [ ] Create `tests/unit/test_coder.py`
- [ ] Create `tests/unit/test_exporter.py`
- [ ] Run pytest and verify all tests pass

---

## STEP 12: Write Integration Tests (30 minutes)

**Location**: `tests/integration/`  
**Purpose**: Test full pipeline flow

### Task 12.1: Create test_pipeline.py
```python
# tests/integration/test_pipeline.py
import pytest
import json
from pathlib import Path
from src.searcher.search_engine import SearchEngine
from src.screener.prisma_screener import PRISMAScreener
from src.coder.paper_coder import PaperCoder
from src.exporter.export_manager import ExportManager

def test_full_pipeline():
    """Test complete pipeline with mock data."""
    # Create mock papers
    from src.models.paper import Paper
    
    papers = [
        Paper(
            id="test_1",
            title="Amharic Morphological Analyzer",
            abstract="We present a tool for Amharic morphology",
            year=2023,
            venue="ACL",
            source="semantic_scholar"
        )
    ]
    
    # Screen
    screener = PRISMAScreener()
    included, excluded = screener.screen(papers)
    assert len(included) > 0
    
    # Code
    coder = PaperCoder()
    coder.papers = included
    coded = coder.code(included)
    assert len(coded) > 0
    
    # Export
    exporter = ExportManager()
    exporter.export(coded)
    
    # Verify output files
    assert (Path("data/exported/csv") / "geez_nlp_papers.csv").exists()
    assert (Path("data/exported/json") / "geez_nlp_papers.json").exists()
```

**Checklist**:
- [ ] Create `tests/integration/test_pipeline.py`
- [ ] Create `tests/integration/test_data_flow.py`
- [ ] Run integration tests

---

## STEP 13: Quality Assurance & Documentation (45 minutes)

**Tasks**:
- [ ] Run all tests: `python -m pytest tests/ -v`
- [ ] Check code coverage: `pytest --cov=src --cov-report=html`
- [ ] Run linting: `flake8 src/`
- [ ] Format code: `black src/`
- [ ] Verify configuration files
- [ ] Test all export formats

**Checklist**:
- [ ] All tests passing (>80% coverage)
- [ ] No linting errors
- [ ] Code formatted consistently
- [ ] CSV exports correctly
- [ ] JSON exports correctly
- [ ] Reports generate correctly

---

## STEP 14: Final Testing & Documentation (30 minutes)

**Tasks**:
- [ ] Run full pipeline: `python src/main.py`
- [ ] Verify Phase 1: Check `data/raw/semantic_scholar/papers.json`
- [ ] Verify Phase 2: Check `data/screened/included/papers.json`
- [ ] Verify Phase 3: Check `data/coded/papers.json`
- [ ] Verify Phase 4: Check `data/exported/csv/geez_nlp_papers.csv`
- [ ] Review summary report
- [ ] Update README with results
- [ ] First commit: `git add . && git commit -m "Implement complete PRISMA pipeline"`

**Checklist**:
- [ ] All phases execute successfully
- [ ] Output files generated correctly
- [ ] Git repository initialized
- [ ] First commit created
- [ ] Project ready for use

---

## Implementation Timeline

| Step | Task | Time | Cumulative |
|------|------|------|-----------|
| 1 | Data Models | 30 min | 30 min |
| 2 | Config Loader | 15 min | 45 min |
| 3 | Logger & Utils | 15 min | 60 min |
| 4 | Base Searcher | 45 min | 105 min |
| 5 | ACL Searcher | 45 min | 150 min |
| 6 | Search Orchestrator | 30 min | 180 min |
| 7 | PRISMA Screener | 45 min | 225 min |
| 8 | Paper Coder | 60 min | 285 min |
| 9 | Exporters | 45 min | 330 min |
| 10 | Pipeline Orchestrator | 30 min | 360 min |
| 11 | Unit Tests | 60 min | 420 min |
| 12 | Integration Tests | 30 min | 450 min |
| 13 | QA & Docs | 45 min | 495 min |
| 14 | Final Testing | 30 min | 525 min |

**Total: 525 minutes (8.75 hours)**

---

## Success Criteria

✅ All 4 phases implemented and working  
✅ >80% test coverage  
✅ No linting errors  
✅ CSV, JSON, and report outputs generated  
✅ Full documentation complete  
✅ Git repository with clean commit history  
✅ Ready for production use

---

**Ready to start? Begin with STEP 1: Create Data Models**


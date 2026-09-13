# A Comprehensive Survey of NLP Tools for Ge'ez-Script Languages (2016-2026)

**Systematic review of 16 tools and 70 papers for Amharic, Tigrinya, and Classical Ge'ez**

## Overview

This repository contains a comprehensive systematic review of NLP tools and research for Ge'ez-script languages using PRISMA methodology. We identify 16 foundational tools across 4 technical pillars and analyze 70 peer-reviewed papers (2016–2026).

## 📄 Primary Deliverable

**`geez_nlp_survey_COMPLETE_REBUILD.pdf`** (16 pages, 216 KB)
- ✅ **MAIN SUBMISSION FILE** for PanAfriCon AI 2026
- Comprehensive, full-length manuscript
- Complete extended discussion, methodology, and analysis
- All 4 figures, full tool inventory, and 5-priority research agenda
- Bibliography with 70 papers and 2 featured citations

**Alternative (streamlined):** `geez_nlp_survey_FINAL_ENHANCED.pdf` (5 pages, 138 KB, core content only)

## Quick Links

- **PDF:** `geez_nlp_survey_COMPLETE_REBUILD.pdf` (16 pages - **SUBMIT THIS**)
- **Source:** `geez_nlp_survey_COMPLETE_REBUILD.tex` (LaTeX)
- **Papers:** `papers_bibliography.json` (70 papers, JSON)
- **Data:** `PAPERS_EXTRACTION_WITH_FULL_TITLES.csv` (70 papers, spreadsheet)

## Key Findings

**Language Coverage:**
- Amharic: 8 tools (50%)
- Tigrinya: 9 tools (56%)
- Classical Ge'ez: 2 tools (12%) ⚠️ **Underrepresented**

**Technical Pillars:**
- P1 (Tokenization): 3 tools
- P2 (Morphology): 3 tools
- P3 (Embeddings/LMs): 4 tools
- P4 (Sequence Labeling): 1 tool ⚠️ **Critical bottleneck**
- Other (Infrastructure): 5 tools

**Design Patterns:**
- 71% single-language (depth-first)
- 65% rule-based (interpretability)
- 29% multilingual (limited transfer)

## Five-Priority Research Agenda

1. Unified script-aware tokenization
2. Cross-lingual morphological transfer
3. Script-optimized embeddings
4. Expanded sequence labeling
5. Community infrastructure

## Files

```
geez_nlp_survey_COMPLETE_REBUILD.pdf     ✅ Main submission (16 pages, comprehensive)
geez_nlp_survey_COMPLETE_REBUILD.tex     # LaTeX source (comprehensive)
geez_nlp_survey_FINAL_ENHANCED.pdf       # Alternative (5 pages, streamlined)
geez_nlp_survey_FINAL_ENHANCED.tex       # LaTeX source (streamlined)
papers_bibliography.json                 # 70 papers (JSON)
PAPERS_EXTRACTION_WITH_FULL_TITLES.csv   # 70 papers (CSV)
data/                                    # PRISMA pipeline data
```

## Citation

```bibtex
@article{teklehaymanot2026geez,
  title={A Comprehensive Survey of NLP Tools for Ge'ez-Script Languages (2016-2026)},
  author={Teklehaymanot, Hailay Kidu},
  journal={PanAfriCon AI},
  year={2026}
}
```

## Usage

**View the manuscript:**
```bash
open geez_nlp_survey_COMPLETE_REBUILD.pdf
```

**Access papers data:**
```python
import json
papers = json.load(open('papers_bibliography.json'))
print(f"Total papers: {len(papers['papers'])}")
```

**Open in spreadsheet:**
Import `PAPERS_EXTRACTION_WITH_FULL_TITLES.csv` to Excel or Google Sheets

**Compile from source:**
```bash
pdflatex geez_nlp_survey_COMPLETE_REBUILD.tex
```

## Statistics

| Metric | Value |
|--------|-------|
| **Pages** | 16 (comprehensive) |
| **File Size** | 216 KB |
| **Ge'ez-script Tools** | 16 (verified scope) |
| **Papers Analyzed** | 70 (peer-reviewed) |
| **Technical Pillars** | 4 (P1, P2, P3, P4) |
| **Scope** | Amharic, Tigrinya, Classical Ge'ez |

## Author

Hailay Kidu Teklehaymanot  
L3S Research Center, Leibniz University Hannover  
teklehaymanot@l3s.uni-hannover.de

---

**Status:** ✅ Publication-Ready (16-page comprehensive manuscript)  
**Submission Target:** PanAfriCon AI 2026  
**Last Updated:** September 13, 2026  
**Compile Command:** `pdflatex geez_nlp_survey_COMPLETE_REBUILD.tex`

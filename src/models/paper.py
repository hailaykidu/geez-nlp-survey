"""Paper, Coding, and Screening data models for the Ge'ez-Script NLP survey."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ScreeningDecisionCode(str, Enum):
    """Exclusion codes for papers that don't meet inclusion criteria."""

    TECHNICAL_REPORT = "technical_report"
    BLOG = "blog"
    THESIS = "thesis"
    PREPRINT_ONLY = "preprint_only"
    NO_GEEZ_SCRIPT_LANGUAGE = "no_geez_script_language"
    LINGUISTICS_ONLY = "linguistics_only"
    HISTORICAL = "historical"
    COMPUTATIONAL_LINGUISTICS_NO_TOOLS = "computational_linguistics_no_tools"
    NO_FOUNDATIONAL_TOOL = "no_foundational_tool"
    DOWNSTREAM_APPLICATION_ONLY = "downstream_application_only"
    DUPLICATE_PAPER = "duplicate_paper"
    OUT_OF_SCOPE = "out_of_scope"
    OUT_OF_DATE = "out_of_date"


@dataclass
class ScreeningDecision:
    """Result of screening decision for a paper."""

    paper_id: str
    included: bool
    decision_code: Optional[ScreeningDecisionCode] = None
    reasoning: str = ""
    screened_by: str = ""
    screened_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


@dataclass
class Paper:
    """Core paper metadata and coding for the NLP survey."""

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

    def to_json_dict(self) -> Dict[str, Any]:
        """Convert to dictionary preserving types for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi,
            "url": self.url,
            "abstract": self.abstract,
            "source": self.source,
            "screened": self.screened,
            "included": self.included,
            "screening_decision": self.screening_decision,
            "screening_notes": self.screening_notes,
            "languages": self.languages,
            "primary_pillar": self.primary_pillar,
            "secondary_pillars": self.secondary_pillars,
            "tool_type": self.tool_type,
            "morphology_focus": self.morphology_focus,
            "morphological_assumption": self.morphological_assumption,
            "script_specific_design": self.script_specific_design,
            "transfer_approach": self.transfer_approach,
            "code_available": self.code_available,
            "data_available": self.data_available,
            "code_url": self.code_url,
            "data_url": self.data_url,
            "created_at": self.created_at,
            "coder_notes": self.coder_notes,
        }


@dataclass
class Coding:
    """Structured coding for a paper across 5 dimensions."""

    paper_id: str
    languages: List[str]
    primary_pillar: str
    secondary_pillars: List[str]
    tool_type: str
    morphology_focus: bool
    morphological_assumption: str = ""
    script_specific_design: bool = False
    transfer_approach: str = ""
    code_available: bool = False
    data_available: bool = False
    code_url: str = ""
    data_url: str = ""
    coder_notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert coding to dictionary."""
        return {
            "paper_id": self.paper_id,
            "languages": self.languages,
            "primary_pillar": self.primary_pillar,
            "secondary_pillars": self.secondary_pillars,
            "tool_type": self.tool_type,
            "morphology_focus": self.morphology_focus,
            "morphological_assumption": self.morphological_assumption,
            "script_specific_design": self.script_specific_design,
            "transfer_approach": self.transfer_approach,
            "code_available": self.code_available,
            "data_available": self.data_available,
            "code_url": self.code_url,
            "data_url": self.data_url,
            "coder_notes": self.coder_notes,
            "created_at": self.created_at,
        }

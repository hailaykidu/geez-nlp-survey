"""Paper data model used to load the verified literature corpus for figure generation."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class Paper:
    """Core paper metadata and coding fields for one row of the verified corpus."""

    # Metadata
    id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    doi: str = ""
    url: str = ""
    abstract: str = ""
    source: str = ""

    # Screening
    screened: bool = False
    included: bool = False
    screening_decision: str = ""
    screening_notes: str = ""

    # Coding
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

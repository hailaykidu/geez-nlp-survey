"""Source adapters for multi-source resource discovery"""
from .academic_searcher import AcademicSearcher
from .github_searcher import GitHubSearcher
from .pypi_searcher import PyPISearcher
from .huggingface_searcher import HuggingFaceSearcher
from .zenodo_searcher import ZenodoSearcher

__all__ = [
    'AcademicSearcher',
    'GitHubSearcher',
    'PyPISearcher',
    'HuggingFaceSearcher',
    'ZenodoSearcher'
]

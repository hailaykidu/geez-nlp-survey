"""Processors for metadata extraction and classification"""
from .contribution_classifier import ContributionClassifier
from .pillar_classifier import PillarClassifier
from .language_detector import LanguageDetector
from .deduplicator import Deduplicator

__all__ = [
    'ContributionClassifier',
    'PillarClassifier',
    'LanguageDetector',
    'Deduplicator'
]

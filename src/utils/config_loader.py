"""Configuration loader for Ge'ez-Script NLP survey.

Loads and validates JSON configuration files for search, screening, and coding phases.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging


class ConfigLoadError(Exception):
    """Raised when configuration loading fails."""

    pass


class ConfigLoader:
    """Load and manage configuration files for the survey pipeline.

    Attributes:
        config_dir: Path to the configuration directory
        _search_config: Cached search configuration
        _screening_config: Cached screening configuration
        _coding_config: Cached coding configuration
    """

    def __init__(self, config_dir: str = "config"):
        """Initialize ConfigLoader with configuration directory path.

        Args:
            config_dir: Path to configuration directory (default: "config")

        Raises:
            ConfigLoadError: If config directory does not exist
        """
        self.config_dir = Path(config_dir)

        if not self.config_dir.exists():
            raise ConfigLoadError(
                f"Configuration directory not found: {self.config_dir.absolute()}"
            )

        self.logger = logging.getLogger(__name__)
        self._search_config: Optional[Dict[str, Any]] = None
        self._screening_config: Optional[Dict[str, Any]] = None
        self._coding_config: Optional[Dict[str, Any]] = None

    def load_search_config(self) -> Dict[str, Any]:
        """Load search configuration from JSON.

        Searches for search_keywords.json in config directory.
        Results are cached for subsequent calls.

        Returns:
            Dictionary containing search configuration with keys:
            - metadata: Version, description, created date
            - search_terms: Search keywords by language
            - sources: API/source configurations

        Raises:
            ConfigLoadError: If file not found or JSON is invalid
        """
        if self._search_config is not None:
            return self._search_config

        config_path = self.config_dir / "search_keywords.json"

        try:
            with open(config_path, encoding="utf-8") as f:
                self._search_config = json.load(f)
                self.logger.debug(f"Loaded search config from {config_path}")
                return self._search_config
        except FileNotFoundError:
            raise ConfigLoadError(f"Search config file not found: {config_path.absolute()}")
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON in search config: {config_path} - {str(e)}")

    def load_screening_config(self) -> Dict[str, Any]:
        """Load screening configuration from JSON.

        Searches for screening_criteria.json in config directory.
        Results are cached for subsequent calls.

        Returns:
            Dictionary containing screening configuration with keys:
            - metadata: Version, description, created date
            - inclusion_criteria: PRISMA inclusion criteria
            - exclusion_criteria: PRISMA exclusion criteria with codes
            - decision_tree: Step-by-step screening decision tree

        Raises:
            ConfigLoadError: If file not found or JSON is invalid
        """
        if self._screening_config is not None:
            return self._screening_config

        config_path = self.config_dir / "screening_criteria.json"

        try:
            with open(config_path, encoding="utf-8") as f:
                self._screening_config = json.load(f)
                self.logger.debug(f"Loaded screening config from {config_path}")
                return self._screening_config
        except FileNotFoundError:
            raise ConfigLoadError(f"Screening config file not found: {config_path.absolute()}")
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON in screening config: {config_path} - {str(e)}")

    def load_coding_config(self) -> Dict[str, Any]:
        """Load coding configuration from JSON.

        Searches for coding_schema.json in config directory.
        Results are cached for subsequent calls.

        Returns:
            Dictionary containing coding configuration with keys:
            - metadata: Version, description, created date
            - dimensions: 5 coding dimensions with allowed values
                - languages: Target languages
                - pillars: NLP pillars
                - tool_types: Tool types
                - morphology: Morphology-specific features
                - script_adaptation: Script adaptation approaches

        Raises:
            ConfigLoadError: If file not found or JSON is invalid
        """
        if self._coding_config is not None:
            return self._coding_config

        config_path = self.config_dir / "coding_schema.json"

        try:
            with open(config_path, encoding="utf-8") as f:
                self._coding_config = json.load(f)
                self.logger.debug(f"Loaded coding config from {config_path}")
                return self._coding_config
        except FileNotFoundError:
            raise ConfigLoadError(f"Coding config file not found: {config_path.absolute()}")
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON in coding config: {config_path} - {str(e)}")

    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load all three configuration files at once.

        Returns:
            Dictionary with keys 'search', 'screening', 'coding' containing
            their respective configurations

        Raises:
            ConfigLoadError: If any configuration file fails to load
        """
        return {
            "search": self.load_search_config(),
            "screening": self.load_screening_config(),
            "coding": self.load_coding_config(),
        }

    def validate_search_config(self, config: Dict[str, Any]) -> bool:
        """Validate search configuration structure.

        Args:
            config: Search configuration dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = {"metadata", "search_terms", "sources"}
        return required_keys.issubset(config.keys())

    def validate_screening_config(self, config: Dict[str, Any]) -> bool:
        """Validate screening configuration structure.

        Args:
            config: Screening configuration dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = {
            "metadata",
            "inclusion_criteria",
            "exclusion_criteria",
            "decision_tree",
        }
        return required_keys.issubset(config.keys())

    def validate_coding_config(self, config: Dict[str, Any]) -> bool:
        """Validate coding configuration structure.

        Args:
            config: Coding configuration dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = {"metadata", "dimensions"}
        return required_keys.issubset(config.keys())

    def clear_cache(self) -> None:
        """Clear cached configurations to force reload from disk."""
        self._search_config = None
        self._screening_config = None
        self._coding_config = None
        self.logger.debug("Configuration cache cleared")

    def get_config_path(self, config_type: str) -> Path:
        """Get the path to a configuration file.

        Args:
            config_type: One of 'search', 'screening', or 'coding'

        Returns:
            Path to the configuration file

        Raises:
            ValueError: If config_type is invalid
        """
        config_files = {
            "search": "search_keywords.json",
            "screening": "screening_criteria.json",
            "coding": "coding_schema.json",
        }

        if config_type not in config_files:
            raise ValueError(
                f"Unknown config type: {config_type}. "
                f"Must be one of {list(config_files.keys())}"
            )

        return self.config_dir / config_files[config_type]

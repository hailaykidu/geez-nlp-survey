"""Unit tests for Configuration Loader.

Tests the ConfigLoader class for loading, validating, and managing
JSON configuration files for the survey pipeline.
"""

import pytest
import json
import tempfile
from pathlib import Path

from src.utils.config_loader import ConfigLoader, ConfigLoadError


class TestConfigLoaderInit:
    """Test ConfigLoader initialization."""

    def test_init_valid_config_dir(self):
        """Test initialization with valid config directory."""
        loader = ConfigLoader(config_dir="config")
        assert loader.config_dir == Path("config")
        assert loader.config_dir.exists()

    def test_init_invalid_config_dir(self):
        """Test initialization with invalid config directory."""
        with pytest.raises(ConfigLoadError):
            ConfigLoader(config_dir="/nonexistent/config/path")

    def test_init_default_config_dir(self):
        """Test initialization with default config directory."""
        loader = ConfigLoader()
        assert loader.config_dir == Path("config")


class TestConfigLoaderSearchConfig:
    """Test loading search configuration."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_load_search_config(self, loader):
        """Test loading search configuration successfully."""
        config = loader.load_search_config()
        assert config is not None
        assert isinstance(config, dict)

    def test_search_config_has_required_keys(self, loader):
        """Test search config has required top-level keys."""
        config = loader.load_search_config()
        assert "metadata" in config
        assert "search_terms" in config
        assert "sources" in config

    def test_search_config_metadata(self, loader):
        """Test search config metadata."""
        config = loader.load_search_config()
        metadata = config.get("metadata", {})
        assert "version" in metadata
        assert "description" in metadata

    def test_search_config_search_terms(self, loader):
        """Test search config contains expected languages."""
        config = loader.load_search_config()
        search_terms = config.get("search_terms", {})
        assert "amharic" in search_terms
        assert "tigrinya" in search_terms
        assert "geez" in search_terms

    def test_search_config_sources(self, loader):
        """Test search config contains expected sources."""
        config = loader.load_search_config()
        sources = config.get("sources", {})
        # At least one source should be present
        assert len(sources) > 0

    def test_search_config_caching(self, loader):
        """Test that search config is cached."""
        config1 = loader.load_search_config()
        config2 = loader.load_search_config()
        assert config1 is config2  # Same object due to caching

    def test_search_config_validate(self, loader):
        """Test search config validation."""
        config = loader.load_search_config()
        assert loader.validate_search_config(config) is True


class TestConfigLoaderScreeningConfig:
    """Test loading screening configuration."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_load_screening_config(self, loader):
        """Test loading screening configuration successfully."""
        config = loader.load_screening_config()
        assert config is not None
        assert isinstance(config, dict)

    def test_screening_config_has_required_keys(self, loader):
        """Test screening config has required top-level keys."""
        config = loader.load_screening_config()
        assert "metadata" in config
        assert "inclusion_criteria" in config
        assert "exclusion_criteria" in config
        assert "decision_tree" in config

    def test_screening_config_metadata(self, loader):
        """Test screening config metadata."""
        config = loader.load_screening_config()
        metadata = config.get("metadata", {})
        assert "version" in metadata
        assert "description" in metadata

    def test_screening_config_inclusion_criteria(self, loader):
        """Test screening config inclusion criteria."""
        config = loader.load_screening_config()
        inclusion = config.get("inclusion_criteria", {})
        assert "peer_reviewed" in inclusion
        assert "target_language_mentioned" in inclusion

    def test_screening_config_exclusion_criteria(self, loader):
        """Test screening config exclusion criteria."""
        config = loader.load_screening_config()
        exclusion = config.get("exclusion_criteria", {})
        # Should have exclusion criteria defined
        assert len(exclusion) > 0

    def test_screening_config_decision_tree(self, loader):
        """Test screening config decision tree."""
        config = loader.load_screening_config()
        decision_tree = config.get("decision_tree", {})
        # Should have decision steps
        assert len(decision_tree) > 0

    def test_screening_config_caching(self, loader):
        """Test that screening config is cached."""
        config1 = loader.load_screening_config()
        config2 = loader.load_screening_config()
        assert config1 is config2  # Same object due to caching

    def test_screening_config_validate(self, loader):
        """Test screening config validation."""
        config = loader.load_screening_config()
        assert loader.validate_screening_config(config) is True


class TestConfigLoaderCodingConfig:
    """Test loading coding configuration."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_load_coding_config(self, loader):
        """Test loading coding configuration successfully."""
        config = loader.load_coding_config()
        assert config is not None
        assert isinstance(config, dict)

    def test_coding_config_has_required_keys(self, loader):
        """Test coding config has required top-level keys."""
        config = loader.load_coding_config()
        assert "metadata" in config
        assert "dimensions" in config

    def test_coding_config_metadata(self, loader):
        """Test coding config metadata."""
        config = loader.load_coding_config()
        metadata = config.get("metadata", {})
        assert "version" in metadata
        assert "description" in metadata

    def test_coding_config_dimensions(self, loader):
        """Test coding config dimensions."""
        config = loader.load_coding_config()
        dimensions = config.get("dimensions", {})
        # Should have at least languages dimension
        assert len(dimensions) > 0

    def test_coding_config_caching(self, loader):
        """Test that coding config is cached."""
        config1 = loader.load_coding_config()
        config2 = loader.load_coding_config()
        assert config1 is config2  # Same object due to caching

    def test_coding_config_validate(self, loader):
        """Test coding config validation."""
        config = loader.load_coding_config()
        assert loader.validate_coding_config(config) is True


class TestConfigLoaderAllConfigs:
    """Test loading all configurations at once."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_load_all_configs(self, loader):
        """Test loading all configurations at once."""
        all_configs = loader.load_all_configs()
        assert all_configs is not None
        assert isinstance(all_configs, dict)

    def test_load_all_configs_has_all_types(self, loader):
        """Test that load_all_configs returns all config types."""
        all_configs = loader.load_all_configs()
        assert "search" in all_configs
        assert "screening" in all_configs
        assert "coding" in all_configs

    def test_load_all_configs_returns_full_configs(self, loader):
        """Test that load_all_configs returns complete configurations."""
        all_configs = loader.load_all_configs()
        assert len(all_configs["search"]) > 0
        assert len(all_configs["screening"]) > 0
        assert len(all_configs["coding"]) > 0


class TestConfigLoaderValidation:
    """Test configuration validation methods."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_validate_search_config_valid(self, loader):
        """Test validation of valid search config."""
        config = loader.load_search_config()
        assert loader.validate_search_config(config) is True

    def test_validate_search_config_missing_key(self, loader):
        """Test validation fails for invalid search config."""
        invalid_config = {"metadata": {}}  # Missing search_terms and sources
        assert loader.validate_search_config(invalid_config) is False

    def test_validate_screening_config_valid(self, loader):
        """Test validation of valid screening config."""
        config = loader.load_screening_config()
        assert loader.validate_screening_config(config) is True

    def test_validate_screening_config_missing_key(self, loader):
        """Test validation fails for invalid screening config."""
        invalid_config = {"metadata": {}}  # Missing other required keys
        assert loader.validate_screening_config(invalid_config) is False

    def test_validate_coding_config_valid(self, loader):
        """Test validation of valid coding config."""
        config = loader.load_coding_config()
        assert loader.validate_coding_config(config) is True

    def test_validate_coding_config_missing_key(self, loader):
        """Test validation fails for invalid coding config."""
        invalid_config = {"metadata": {}}  # Missing dimensions
        assert loader.validate_coding_config(invalid_config) is False


class TestConfigLoaderPaths:
    """Test configuration file path methods."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_get_search_config_path(self, loader):
        """Test getting search config file path."""
        path = loader.get_config_path("search")
        assert path.name == "search_keywords.json"

    def test_get_screening_config_path(self, loader):
        """Test getting screening config file path."""
        path = loader.get_config_path("screening")
        assert path.name == "screening_criteria.json"

    def test_get_coding_config_path(self, loader):
        """Test getting coding config file path."""
        path = loader.get_config_path("coding")
        assert path.name == "coding_schema.json"

    def test_get_config_path_invalid_type(self, loader):
        """Test getting config path with invalid type."""
        with pytest.raises(ValueError):
            loader.get_config_path("invalid")


class TestConfigLoaderCache:
    """Test configuration caching behavior."""

    @pytest.fixture
    def loader(self):
        """Provide ConfigLoader instance."""
        return ConfigLoader(config_dir="config")

    def test_cache_initial_state(self, loader):
        """Test that cache is empty initially."""
        assert loader._search_config is None
        assert loader._screening_config is None
        assert loader._coding_config is None

    def test_cache_after_load(self, loader):
        """Test that config is cached after loading."""
        loader.load_search_config()
        assert loader._search_config is not None

    def test_clear_cache(self, loader):
        """Test clearing configuration cache."""
        loader.load_search_config()
        assert loader._search_config is not None
        loader.clear_cache()
        assert loader._search_config is None
        assert loader._screening_config is None
        assert loader._coding_config is None

    def test_reload_after_clear(self, loader):
        """Test reloading config after cache clear."""
        config1 = loader.load_search_config()
        loader.clear_cache()
        config2 = loader.load_search_config()
        assert config1 is not config2
        assert config1 == config2  # Same content, different object


class TestConfigLoaderErrorHandling:
    """Test error handling in ConfigLoader."""

    def test_load_from_nonexistent_directory(self):
        """Test error when config directory does not exist."""
        with pytest.raises(ConfigLoadError):
            ConfigLoader(config_dir="/nonexistent/path")

    def test_load_nonexistent_search_config(self):
        """Test error when search config file is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = ConfigLoader(config_dir=tmpdir)
            with pytest.raises(ConfigLoadError):
                loader.load_search_config()

    def test_load_invalid_json_search_config(self):
        """Test error when search config contains invalid JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create invalid JSON file
            config_file = Path(tmpdir) / "search_keywords.json"
            config_file.write_text("{ invalid json }")

            loader = ConfigLoader(config_dir=tmpdir)
            with pytest.raises(ConfigLoadError):
                loader.load_search_config()

    def test_get_invalid_config_path(self):
        """Test error when getting invalid config type path."""
        loader = ConfigLoader(config_dir="config")
        with pytest.raises(ValueError):
            loader.get_config_path("invalid_type")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

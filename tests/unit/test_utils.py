"""Unit tests for utilities (logger and helpers).

Tests logging configuration and helper utility functions used throughout
the survey pipeline.
"""

import pytest
import json
import csv
import tempfile
import logging
from pathlib import Path

from src.utils.logger import (
    setup_logger,
    get_logger,
    disable_logger,
    enable_logger,
    set_log_level,
    clear_handlers,
)
from src.utils.helpers import (
    ensure_dir,
    safe_file_write,
    safe_file_read,
    write_json,
    read_json,
    write_csv,
    read_csv,
    get_file_hash,
    sanitize_filename,
    normalize_text,
    truncate_text,
    flatten_dict,
    get_timestamp,
    get_timestamp_filename,
    list_files,
    merge_dicts,
    chunk_list,
)


class TestLogger:
    """Test logger setup and configuration."""

    def test_setup_logger_console_only(self):
        """Test logger setup with console output only."""
        logger = setup_logger("test_logger_1")
        assert logger is not None
        assert logger.name == "test_logger_1"
        assert len(logger.handlers) > 0

    def test_setup_logger_with_file(self):
        """Test logger setup with file output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            logger = setup_logger("test_logger_2", log_file=str(log_file))

            logger.info("Test message")
            assert log_file.exists()
            assert "Test message" in log_file.read_text()

    def test_logger_debug_to_file_info_to_console(self):
        """Test that file captures DEBUG but console shows INFO."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            logger = setup_logger("test_logger_3", log_file=str(log_file))

            logger.debug("Debug message")
            logger.info("Info message")

            log_content = log_file.read_text()
            assert "Debug message" in log_content
            assert "Info message" in log_content

    def test_get_logger(self):
        """Test getting a logger instance."""
        logger1 = setup_logger("test_logger_4")
        logger2 = get_logger("test_logger_4")
        assert logger1 is logger2

    def test_disable_logger(self):
        """Test disabling a logger."""
        logger = setup_logger("test_logger_5")
        disable_logger("test_logger_5")
        assert logger.disabled is True

    def test_enable_logger(self):
        """Test enabling a logger."""
        logger = setup_logger("test_logger_6")
        disable_logger("test_logger_6")
        enable_logger("test_logger_6")
        assert logger.disabled is False

    def test_set_log_level(self):
        """Test changing log level."""
        logger = setup_logger("test_logger_7")
        set_log_level("test_logger_7", logging.WARNING)
        assert logger.level == logging.WARNING

    def test_clear_handlers(self):
        """Test clearing logger handlers."""
        logger = setup_logger("test_logger_8")
        initial_handlers = len(logger.handlers)
        clear_handlers("test_logger_8")
        assert len(logger.handlers) == 0

    def test_logger_creates_log_directory(self):
        """Test that logger creates parent directory for log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "logs" / "subdir" / "test.log"
            logger = setup_logger("test_logger_9", log_file=str(log_file))
            logger.info("Test")
            assert log_file.parent.exists()


class TestHelpersDirAndFiles:
    """Test directory and file helper functions."""

    def test_ensure_dir_creates_directory(self):
        """Test that ensure_dir creates directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "new" / "nested" / "dir"
            result = ensure_dir(test_dir)
            assert result.exists()
            assert result.is_dir()

    def test_ensure_dir_returns_path_object(self):
        """Test that ensure_dir returns Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = ensure_dir(tmpdir)
            assert isinstance(result, Path)

    def test_safe_file_write(self):
        """Test safe file write."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            content = "Test content"
            result = safe_file_write(file_path, content)

            assert result.exists()
            assert result.read_text() == content

    def test_safe_file_write_creates_parent_dirs(self):
        """Test that safe_file_write creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "a" / "b" / "c" / "test.txt"
            safe_file_write(file_path, "content")
            assert file_path.exists()

    def test_safe_file_write_with_backup(self):
        """Test that safe_file_write creates backup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            safe_file_write(file_path, "original")
            safe_file_write(file_path, "modified", create_backup=True)

            backup_path = file_path.with_suffix(".txt.bak")
            assert backup_path.exists()
            assert backup_path.read_text() == "original"
            assert file_path.read_text() == "modified"

    def test_safe_file_read(self):
        """Test safe file read."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            original_content = "Read this content"
            file_path.write_text(original_content)

            content = safe_file_read(file_path)
            assert content == original_content

    def test_safe_file_read_missing_file(self):
        """Test safe_file_read raises for missing file."""
        with pytest.raises(FileNotFoundError):
            safe_file_read("/nonexistent/file.txt")


class TestJsonHelpers:
    """Test JSON helper functions."""

    def test_write_json(self):
        """Test writing JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.json"
            data = {"name": "Test", "value": 42, "nested": {"key": "value"}}

            result = write_json(data, file_path)
            assert result.exists()

            loaded = json.loads(file_path.read_text())
            assert loaded == data

    def test_write_json_creates_parent_dirs(self):
        """Test that write_json creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "a" / "b" / "data.json"
            write_json({"test": "data"}, file_path)
            assert file_path.exists()

    def test_read_json(self):
        """Test reading JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.json"
            original_data = {"key": "value", "number": 123}
            file_path.write_text(json.dumps(original_data))

            data = read_json(file_path)
            assert data == original_data

    def test_write_read_json_preserves_unicode(self):
        """Test that write/read JSON preserves Unicode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "unicode.json"
            data = {"amharic": "አማርኛ", "tigrinya": "ትግርኛ"}

            write_json(data, file_path, ensure_ascii=False)
            loaded = read_json(file_path)
            assert loaded == data


class TestCsvHelpers:
    """Test CSV helper functions."""

    def test_write_csv(self):
        """Test writing CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.csv"
            data = [
                {"name": "Alice", "age": "30"},
                {"name": "Bob", "age": "25"},
            ]

            result = write_csv(data, file_path)
            assert result.exists()

    def test_read_csv(self):
        """Test reading CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.csv"
            original_data = [
                {"name": "Alice", "age": "30"},
                {"name": "Bob", "age": "25"},
            ]
            write_csv(original_data, file_path)

            data = read_csv(file_path)
            assert len(data) == 2
            assert data[0]["name"] == "Alice"

    def test_write_csv_empty_data_raises(self):
        """Test that write_csv raises for empty data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "data.csv"
            with pytest.raises(ValueError):
                write_csv([], file_path)


class TestFileHash:
    """Test file hashing."""

    def test_get_file_hash(self):
        """Test calculating file hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            file_path.write_text("Test content")

            hash1 = get_file_hash(file_path)
            assert isinstance(hash1, str)
            assert len(hash1) == 64  # SHA256 is 64 hex chars

    def test_get_file_hash_same_for_same_content(self):
        """Test that identical files have same hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"
            content = "Same content"

            file1.write_text(content)
            file2.write_text(content)

            hash1 = get_file_hash(file1)
            hash2 = get_file_hash(file2)
            assert hash1 == hash2

    def test_get_file_hash_different_for_different_content(self):
        """Test that different files have different hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"

            file1.write_text("Content 1")
            file2.write_text("Content 2")

            hash1 = get_file_hash(file1)
            hash2 = get_file_hash(file2)
            assert hash1 != hash2


class TestTextHelpers:
    """Test text manipulation helpers."""

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        dirty = 'My Paper: "NLP & ML" (2023) | v2.0'
        clean = sanitize_filename(dirty)
        assert ":" not in clean
        assert '"' not in clean
        assert "|" not in clean

    def test_normalize_text(self):
        """Test text normalization."""
        text = "  Multiple   spaces   here  "
        normalized = normalize_text(text)
        assert normalized == "Multiple spaces here"

    def test_normalize_text_newlines(self):
        """Test that normalize_text handles newlines."""
        text = "Line 1\n\n\nLine 2"
        normalized = normalize_text(text)
        assert normalized == "Line 1 Line 2"

    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a very long text that needs truncation"
        truncated = truncate_text(text, max_length=20)
        assert len(truncated) <= 20
        assert truncated.endswith("...")

    def test_truncate_text_no_truncation_needed(self):
        """Test truncate_text when text is short."""
        text = "Short"
        truncated = truncate_text(text, max_length=20)
        assert truncated == text


class TestDictHelpers:
    """Test dictionary helpers."""

    def test_flatten_dict(self):
        """Test flattening nested dictionary."""
        nested = {
            "level1": {
                "level2a": 1,
                "level2b": {"level3": 2}
            }
        }
        flat = flatten_dict(nested)
        assert "level1_level2a" in flat
        assert "level1_level2b_level3" in flat
        assert flat["level1_level2a"] == 1
        assert flat["level1_level2b_level3"] == 2

    def test_flatten_dict_custom_separator(self):
        """Test flatten_dict with custom separator."""
        nested = {"a": {"b": 1}}
        flat = flatten_dict(nested, sep=".")
        assert "a.b" in flat

    def test_merge_dicts(self):
        """Test merging dictionaries."""
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3}
        d3 = {"a": 10}

        merged = merge_dicts(d1, d2, d3)
        assert merged["a"] == 10  # d3 overrides d1
        assert merged["b"] == 2
        assert merged["c"] == 3


class TestTimestamps:
    """Test timestamp helpers."""

    def test_get_timestamp(self):
        """Test getting current timestamp."""
        ts = get_timestamp()
        assert isinstance(ts, str)
        assert "T" in ts  # ISO format includes T

    def test_get_timestamp_filename(self):
        """Test generating timestamp filename."""
        filename = get_timestamp_filename("export", ".json")
        assert filename.startswith("export_")
        assert filename.endswith(".json")

    def test_get_timestamp_filename_no_prefix(self):
        """Test timestamp filename without prefix."""
        filename = get_timestamp_filename(suffix=".csv")
        assert filename.endswith(".csv")


class TestListFiles:
    """Test file listing helpers."""

    def test_list_files(self):
        """Test listing files in directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.txt").touch()
            Path(tmpdir, "file2.txt").touch()
            Path(tmpdir, "file3.json").touch()

            txt_files = list_files(tmpdir, pattern="*.txt")
            assert len(txt_files) == 2

    def test_list_files_recursive(self):
        """Test listing files recursively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.txt").touch()
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            Path(subdir, "file2.txt").touch()

            txt_files = list_files(tmpdir, pattern="*.txt", recursive=True)
            assert len(txt_files) == 2

    def test_list_files_nonexistent_dir(self):
        """Test list_files with nonexistent directory."""
        files = list_files("/nonexistent/directory")
        assert files == []


class TestChunkList:
    """Test list chunking helper."""

    def test_chunk_list(self):
        """Test chunking a list."""
        lst = [1, 2, 3, 4, 5, 6, 7]
        chunks = chunk_list(lst, 3)
        assert len(chunks) == 3
        assert chunks[0] == [1, 2, 3]
        assert chunks[1] == [4, 5, 6]
        assert chunks[2] == [7]

    def test_chunk_list_exact_chunks(self):
        """Test chunking with exact division."""
        lst = [1, 2, 3, 4]
        chunks = chunk_list(lst, 2)
        assert len(chunks) == 2
        assert chunks[0] == [1, 2]
        assert chunks[1] == [3, 4]

    def test_chunk_list_single_chunk(self):
        """Test chunking larger than list."""
        lst = [1, 2, 3]
        chunks = chunk_list(lst, 10)
        assert len(chunks) == 1
        assert chunks[0] == lst


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

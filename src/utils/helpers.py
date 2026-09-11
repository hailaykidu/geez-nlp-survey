"""Helper utilities for the Ge'ez-Script NLP survey pipeline.

Provides utility functions for common tasks like data validation, file operations,
text processing, and data serialization.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import hashlib


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object of the directory

    Raises:
        OSError: If directory cannot be created
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def safe_file_write(
    file_path: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
    create_backup: bool = False,
) -> Path:
    """Safely write content to a file.

    Creates parent directories as needed and optionally backs up existing files.

    Args:
        file_path: Path to file to write
        content: Content to write
        encoding: File encoding (default: utf-8)
        create_backup: If True, backup existing file with .bak extension

    Returns:
        Path object of written file

    Raises:
        IOError: If file cannot be written
    """
    file_path = Path(file_path)
    ensure_dir(file_path.parent)

    # Create backup if file exists
    if create_backup and file_path.exists():
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        file_path.rename(backup_path)

    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)

    return file_path


def safe_file_read(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Safely read content from a file.

    Args:
        file_path: Path to file to read
        encoding: File encoding (default: utf-8)

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file does not exist
        IOError: If file cannot be read
    """
    file_path = Path(file_path)
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()


def write_json(
    data: Any,
    file_path: Union[str, Path],
    indent: int = 2,
    ensure_ascii: bool = False,
) -> Path:
    """Write data to a JSON file.

    Args:
        data: Data to serialize to JSON
        file_path: Path to output file
        indent: JSON indentation level (default: 2)
        ensure_ascii: If False, preserve Unicode characters (default: False)

    Returns:
        Path object of written file

    Raises:
        TypeError: If data is not JSON serializable
        IOError: If file cannot be written
    """
    file_path = Path(file_path)
    ensure_dir(file_path.parent)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)

    return file_path


def read_json(file_path: Union[str, Path]) -> Any:
    """Read data from a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Deserialized JSON data

    Raises:
        FileNotFoundError: If file does not exist
        json.JSONDecodeError: If JSON is invalid
    """
    file_path = Path(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_csv(
    data: List[Dict[str, Any]],
    file_path: Union[str, Path],
    fieldnames: Optional[List[str]] = None,
) -> Path:
    """Write data to a CSV file.

    Args:
        data: List of dictionaries to write
        file_path: Path to output CSV file
        fieldnames: Optional list of field names (auto-detected if None)

    Returns:
        Path object of written file

    Raises:
        ValueError: If data is empty or fieldnames invalid
        IOError: If file cannot be written
    """
    file_path = Path(file_path)
    ensure_dir(file_path.parent)

    if not data:
        raise ValueError("Cannot write empty data to CSV")

    # Auto-detect fieldnames from first row
    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return file_path


def read_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Read data from a CSV file.

    Args:
        file_path: Path to CSV file

    Returns:
        List of dictionaries representing rows

    Raises:
        FileNotFoundError: If file does not exist
        csv.Error: If CSV is malformed
    """
    file_path = Path(file_path)
    rows = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def get_file_hash(file_path: Union[str, Path], algorithm: str = "sha256") -> str:
    """Calculate hash of a file.

    Useful for detecting duplicate files or verifying file integrity.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (default: sha256)

    Returns:
        Hex string of file hash

    Raises:
        FileNotFoundError: If file does not exist
    """
    file_path = Path(file_path)
    hasher = hashlib.new(algorithm)

    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing/replacing invalid characters.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename

    Example:
        >>> sanitize_filename("My Paper: NLP & ML (2023)")
        "My_Paper_NLP_and_ML_2023"
    """
    # Replace invalid characters
    invalid_chars = r'<>:"/\\|?*'
    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, "_")

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")

    return sanitized


def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace.

    Args:
        text: Text to normalize

    Returns:
        Normalized text

    Example:
        >>> normalize_text("  Multiple   spaces  ")
        "Multiple spaces"
    """
    return " ".join(text.split())


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to maximum length with optional suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length (default: 200)
        suffix: Suffix to add if truncated (default: "...")

    Returns:
        Truncated text

    Example:
        >>> truncate_text("Very long text", max_length=8)
        "Very ..."
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = "_") -> Dict[str, Any]:
    """Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Prefix for keys (used in recursion)
        sep: Separator between nested keys (default: "_")

    Returns:
        Flattened dictionary

    Example:
        >>> flatten_dict({"a": {"b": 1, "c": 2}})
        {"a_b": 1, "a_c": 2}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_timestamp() -> str:
    """Get current timestamp in ISO format.

    Returns:
        ISO 8601 formatted timestamp

    Example:
        >>> ts = get_timestamp()
        "2026-09-11T15:30:45.123456"
    """
    return datetime.now().isoformat()


def get_timestamp_filename(prefix: str = "", suffix: str = "") -> str:
    """Generate a filename with timestamp.

    Args:
        prefix: Prefix for filename
        suffix: Suffix for filename

    Returns:
        Filename with timestamp

    Example:
        >>> fn = get_timestamp_filename("export", ".json")
        "export_20260911_153045.json"
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if prefix:
        return f"{prefix}_{timestamp}{suffix}"
    return f"{timestamp}{suffix}"


def list_files(
    directory: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
) -> List[Path]:
    """List files in a directory matching a pattern.

    Args:
        directory: Directory to search
        pattern: Glob pattern (default: "*")
        recursive: If True, search recursively (default: False)

    Returns:
        List of matching file paths

    Example:
        >>> files = list_files("data", pattern="*.json", recursive=True)
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        return []

    if recursive:
        return list(dir_path.rglob(pattern))
    else:
        return list(dir_path.glob(pattern))


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries into one.

    Args:
        *dicts: Variable number of dictionaries to merge

    Returns:
        Merged dictionary (later values override earlier ones)

    Example:
        >>> merge_dicts({"a": 1}, {"b": 2}, {"a": 3})
        {"a": 3, "b": 2}
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size.

    Args:
        lst: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks (lists)

    Example:
        >>> chunk_list([1,2,3,4,5], 2)
        [[1,2], [3,4], [5]]
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

"""Shared local-only JSON and path helpers. Python 3.10 or later."""

import json
import math
import os
from pathlib import Path, PurePosixPath
import tempfile
import unicodedata


def parse_json(text):
    """Parse JSON without duplicate keys, non-finite constants, or float overflow."""
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_number(value):
        raise ValueError(f"non-finite JSON number: {value}")

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            invalid_number(value)
        return number

    return json.loads(text, object_pairs_hook=unique_pairs,
                      parse_constant=invalid_number, parse_float=finite_float)


def read_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return parse_json(stream.read())


def safe_relative_path(value, root):
    """Reject absolute, parent, ambiguous, and symlink-escaping paths."""
    if not isinstance(value, str) or not value or any(unicodedata.category(c) == "Cc" for c in value):
        raise ValueError("must be a nonempty project-relative path")
    if "\\" in value or ":" in value or value.startswith("/"):
        raise ValueError("must use a relative POSIX path without a protocol")
    if any(part in ("", ".", "..") for part in value.split("/")):
        raise ValueError("empty, dot, and parent path components are forbidden")
    path = Path(root).resolve() / PurePosixPath(value)
    if not path.resolve().is_relative_to(Path(root).resolve()):
        raise ValueError("path resolves outside the project")
    return path


def write_json(path, value, force=False):
    """Publish a complete file atomically, without overwrite by default."""
    path = Path(path)
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temporary, path)
        else:
            # A hard link creates the destination only if it does not exist.
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

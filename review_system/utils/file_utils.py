"""
review_system/utils/file_utils.py

Safe filesystem helpers for the review system.
All helpers that might touch the filesystem live here.
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, List


def safe_mkdir(path: Path) -> None:
    """Create directory and all parents. Never raises if it already exists."""
    path.mkdir(parents=True, exist_ok=True)


def read_text_safe(path: Path, encoding: str = "utf-8") -> Optional[str]:
    """Read a text file. Returns None on any error instead of raising."""
    try:
        return path.read_text(encoding=encoding, errors="replace")
    except Exception:
        return None


def write_text_safe(path: Path, content: str, encoding: str = "utf-8") -> bool:
    """Write text to file. Returns True on success, False on error."""
    try:
        safe_mkdir(path.parent)
        path.write_text(content, encoding=encoding)
        return True
    except Exception:
        return False


def write_json_safe(path: Path, data: Any, indent: int = 2) -> bool:
    """Serialise data to JSON and write to file."""
    try:
        safe_mkdir(path.parent)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception:
        return False


def read_json_safe(path: Path) -> Optional[Dict[str, Any]]:
    """Read and parse a JSON file. Returns None on any error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def resolve_report_path(path_str: str) -> Optional[Path]:
    """
    Resolve a CLI-supplied report path to an absolute Path.
    Returns None if the path does not exist or is not a file.
    """
    p = Path(path_str).resolve()
    if not p.exists():
        return None
    if not p.is_file():
        return None
    return p


def strip_html_tags(html: str) -> str:
    """Lightweight HTML-to-text converter (no dependencies)."""
    from html.parser import HTMLParser

    class _Extractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self._chunks: List[str] = []
            self._skip = False

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style"):
                self._skip = True
            elif tag in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6"):
                self._chunks.append("\n")

        def handle_endtag(self, tag):
            if tag in ("script", "style"):
                self._skip = False

        def handle_data(self, data):
            if not self._skip:
                stripped = data.strip()
                if stripped:
                    self._chunks.append(stripped)

        def get_text(self) -> str:
            return "\n".join(self._chunks)

    parser = _Extractor()
    parser.feed(html)
    return parser.get_text()


def infer_report_title(path: Path, fallback: str = "Untitled Report") -> str:
    """
    Try to derive a human-readable title from a report path or its content.
    Priority: manifest.json → first H1 in file → filename stem.
    """
    parent = path.parent

    # 1. manifest.json in same directory
    manifest_path = parent / "manifest.json"
    if manifest_path.exists():
        manifest = read_json_safe(manifest_path)
        if manifest:
            for key in ("title", "report_title", "_display_topic", "topic"):
                if manifest.get(key):
                    return str(manifest[key])

    # 2. First H1 line in the file itself
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
            if line and not line.startswith("#"):
                break  # stop after preamble
    except Exception:
        pass

    # 3. Filename stem, humanised
    stem = path.stem.replace("_", " ").replace("-", " ").title()
    return stem or fallback

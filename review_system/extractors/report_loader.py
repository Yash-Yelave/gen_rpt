"""
review_system/extractors/report_loader.py

Loads a report artifact from any supported format and returns raw text + title.
Reads from gen_rpt_original output dirs or any path — never writes anywhere.

Load priority:
  1. .md  (markdown — best structure preservation)
  2. .html (HTML — stripped to text)
  3. .json (flat JSON — field values concatenated)
  4. .txt  (plain text)
"""
from pathlib import Path
from typing import Optional, Tuple

from review_system.utils.file_utils import (
    read_text_safe, strip_html_tags, infer_report_title,
)
from review_system.utils.logging_utils import get_run_logger

log = get_run_logger()


def load_report(path: Path) -> Tuple[str, str]:
    """
    Load a report from `path` and return (raw_text, title).

    Raises FileNotFoundError if path does not exist.
    Raises ValueError if file content is too short to be a real report.
    """
    if not path.exists():
        raise FileNotFoundError(f"Report file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    suffix = path.suffix.lower()

    if suffix in (".md", ".txt"):
        raw = read_text_safe(path)
    elif suffix in (".html", ".htm"):
        raw = _load_html(path)
    elif suffix == ".json":
        raw = _load_json(path)
    else:
        # Try as plain text regardless of extension
        raw = read_text_safe(path)

    if raw is None:
        raise ValueError(f"Could not read content from {path}")

    raw = raw.strip()
    if len(raw) < 100:
        raise ValueError(
            f"Report content from {path} is too short ({len(raw)} chars) to audit."
        )

    title = infer_report_title(path)
    log.info("Loaded report: %r | %d chars | title=%r", str(path), len(raw), title)
    return raw, title


def _load_html(path: Path) -> Optional[str]:
    raw_html = read_text_safe(path)
    if raw_html is None:
        return None
    text = strip_html_tags(raw_html)
    return text if len(text) > 100 else None


def _load_json(path: Path) -> Optional[str]:
    import json
    raw = read_text_safe(path)
    if raw is None:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw  # treat as plain text

    parts = []

    def _flatten(obj):
        if isinstance(obj, str) and obj.strip():
            parts.append(obj.strip())
        elif isinstance(obj, dict):
            for v in obj.values():
                _flatten(v)
        elif isinstance(obj, list):
            for item in obj:
                _flatten(item)

    _flatten(data)
    return "\n\n".join(parts) or None

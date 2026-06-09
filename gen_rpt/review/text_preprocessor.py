"""
text_preprocessor.py

Parses raw report text (markdown or plain text) into a structured
list of sections, each with numbered paragraphs. Provides the
location-reference substrate used by all downstream review steps.
"""
import re
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Paragraph:
    """One paragraph inside a section."""
    def __init__(self, index: int, text: str):
        self.index: int = index          # 1-based within its section
        self.text: str = text.strip()

    def opening(self, n: int = 8) -> str:
        words = self.text.split()
        return " ".join(words[:n])

    def closing(self, n: int = 8) -> str:
        words = self.text.split()
        return " ".join(words[-n:])

    def location_snippet(self) -> str:
        return f'"{self.opening()}" → "{self.closing()}"'

    def __repr__(self) -> str:
        return f"<Para {self.index}: {self.text[:60]}...>"


class Section:
    """One headed section of the report."""
    def __init__(self, title: str, level: int, paragraphs: List[Paragraph]):
        self.title: str = title
        self.level: int = level                  # heading depth (1-6)
        self.paragraphs: List[Paragraph] = paragraphs

    @property
    def full_text(self) -> str:
        return "\n\n".join(p.text for p in self.paragraphs)

    @property
    def word_count(self) -> int:
        return len(self.full_text.split())

    def location_ref(self, para_index: int | None = None) -> str:
        if para_index is not None:
            try:
                para = self.paragraphs[para_index - 1]
                return (
                    f"Location → [{self.title}] | "
                    f"Para {para_index} | {para.location_snippet()}"
                )
            except IndexError:
                pass
        return f"Location → [{self.title}]"

    def __repr__(self) -> str:
        return f"<Section '{self.title}' ({len(self.paragraphs)} paras)>"


class ParsedReport:
    """Full parsed representation of a report."""
    def __init__(self, sections: List[Section], raw_text: str):
        self.sections: List[Section] = sections
        self.raw_text: str = raw_text

    @property
    def section_titles(self) -> List[str]:
        return [s.title for s in self.sections]

    @property
    def total_words(self) -> int:
        return sum(s.word_count for s in self.sections)

    def get_section(self, title: str) -> Section | None:
        tl = title.lower()
        for s in self.sections:
            if s.title.lower() == tl:
                return s
        return None

    def as_context_dict(self) -> Dict[str, Any]:
        """Compact dict for stuffing into LLM prompts."""
        return {
            "total_words": self.total_words,
            "section_count": len(self.sections),
            "sections": [
                {
                    "title": s.title,
                    "level": s.level,
                    "word_count": s.word_count,
                    "paragraphs": [
                        {"index": p.index, "text": p.text}
                        for p in s.paragraphs
                    ],
                }
                for s in self.sections
            ],
        }

    def __repr__(self) -> str:
        return (
            f"<ParsedReport {len(self.sections)} sections, "
            f"{self.total_words} words>"
        )


# ---------------------------------------------------------------------------
# Parsing logic
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_BLANK_LINE_RE = re.compile(r"\n{2,}")


def _strip_markdown_noise(text: str) -> str:
    """Remove common markdown decoration that isn't content."""
    # Remove horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_paragraphs(raw_block: str) -> List[Paragraph]:
    """Split a section body into non-empty paragraphs."""
    chunks = _BLANK_LINE_RE.split(raw_block.strip())
    paras: List[Paragraph] = []
    for i, chunk in enumerate(chunks, start=1):
        chunk = chunk.strip()
        if chunk:
            paras.append(Paragraph(index=i, text=chunk))
    return paras


def parse_report(text: str) -> ParsedReport:
    """
    Parse a markdown or plain-text report into a ParsedReport.

    Strategy:
    1. Find all heading positions.
    2. Slice the text between consecutive headings into section bodies.
    3. Chunk each body into paragraphs.
    4. If no headings found at all, treat the whole document as one
       un-titled section so the pipeline never receives empty input.
    """
    cleaned = _strip_markdown_noise(text)

    matches = list(_HEADING_RE.finditer(cleaned))

    if not matches:
        # Plain text with no markdown headings
        paras = _extract_paragraphs(cleaned)
        sections = [Section(title="[Document]", level=1, paragraphs=paras)]
        return ParsedReport(sections=sections, raw_text=text)

    sections: List[Section] = []

    # Optional preamble before the first heading
    preamble = cleaned[: matches[0].start()].strip()
    if preamble:
        paras = _extract_paragraphs(preamble)
        if paras:
            sections.append(Section(title="[Preamble]", level=0, paragraphs=paras))

    for idx, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()

        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
        body = cleaned[body_start:body_end].strip()

        paras = _extract_paragraphs(body)
        # Always add the section — even if empty so titles appear in analysis
        sections.append(Section(title=title, level=level, paragraphs=paras))

    return ParsedReport(sections=sections, raw_text=text)


def truncate_for_prompt(parsed: ParsedReport, max_chars: int = 28_000) -> str:
    """
    Return a compact text representation of the parsed report, suitable
    for injection into a Groq prompt, capped at max_chars.

    Format:
        ## [Section Title]
        [Para 1 text]
        [Para 2 text]
        ...
    """
    lines: List[str] = []
    for s in parsed.sections:
        lines.append(f"\n## {s.title}")
        for p in s.paragraphs:
            lines.append(f"[Para {p.index}] {p.text}")

    full = "\n".join(lines)
    if len(full) <= max_chars:
        return full

    # Hard-truncate with a clear marker
    return full[:max_chars] + "\n\n[... report truncated for length ...]"

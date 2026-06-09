"""
shared/report_schema.py

Pure data schema for a parsed report.
No business logic. Import freely from both generation and review systems.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Paragraph:
    index: int          # 1-based within its section
    text: str

    def opening(self, n: int = 8) -> str:
        words = self.text.split()
        return " ".join(words[:n])

    def closing(self, n: int = 8) -> str:
        words = self.text.split()
        return " ".join(words[-n:])

    def snippet(self) -> str:
        return f'"{self.opening()}" -> "{self.closing()}"'


@dataclass
class Section:
    title: str
    level: int                              # heading depth 1-6; 0 = preamble
    paragraphs: List[Paragraph] = field(default_factory=list)

    @property
    def full_text(self) -> str:
        return "\n\n".join(p.text for p in self.paragraphs)

    @property
    def word_count(self) -> int:
        return len(self.full_text.split())

    def location_ref(self, para_index: Optional[int] = None) -> str:
        if para_index is not None and 1 <= para_index <= len(self.paragraphs):
            p = self.paragraphs[para_index - 1]
            return (
                f"Location -> [{self.title}] | Para {para_index} | {p.snippet()}"
            )
        return f"Location -> [{self.title}]"


@dataclass
class ParsedReport:
    sections: List[Section]
    raw_text: str
    title: str = "Untitled Report"

    @property
    def section_titles(self) -> List[str]:
        return [s.title for s in self.sections]

    @property
    def total_words(self) -> int:
        return sum(s.word_count for s in self.sections)

    def get_section(self, title: str) -> Optional[Section]:
        tl = title.lower()
        for s in self.sections:
            if s.title.lower() == tl:
                return s
        return None

    def as_prompt_text(self, max_chars: int = 24_000) -> str:
        """Compact text for LLM prompts."""
        lines: List[str] = []
        for s in self.sections:
            lines.append(f"\n## {s.title}")
            for p in s.paragraphs:
                lines.append(f"[Para {p.index}] {p.text}")
        full = "\n".join(lines)
        if len(full) <= max_chars:
            return full
        return full[:max_chars] + "\n\n[... report truncated for length ...]"

    def as_context_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
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

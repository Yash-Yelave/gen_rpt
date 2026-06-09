"""
review_system/extractors/section_parser.py

Parses raw report text (markdown or plain text) into a ParsedReport.
Uses shared/report_schema.py data classes.
"""
import re
from typing import List

from shared.report_schema import ParsedReport, Section, Paragraph
from review_system.utils.logging_utils import get_run_logger

log = get_run_logger()

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_BLANK_LINE_RE = re.compile(r"\n{2,}")


def _clean(text: str) -> str:
    """Strip markdown noise: horizontal rules, excess blank lines."""
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _make_paragraphs(block: str) -> List[Paragraph]:
    chunks = _BLANK_LINE_RE.split(block.strip())
    paras = []
    for i, chunk in enumerate(chunks, start=1):
        chunk = chunk.strip()
        if chunk:
            paras.append(Paragraph(index=i, text=chunk))
    return paras


def parse_report(text: str, title: str = "Untitled Report") -> ParsedReport:
    """
    Parse raw report text into a ParsedReport.

    If no markdown headings are found, the whole document becomes one
    un-titled section so the pipeline never receives empty input.
    """
    cleaned = _clean(text)
    matches = list(_HEADING_RE.finditer(cleaned))
    sections: List[Section] = []

    if not matches:
        paras = _make_paragraphs(cleaned)
        sections.append(Section(title="[Document]", level=1, paragraphs=paras))
        log.info("Parsed (no headings): 1 section, %d words", sum(len(p.text.split()) for p in paras))
        return ParsedReport(sections=sections, raw_text=text, title=title)

    # Optional preamble before first heading
    preamble = cleaned[: matches[0].start()].strip()
    if preamble:
        paras = _make_paragraphs(preamble)
        if paras:
            sections.append(Section(title="[Preamble]", level=0, paragraphs=paras))

    for idx, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(2).strip()
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
        body = cleaned[body_start:body_end].strip()
        paras = _make_paragraphs(body)
        sections.append(Section(title=heading, level=level, paragraphs=paras))

    parsed = ParsedReport(sections=sections, raw_text=text, title=title)
    log.info(
        "Parsed report: %d sections, %d words",
        len(sections), parsed.total_words,
    )
    return parsed

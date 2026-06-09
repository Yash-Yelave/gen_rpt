"""
review_system/extractors/location_mapper.py

Builds standardised location reference strings for any section/paragraph.
Used by all analyzers and claim extractors to produce consistent refs.

Format: "Location -> [<section_title>] | Para <N> | "<opening>" -> "<closing>""
"""
from typing import Optional

from shared.report_schema import ParsedReport, Section, Paragraph


def make_ref(
    section_title: str,
    para_index: Optional[int] = None,
    opening: Optional[str] = None,
    closing: Optional[str] = None,
) -> str:
    """Build a location reference string from components."""
    base = f"Location -> [{section_title}]"
    if para_index is not None:
        base += f" | Para {para_index}"
        if opening and closing:
            base += f' | "{opening}" -> "{closing}"'
    return base


def ref_from_para(section: Section, para: Paragraph) -> str:
    """Build a location reference from a Section + Paragraph."""
    return make_ref(
        section_title=section.title,
        para_index=para.index,
        opening=para.opening(),
        closing=para.closing(),
    )


def ref_from_section(section: Section) -> str:
    """Location reference for a whole section (no paragraph)."""
    return make_ref(section_title=section.title)


def find_location(
    parsed: ParsedReport,
    section_title: str,
    para_index: Optional[int] = None,
) -> str:
    """
    Construct a location ref for a known section title and optional paragraph.
    Falls back gracefully if section/para not found.
    """
    section = parsed.get_section(section_title)
    if section is None:
        return make_ref(section_title=section_title, para_index=para_index)

    if para_index is not None and 1 <= para_index <= len(section.paragraphs):
        para = section.paragraphs[para_index - 1]
        return ref_from_para(section, para)

    return ref_from_section(section)

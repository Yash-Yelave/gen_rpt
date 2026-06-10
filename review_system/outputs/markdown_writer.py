"""
review_system/outputs/markdown_writer.py

Renders the complete ReviewData into a rich, never-empty Markdown report.
12 sections, severity badges, emoji location pins, improvement task cards.
"""
from pathlib import Path
from typing import Dict, Any, List

from review_system.config.review_config import OUTPUT_FILES
from review_system.utils.file_utils import write_text_safe
from review_system.utils.logging_utils import get_generation_logger

log = get_generation_logger()

# ── Badge helpers ────────────────────────────────────────────────────────────

def _sev(s: str) -> str:
    return {"Critical": "**[CRITICAL]**", "High": "**[HIGH]**",
            "Medium": "**[MEDIUM]**", "Low": "**[LOW]**"}.get(s, f"**[{s}]**")

def _grade_badge(g: str) -> str:
    return {"Gold": "Gold (90-100)", "Silver": "Silver (75-89)",
            "Bronze": "Bronze (60-74)", "Red": "Red — Revision Required (<60)"}.get(g, g)

def _ready(flag: bool) -> str:
    return "YES" if flag else "NO"

def _none_note() -> str:
    return "_None identified in this report._\n\n"

def _pin(loc: str) -> str:
    if loc and loc != "N/A":
        return f"\n  > {loc}\n"
    return ""

# ── Section renderers ────────────────────────────────────────────────────────

def _render_located(items: List[Dict]) -> str:
    if not items:
        return _none_note()
    lines = []
    for item in items:
        text = (item.get("finding") or item.get("issue") or
                item.get("weakness") or item.get("strength") or "")
        sev  = item.get("severity", "Medium")
        loc  = item.get("location_ref", "")
        lines.append(f"- {_sev(sev)} {text}{_pin(loc)}")
    return "\n".join(lines) + "\n\n"


def _render_data_gaps(items: List[Dict]) -> str:
    if not items:
        return _none_note()
    lines = []
    for g in items:
        sev  = g.get("severity", "Medium")
        sect = g.get("section", "Unknown")
        clm  = g.get("claim", "")
        miss = g.get("missing_data", [])
        loc  = g.get("location_ref", "")
        lines.append(f"- {_sev(sev)} **[{sect}]** {clm}")
        if miss:
            lines.append(f"  - Missing: {', '.join(miss)}")
        lines.append(_pin(loc).strip())
    return "\n".join(lines) + "\n\n"


def _render_weak_assumptions(items: List[Dict]) -> str:
    if not items:
        return _none_note()
    lines = []
    for w in items:
        sev  = w.get("severity", "Medium")
        clm  = w.get("forecast_or_claim", "")
        miss = w.get("missing_evidence", "")
        loc  = w.get("location_ref", "")
        lines.append(f"- {_sev(sev)} {clm}")
        if miss:
            lines.append(f"  - Missing evidence: {miss}")
        lines.append(_pin(loc).strip())
    return "\n".join(lines) + "\n\n"


def _render_writing_flaws(items: List[Dict]) -> str:
    if not items:
        return _none_note()
    lines = []
    for w in items:
        sev   = w.get("severity", "Medium")
        ftype = w.get("flaw_type", "")
        ex    = w.get("example", "")
        loc   = w.get("location_ref", "")
        sugg  = w.get("suggestion", "")
        lines.append(f"- {_sev(sev)} **{ftype}**")
        if ex:
            lines.append(f'  - Example: _"{ex}"_')
        if sugg:
            lines.append(f"  - Fix: {sugg}")
        lines.append(_pin(loc).strip())
    return "\n".join(lines) + "\n\n"


def _render_task(i: int, task: Dict) -> str:
    pri    = task.get("priority", "Medium")
    sect   = task.get("section", "General")
    issue  = task.get("issue", "")
    fix    = task.get("fix", "")
    impact = task.get("expected_impact", "")
    return (
        f"### Task {i}: {_sev(pri)} — {sect}\n\n"
        f"**Issue:** {issue}\n\n"
        f"**Fix:** {fix}\n\n"
        f"**Expected Impact:** {impact}\n\n"
    )


# ── Main renderer ────────────────────────────────────────────────────────────

def generate_markdown(review_data: Dict[str, Any]) -> str:
    scores     = review_data.get("scores", {})
    recs       = review_data.get("recommendations", {})
    claims     = review_data.get("claims_audit", {})
    title      = review_data.get("report_title", "Untitled Report")
    ts         = review_data.get("timestamp", "")
    grade      = scores.get("grade", "N/A")
    overall    = scores.get("overall_score", "N/A")
    exec_comm  = recs.get("executive_communication", {})

    rq = scores.get("research_quality", {})
    ec = scores.get("evidence_and_citations", {})
    sc = scores.get("strategic_clarity", {})
    ws = scores.get("writing_and_structure", {})

    md: List[str] = []
    md.append("# Institutional Research Audit Report\n\n")
    md.append(f"> **Report:** {title}  \n> **Timestamp:** {ts}\n\n")
    md.append("---\n\n")

    # 1. Executive Summary Table (score + grade only)
    md.append("## 1. Executive Review\n\n")
    md.append("| Metric | Value |\n|--------|-------|\n")
    md.append(f"| **Overall Score** | **{overall} / 100** |\n")
    md.append(f"| **Grade** | {_grade_badge(grade)} |\n\n")

    # 2. Scores — new What Works / What Fails bullet format
    md.append("## 2. Scores and Justifications\n\n")

    dim_labels = [
        ("research_quality",       "Research Quality",      rq,  30),
        ("evidence_and_citations", "Evidence & Citations",  ec,  25),
        ("strategic_clarity",      "Strategic Clarity",     sc,  25),
        ("writing_and_structure",  "Writing & Structure",   ws,  20),
    ]

    for _, dim_label, dim_data, dim_max in dim_labels:
        s  = dim_data.get("score", "N/A")
        ww = dim_data.get("what_works") or []
        wf = dim_data.get("what_fails") or []
        md.append(f"### {dim_label}: {s} / {dim_max}\n\n")
        md.append("**What Works:**\n\n")
        if ww:
            for item in ww:
                pt  = item.get("point", "") if isinstance(item, dict) else str(item)
                loc = item.get("location_ref", "") if isinstance(item, dict) else ""
                md.append(f"- {pt}")
                if loc and loc != "N/A":
                    md.append(f"  \n  > {loc}")
                md.append("\n")
        else:
            md.append("- _No specific strengths identified._\n")
        md.append("\n**What Fails:**\n\n")
        if wf:
            for item in wf:
                pt  = item.get("point", "") if isinstance(item, dict) else str(item)
                loc = item.get("location_ref", "") if isinstance(item, dict) else ""
                md.append(f"- {pt}\n")
                if loc and loc != "N/A":
                    md.append(f"  > Location → {loc.replace('Location -> ', '').replace('Location → ', '')}\n")
        else:
            md.append("- _No specific deficiencies identified._\n")
        md.append("\n")

    # Total + Grade + Audience Readiness (all in Section 2)
    md.append(f"**Total Score: {overall} / 100**  \n")
    md.append(f"**Grade: {_grade_badge(grade)}**\n\n")
    md.append(f"**Minister Ready:** {_ready(exec_comm.get('minister_ready', False))} — {exec_comm.get('minister_reason', 'Not assessed.')}  \n")
    md.append(f"**Board Ready:** {_ready(exec_comm.get('board_ready', False))} — {exec_comm.get('board_reason', 'Not assessed.')}  \n")
    md.append(f"**SWF Ready:** {_ready(exec_comm.get('swf_ready', False))} — {exec_comm.get('swf_reason', 'Not assessed.')}  \n\n")

    # 3. High-Risk Claims
    md.append("## 3. High-Risk and Unsupported Claims\n\n")
    bad = [c for c in claims.get("claims", [])
           if c.get("classification") in ("unsupported", "high_risk", "speculative")]
    if bad:
        md.append(
            f"_{len(bad)} claims flagged of {claims.get('total_claims', 0)} total. "
            f"Quantification ratio: {claims.get('quantification_ratio', 0)}%._\n\n"
        )
        for c in bad:
            cls = c.get("classification", "?").replace("_", " ").title()
            md.append(f"- **[{cls}]** {c.get('claim', '')}\n")
            if c.get("location_ref"):
                md.append(f"  > {c['location_ref']}\n")
            failed = [
                k.replace("_", " ")
                for k in ("evidence_provided", "data_provided", "source_referenced",
                          "quantified", "confidence_justified")
                if not c.get(k, False)
            ]
            if failed:
                md.append(f"  - Missing: {', '.join(failed)}\n")
    else:
        md.append("_No high-risk or unsupported claims detected._\n")
    md.append("\n")

    # 4–10. Findings sections
    md.append("## 4. Strengths\n\n")
    md.append(_render_located(recs.get("strengths", [])))

    md.append("## 5. General Weaknesses\n\n")
    md.append(_render_located(recs.get("weaknesses", [])))

    md.append("## 6. Data Gaps\n\n")
    md.append(_render_data_gaps(recs.get("data_gaps", [])))

    md.append("## 7. Weak Assumptions\n\n")
    md.append(_render_weak_assumptions(recs.get("weak_assumptions", [])))

    md.append("## 8. Writing Flaws\n\n")
    md.append(_render_writing_flaws(recs.get("writing_flaws", [])))

    md.append("## 9. Narrative Gaps\n\n")
    md.append(_render_located(recs.get("narrative_gaps", [])))

    md.append("## 10. Strategic Gaps\n\n")
    md.append(_render_located(recs.get("strategic_gaps", [])))

    md.append("## 11. Audience Relevance Gaps\n\n")
    md.append(_render_located(recs.get("audience_relevance_gaps", [])))

    # 12. Flagged Sections
    md.append("## 12. Sections Flagged for Executive Audiences\n\n")
    flagged = exec_comm.get("flagged_sections", [])
    if flagged:
        for f in flagged:
            md.append(f"- **{f.get('section', '')}**: {f.get('issue', '')}\n")
    else:
        md.append("_No specific sections flagged._\n")
    md.append("\n")

    # 13. Improvement Tasks
    md.append("## 13. Improvement Tasks\n\n")
    tasks = recs.get("improvement_tasks", [])
    if tasks:
        for i, t in enumerate(tasks, 1):
            md.append(_render_task(i, t))
    else:
        md.append(_none_note())

    return "".join(md)


def write_markdown(output_dir: Path, review_data: Dict[str, Any]) -> None:
    content = generate_markdown(review_data)
    path = output_dir / OUTPUT_FILES["review_md"]
    ok = write_text_safe(path, content)
    if ok:
        log.info("Markdown written: %s", path)
    else:
        log.error("Failed to write markdown: %s", path)

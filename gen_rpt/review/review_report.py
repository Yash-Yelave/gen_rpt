"""
review_report.py

Renders the full audit data into human-readable output files.

Output files produced:
  - review_report.md     — Full formatted audit report (never-empty sections)
  - review_summary.txt   — Concise executive text summary
  - review_report.json   — Master data file
  - improvement_tasks.json — Actionable task list only
  - claims.json          — Written separately by claim_extractor
"""
import json
from pathlib import Path
from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def _md_severity_badge(severity: str) -> str:
    badges = {
        "Critical": "🔴 **Critical**",
        "High":     "🟠 **High**",
        "Medium":   "🟡 **Medium**",
        "Low":      "🟢 **Low**",
    }
    return badges.get(severity, f"**{severity}**")


def _md_grade_badge(grade: str) -> str:
    badges = {
        "Gold":   "🥇 Gold",
        "Silver": "🥈 Silver",
        "Bronze": "🥉 Bronze",
        "Red":    "🔴 Red — Revision Required",
    }
    return badges.get(grade, grade)


def _md_readiness(flag: bool) -> str:
    return "✅ YES" if flag else "❌ NO"


def _section_header(title: str, level: int = 2) -> str:
    return f"{'#' * level} {title}\n"


def _none_note() -> str:
    return "_None identified in the report text reviewed._\n"


def _render_located_findings(items: List[Dict], label: str = "Finding") -> str:
    if not items:
        return _none_note()
    lines = []
    for item in items:
        finding = item.get("finding", item.get("issue", item.get("weakness", item.get("strength", ""))))
        loc     = item.get("location_ref", "N/A")
        sev     = item.get("severity", "Medium")
        lines.append(f"- {_md_severity_badge(sev)}: {finding}\n")
        if loc and loc != "N/A":
            lines.append(f"  - 📍 `{loc}`\n")
    return "".join(lines) + "\n"


def generate_markdown(review_data: Dict[str, Any]) -> str:
    scores  = review_data.get("scores", {})
    recs    = review_data.get("recommendations", {})
    claims  = review_data.get("claims_audit", {})
    title   = review_data.get("report_title", "Untitled Report")

    grade        = scores.get("grade", "N/A")
    overall      = scores.get("overall_score", "N/A")
    rq           = scores.get("research_quality", {})
    ec           = scores.get("evidence_and_citations", {})
    sc           = scores.get("strategic_clarity", {})
    ws           = scores.get("writing_and_structure", {})
    exec_comm    = recs.get("executive_communication", {})

    md = []
    md.append("# Institutional Research Audit Report\n")
    md.append(f"> **Report Reviewed:** {title}\n\n")

    # ─── 1. Executive Review ────────────────────────────────────────────────
    md.append(_section_header("1. Executive Review"))
    md.append(f"| Metric | Value |\n|--------|-------|\n")
    md.append(f"| **Overall Score** | **{overall} / 100** |\n")
    md.append(f"| **Grade** | {_md_grade_badge(grade)} |\n")
    md.append(f"| **Minister Ready** | {_md_readiness(exec_comm.get('minister_ready', False))} — {exec_comm.get('minister_reason', 'Not assessed.')} |\n")
    md.append(f"| **Board Ready** | {_md_readiness(exec_comm.get('board_ready', False))} — {exec_comm.get('board_reason', 'Not assessed.')} |\n")
    md.append(f"| **SWF Ready** | {_md_readiness(exec_comm.get('swf_ready', False))} — {exec_comm.get('swf_reason', 'Not assessed.')} |\n\n")

    # ─── 2. Scores & Justifications ─────────────────────────────────────────
    md.append(_section_header("2. Scores and Justifications"))

    for dim_key, dim_label in [
        ("research_quality",       "Research Quality"),
        ("evidence_and_citations", "Evidence and Citations"),
        ("strategic_clarity",      "Strategic Clarity"),
        ("writing_and_structure",  "Writing and Structure"),
    ]:
        dim = scores.get(dim_key, {})
        dim_score  = dim.get("score", "N/A")
        dim_max    = dim.get("max_points", "N/A")
        dim_just   = dim.get("justification", "Not evaluated.")
        pos_factors = dim.get("positive_factors") or []
        neg_factors = dim.get("negative_factors") or []

        md.append(f"### {dim_label}: {dim_score} / {dim_max}\n")
        md.append(f"**Justification:** {dim_just}\n\n")
        if pos_factors:
            md.append("**Strengths:**\n")
            for p in pos_factors:
                md.append(f"- {p}\n")
        if neg_factors:
            md.append("**Deficiencies:**\n")
            for n in neg_factors:
                md.append(f"- {n}\n")
        md.append("\n")

    # ─── 3. High-Risk & Unsupported Claims ───────────────────────────────────
    md.append(_section_header("3. High-Risk and Unsupported Claims"))
    all_claims: List[Dict] = claims.get("claims", [])
    bad_claims = [
        c for c in all_claims
        if c.get("classification") in ("unsupported", "high_risk", "speculative")
    ]

    if bad_claims:
        md.append(
            f"_{len(bad_claims)} claims flagged out of {claims.get('total_claims', 0)} "
            f"total. Quantification ratio: {claims.get('quantification_ratio', 0)}%._\n\n"
        )
        for c in bad_claims:
            cls_label = c.get("classification", "unknown").replace("_", " ").title()
            md.append(f"- **[{cls_label}]** {c.get('claim', '')}\n")
            loc = c.get("location_ref", "")
            if loc:
                md.append(f"  - 📍 `{loc}`\n")
            # Show which criteria failed
            failed = [
                k for k in ("evidence_provided", "data_provided",
                            "source_referenced", "quantified", "confidence_justified")
                if not c.get(k, False)
            ]
            if failed:
                md.append(f"  - ⚠️ Missing: {', '.join(f.replace('_', ' ') for f in failed)}\n")
        md.append("\n")
    else:
        md.append("_No high-risk or unsupported claims detected._\n\n")

    # ─── 4-11. Findings sections ─────────────────────────────────────────────
    sections_map = [
        ("4. Strengths",                     "strengths",              "located"),
        ("5. General Weaknesses",            "weaknesses",             "located"),
        ("6. Data Gaps",                     "data_gaps",              "data_gap"),
        ("7. Weak Assumptions",              "weak_assumptions",       "assumption"),
        ("8. Writing Flaws",                 "writing_flaws",          "writing"),
        ("9. Narrative and Strategic Gaps",  None,                     "narrative_strategic"),
        ("10. Audience Relevance Gaps",      "audience_relevance_gaps","located"),
        ("11. Executive Communication",      None,                     "exec_comm"),
        ("12. Improvement Tasks",            "improvement_tasks",      "tasks"),
    ]

    for heading, key, fmt in sections_map:
        md.append(_section_header(heading))

        if fmt == "located":
            items = recs.get(key, [])
            md.append(_render_located_findings(items))

        elif fmt == "data_gap":
            items = recs.get(key, [])
            if not items:
                md.append(_none_note())
            else:
                for gap in items:
                    sev  = gap.get("severity", "Medium")
                    sect = gap.get("section", "Unknown")
                    clm  = gap.get("claim", "")
                    miss = gap.get("missing_data", [])
                    loc  = gap.get("location_ref", "N/A")
                    md.append(f"- {_md_severity_badge(sev)} **[{sect}]** {clm}\n")
                    if miss:
                        md.append(f"  - Missing: {', '.join(miss)}\n")
                    if loc and loc != "N/A":
                        md.append(f"  - 📍 `{loc}`\n")
                md.append("\n")

        elif fmt == "assumption":
            items = recs.get(key, [])
            if not items:
                md.append(_none_note())
            else:
                for wa in items:
                    sev   = wa.get("severity", "Medium")
                    claim = wa.get("forecast_or_claim", "")
                    miss  = wa.get("missing_evidence", "")
                    loc   = wa.get("location_ref", "N/A")
                    md.append(f"- {_md_severity_badge(sev)}: {claim}\n")
                    if miss:
                        md.append(f"  - Missing evidence: {miss}\n")
                    if loc and loc != "N/A":
                        md.append(f"  - 📍 `{loc}`\n")
                md.append("\n")

        elif fmt == "writing":
            items = recs.get(key, [])
            if not items:
                md.append(_none_note())
            else:
                for wf in items:
                    sev  = wf.get("severity", "Medium")
                    ftype = wf.get("flaw_type", "")
                    ex   = wf.get("example", "")
                    loc  = wf.get("location_ref", "N/A")
                    md.append(f"- {_md_severity_badge(sev)} **{ftype}**\n")
                    if ex:
                        md.append(f"  - Example: _\"{ex}\"_\n")
                    if loc and loc != "N/A":
                        md.append(f"  - 📍 `{loc}`\n")
                md.append("\n")

        elif fmt == "narrative_strategic":
            nar_items = recs.get("narrative_gaps", [])
            strat_items = recs.get("strategic_gaps", [])
            if not nar_items and not strat_items:
                md.append(_none_note())
            else:
                if nar_items:
                    md.append("**Narrative Gaps:**\n")
                    md.append(_render_located_findings(nar_items))
                if strat_items:
                    md.append("**Strategic Gaps:**\n")
                    md.append(_render_located_findings(strat_items))

        elif fmt == "exec_comm":
            flagged = exec_comm.get("flagged_sections", [])
            if flagged:
                md.append("**Flagged Sections for Executive Audiences:**\n")
                for flag in flagged:
                    md.append(f"- **{flag.get('section', '')}**: {flag.get('issue', '')}\n")
            else:
                md.append("_No specific sections flagged for executive audience readiness._\n")
            md.append("\n")

        elif fmt == "tasks":
            tasks = recs.get(key, [])
            if not tasks:
                md.append(_none_note())
            else:
                for i, task in enumerate(tasks, 1):
                    pri   = task.get("priority", "Medium")
                    sect  = task.get("section", "General")
                    issue = task.get("issue", "")
                    fix   = task.get("fix", "")
                    impact = task.get("expected_impact", "")
                    md.append(f"### Task {i}: {_md_severity_badge(pri)} — {sect}\n")
                    md.append(f"**Issue:** {issue}\n\n")
                    md.append(f"**Fix:** {fix}\n\n")
                    md.append(f"**Expected Impact:** {impact}\n\n")

    return "".join(md)


# ---------------------------------------------------------------------------
# Text summary renderer
# ---------------------------------------------------------------------------

def generate_txt_summary(review_data: Dict[str, Any]) -> str:
    scores  = review_data.get("scores", {})
    recs    = review_data.get("recommendations", {})
    claims  = review_data.get("claims_audit", {})

    grade   = scores.get("grade", "N/A")
    overall = scores.get("overall_score", "N/A")
    title   = review_data.get("report_title", "Untitled Report")

    exec_comm = recs.get("executive_communication", {})
    min_r = "YES" if exec_comm.get("minister_ready") else "NO"
    brd_r = "YES" if exec_comm.get("board_ready")    else "NO"
    swf_r = "YES" if exec_comm.get("swf_ready")      else "NO"

    top_strengths = [
        s.get("finding", "") for s in recs.get("strengths", [])[:3]
    ]
    top_tasks = recs.get("improvement_tasks", [])[:3]

    bad_count = (
        claims.get("unsupported_count", 0) + claims.get("high_risk_count", 0)
    )

    lines = [
        "GROQ AI INSTITUTIONAL AUDIT SUMMARY",
        "=" * 40,
        f"Report: {title}",
        f"Grade:  {grade}",
        f"Score:  {overall} / 100",
        "",
        f"Minister Ready: {min_r}  |  Board Ready: {brd_r}  |  SWF Ready: {swf_r}",
        "",
        f"Claims Audited: {claims.get('total_claims', 0)} | "
        f"High-Risk / Unsupported: {bad_count}",
        f"Quantification Ratio: {claims.get('quantification_ratio', 0)}%",
        "",
        "TOP STRENGTHS:",
    ]
    for s in top_strengths:
        lines.append(f"  - {s}")
    if not top_strengths:
        lines.append("  - None identified.")

    lines.append("")
    lines.append("PRIORITY IMPROVEMENT TASKS:")
    for t in top_tasks:
        lines.append(
            f"  - [{t.get('priority', 'Medium')}] {t.get('section', 'General')}: "
            f"{t.get('issue', '')}"
        )
    if not top_tasks:
        lines.append("  - None generated.")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Artifact writer
# ---------------------------------------------------------------------------

def generate_review_artifacts(
    output_dir: Path,
    review_data: Dict[str, Any],
) -> None:
    """
    Write all review output files to output_dir.

    Files written:
      review_report.json
      review_report.md
      review_summary.txt
      improvement_tasks.json
    (claims.json is written by claim_extractor independently)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Master JSON
    json_path = output_dir / "review_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)

    # 2. Markdown report
    md_content = generate_markdown(review_data)
    md_path = output_dir / "review_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 3. Text summary
    txt_content = generate_txt_summary(review_data)
    txt_path = output_dir / "review_summary.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    # 4. Improvement tasks only
    tasks = review_data.get("recommendations", {}).get("improvement_tasks", [])
    tasks_path = output_dir / "improvement_tasks.json"
    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    # 5. Update manifest if it exists (pipeline mode)
    manifest_path = output_dir / "manifest.json"
    manifest: Dict[str, Any] = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            pass

    scores = review_data.get("scores", {})
    manifest["ai_review_score"] = scores.get("overall_score")
    manifest["ai_review_grade"] = scores.get("grade")
    manifest["review_timestamp"] = review_data.get("timestamp")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(
        f"[REVIEW] Artifacts written to {output_dir}:\n"
        f"         review_report.md | review_report.json | "
        f"review_summary.txt | improvement_tasks.json"
    )

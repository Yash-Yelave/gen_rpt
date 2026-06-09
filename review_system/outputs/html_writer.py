"""
review_system/outputs/html_writer.py

Renders the ReviewData into a self-contained, styled HTML review report.
No external assets — all CSS is inline. Opens cleanly in any browser.
"""
from pathlib import Path
from typing import Dict, Any, List

from review_system.config.review_config import OUTPUT_FILES
from review_system.utils.file_utils import write_text_safe
from review_system.utils.logging_utils import get_generation_logger

log = get_generation_logger()

_CSS = """
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         max-width: 960px; margin: 40px auto; padding: 0 24px;
         background: #0f1117; color: #e1e4e8; line-height: 1.7; }
  h1 { color: #58a6ff; border-bottom: 2px solid #21262d; padding-bottom: 12px; }
  h2 { color: #79c0ff; margin-top: 40px; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
  h3 { color: #b8d0ff; margin-top: 24px; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; }
  th, td { padding: 10px 14px; border: 1px solid #30363d; text-align: left; }
  th { background: #161b22; color: #58a6ff; }
  tr:nth-child(even) { background: #161b22; }
  .badge-critical { color: #ff7b72; font-weight: 700; }
  .badge-high     { color: #ffa657; font-weight: 700; }
  .badge-medium   { color: #e3b341; font-weight: 700; }
  .badge-low      { color: #3fb950; font-weight: 700; }
  .location       { font-size: 0.82em; color: #8b949e; font-family: monospace;
                    background: #161b22; padding: 4px 8px; border-radius: 4px;
                    display: inline-block; margin: 4px 0; }
  .task-card      { background: #161b22; border: 1px solid #30363d;
                    border-radius: 8px; padding: 16px 20px; margin: 12px 0; }
  .task-card h4   { margin: 0 0 8px 0; color: #79c0ff; }
  blockquote      { border-left: 3px solid #30363d; margin: 8px 0; padding: 4px 12px;
                    color: #8b949e; font-style: italic; }
  .score-bar      { height: 8px; border-radius: 4px; background: #21262d;
                    margin: 4px 0 12px 0; }
  .score-fill     { height: 100%; border-radius: 4px; background: #58a6ff; }
  hr              { border: none; border-top: 1px solid #21262d; margin: 32px 0; }
  .claim-block    { background: #161b22; border-left: 3px solid #ff7b72;
                    padding: 8px 12px; margin: 8px 0; border-radius: 0 4px 4px 0; }
"""


def _sev_class(s: str) -> str:
    return {"Critical": "badge-critical", "High": "badge-high",
            "Medium": "badge-medium", "Low": "badge-low"}.get(s, "badge-medium")


def _sev_label(s: str) -> str:
    return f'<span class="{_sev_class(s)}">[{s}]</span>'


def _esc(text: str) -> str:
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def _loc(ref: str) -> str:
    if ref and ref != "N/A":
        return f'<div class="location">{_esc(ref)}</div>'
    return ""


def _render_located_html(items: List[Dict]) -> str:
    if not items:
        return "<p><em>None identified.</em></p>"
    rows = []
    for item in items:
        text = (item.get("finding") or item.get("issue") or "")
        sev  = item.get("severity", "Medium")
        loc  = item.get("location_ref", "")
        rows.append(
            f"<li>{_sev_label(sev)} {_esc(text)}{_loc(loc)}</li>"
        )
    return "<ul>" + "".join(rows) + "</ul>"


def _score_bar(score: int, max_pts: int) -> str:
    pct = round((score / max_pts) * 100) if max_pts else 0
    return (
        f'<div class="score-bar"><div class="score-fill" style="width:{pct}%"></div></div>'
    )


def generate_html(review_data: Dict[str, Any]) -> str:
    scores    = review_data.get("scores", {})
    recs      = review_data.get("recommendations", {})
    claims    = review_data.get("claims_audit", {})
    title     = _esc(review_data.get("report_title", "Untitled Report"))
    ts        = review_data.get("timestamp", "")
    grade     = scores.get("grade", "N/A")
    overall   = scores.get("overall_score", 0)
    exec_comm = recs.get("executive_communication", {})
    rq = scores.get("research_quality", {})
    ec = scores.get("evidence_and_citations", {})
    sc = scores.get("strategic_clarity", {})
    ws = scores.get("writing_and_structure", {})

    grade_color = {"Gold": "#e3b341", "Silver": "#8b949e",
                   "Bronze": "#d18b47", "Red": "#ff7b72"}.get(grade, "#8b949e")

    parts: List[str] = [f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audit Report — {title}</title>
  <style>{_CSS}</style>
</head>
<body>
<h1>Institutional Research Audit Report</h1>
<p><strong>Report:</strong> {title}<br>
<strong>Timestamp:</strong> {_esc(ts)}</p>
<hr>

<h2>1. Executive Review</h2>
<table>
  <tr><th>Metric</th><th>Value</th></tr>
  <tr><td><strong>Overall Score</strong></td>
      <td><strong style="font-size:1.4em;color:{grade_color}">{overall} / 100</strong></td></tr>
  <tr><td><strong>Grade</strong></td>
      <td style="color:{grade_color};font-weight:700">{grade}</td></tr>
  <tr><td><strong>Minister Ready</strong></td>
      <td>{'YES' if exec_comm.get('minister_ready') else 'NO'} — {_esc(exec_comm.get('minister_reason',''))}</td></tr>
  <tr><td><strong>Board Ready</strong></td>
      <td>{'YES' if exec_comm.get('board_ready') else 'NO'} — {_esc(exec_comm.get('board_reason',''))}</td></tr>
  <tr><td><strong>SWF Ready</strong></td>
      <td>{'YES' if exec_comm.get('swf_ready') else 'NO'} — {_esc(exec_comm.get('swf_reason',''))}</td></tr>
</table>

<h2>2. Scores and Justifications</h2>
"""]

    for dim_label, dim_data in [
        ("Research Quality", rq),
        ("Evidence and Citations", ec),
        ("Strategic Clarity", sc),
        ("Writing and Structure", ws),
    ]:
        s   = dim_data.get("score", 0)
        mx  = dim_data.get("max_points", 0)
        jst = _esc(dim_data.get("justification", "Not evaluated."))
        pos = dim_data.get("positive_factors") or []
        neg = dim_data.get("negative_factors") or []
        parts.append(f"<h3>{dim_label}: {s} / {mx}</h3>")
        parts.append(_score_bar(s, mx))
        parts.append(f"<p><strong>Justification:</strong> {jst}</p>")
        if pos:
            parts.append("<p><strong>Strengths:</strong></p><ul>" +
                         "".join(f"<li>{_esc(p)}</li>" for p in pos) + "</ul>")
        if neg:
            parts.append("<p><strong>Deficiencies:</strong></p><ul>" +
                         "".join(f"<li>{_esc(n)}</li>" for n in neg) + "</ul>")

    # High-risk claims
    bad = [c for c in claims.get("claims", [])
           if c.get("classification") in ("unsupported", "high_risk", "speculative")]
    parts.append("<h2>3. High-Risk and Unsupported Claims</h2>")
    if bad:
        parts.append(f"<p><em>{len(bad)} of {claims.get('total_claims',0)} claims flagged. "
                     f"Quantification: {claims.get('quantification_ratio',0)}%.</em></p>")
        for c in bad:
            cls  = _esc(c.get("classification", "?").replace("_", " ").title())
            text = _esc(c.get("claim", ""))
            loc  = _loc(c.get("location_ref", ""))
            parts.append(
                f'<div class="claim-block"><strong>[{cls}]</strong> {text}{loc}</div>'
            )
    else:
        parts.append("<p><em>No high-risk claims detected.</em></p>")

    # Findings sections
    for num, heading, key, renderer in [
        (4,  "Strengths",              "strengths",              "located"),
        (5,  "General Weaknesses",     "weaknesses",             "located"),
        (6,  "Narrative Gaps",         "narrative_gaps",         "located"),
        (7,  "Strategic Gaps",         "strategic_gaps",         "located"),
        (8,  "Audience Relevance Gaps","audience_relevance_gaps","located"),
    ]:
        parts.append(f"<h2>{num}. {heading}</h2>")
        parts.append(_render_located_html(recs.get(key, [])))

    # Data gaps
    parts.append("<h2>9. Data Gaps</h2>")
    dg = recs.get("data_gaps", [])
    if dg:
        rows = []
        for g in dg:
            miss = ", ".join(g.get("missing_data", []))
            rows.append(
                f"<li>{_sev_label(g.get('severity','Medium'))} "
                f"<strong>[{_esc(g.get('section',''))}]</strong> {_esc(g.get('claim',''))}"
                f"<br><small>Missing: {_esc(miss)}</small>{_loc(g.get('location_ref',''))}</li>"
            )
        parts.append("<ul>" + "".join(rows) + "</ul>")
    else:
        parts.append("<p><em>None identified.</em></p>")

    # Writing flaws
    parts.append("<h2>10. Writing Flaws</h2>")
    wf = recs.get("writing_flaws", [])
    if wf:
        rows = []
        for w in wf:
            ex   = _esc(w.get("example", ""))
            sugg = _esc(w.get("suggestion", ""))
            rows.append(
                f"<li>{_sev_label(w.get('severity','Medium'))} "
                f"<strong>{_esc(w.get('flaw_type',''))}</strong>"
                + (f"<blockquote>{ex}</blockquote>" if ex else "")
                + (f"<small>Fix: {sugg}</small>" if sugg else "")
                + _loc(w.get("location_ref", ""))
                + "</li>"
            )
        parts.append("<ul>" + "".join(rows) + "</ul>")
    else:
        parts.append("<p><em>None identified.</em></p>")

    # Weak assumptions
    parts.append("<h2>11. Weak Assumptions</h2>")
    wa = recs.get("weak_assumptions", [])
    if wa:
        rows = []
        for w in wa:
            rows.append(
                f"<li>{_sev_label(w.get('severity','Medium'))} {_esc(w.get('forecast_or_claim',''))}"
                f"<br><small>Missing evidence: {_esc(w.get('missing_evidence',''))}</small>"
                + _loc(w.get("location_ref","")) + "</li>"
            )
        parts.append("<ul>" + "".join(rows) + "</ul>")
    else:
        parts.append("<p><em>None identified.</em></p>")

    # Improvement tasks
    parts.append("<h2>12. Improvement Tasks</h2>")
    tasks = recs.get("improvement_tasks", [])
    if tasks:
        for i, t in enumerate(tasks, 1):
            pri   = t.get("priority", "Medium")
            sect  = _esc(t.get("section", "General"))
            issue = _esc(t.get("issue", ""))
            fix   = _esc(t.get("fix", ""))
            imp   = _esc(t.get("expected_impact", ""))
            parts.append(
                f'<div class="task-card">'
                f'<h4>Task {i}: {_sev_label(pri)} — {sect}</h4>'
                f'<p><strong>Issue:</strong> {issue}</p>'
                f'<p><strong>Fix:</strong> {fix}</p>'
                f'<p><strong>Expected Impact:</strong> {imp}</p>'
                f'</div>'
            )
    else:
        parts.append("<p><em>No improvement tasks generated.</em></p>")

    parts.append("</body>\n</html>")
    return "\n".join(parts)


def write_html(output_dir: Path, review_data: Dict[str, Any]) -> None:
    content = generate_html(review_data)
    path = output_dir / OUTPUT_FILES["review_html"]
    ok = write_text_safe(path, content)
    if ok:
        log.info("HTML written: %s", path)
    else:
        log.error("Failed to write HTML: %s", path)

import json
from pathlib import Path
from typing import Dict, Any

def _generate_markdown_content(review_data: Dict[str, Any], recs: Dict[str, Any]) -> str:
    md_content = f"""# Institutional Research Audit Report

## Executive Review
**Overall Score**: {review_data.get('scores', {}).get('overall_score', 'N/A')} / 100
**Grade**: {review_data.get('scores', {}).get('grade', 'N/A')}

## Section Scores
"""
    section_scores = review_data.get('scores', {}).get('components', [])
    if isinstance(section_scores, list):
        for sec in section_scores:
            md_content += f"### {sec.get('section_name', 'Section')}\n"
            md_content += f"- **Evidence Strength**: {sec.get('evidence_strength', 'N/A')}\n\n"
            for ev_key, label in [("research_evaluation", "Research Score"), ("evidence_evaluation", "Evidence Score"), ("writing_evaluation", "Writing Score"), ("strategic_evaluation", "Strategic Score")]:
                ev = sec.get(ev_key, {})
                if not isinstance(ev, dict):
                    continue
                score = ev.get('score', 'N/A')
                conf = ev.get('confidence', 'N/A')
                md_content += f"#### {label}: {score} (Confidence: {conf})\n"
                
                pos = ev.get('positive_factors', [])
                if pos:
                    md_content += "**Positive Factors**:\n"
                    for p in pos:
                        md_content += f"- {p}\n"
                        
                neg = ev.get('negative_factors', [])
                if neg:
                    md_content += "**Negative Factors**:\n"
                    for n in neg:
                        md_content += f"- {n}\n"
                        
                brk = ev.get('score_breakdown', {})
                if brk:
                    md_content += "**Score Breakdown**:\n"
                    for k, v in brk.items():
                        md_content += f"- {k}: {v}\n"
                md_content += "\n"
    
    claims_data = review_data.get('claims', {})
    if isinstance(claims_data, dict):
        md_content += f"\n**Quantification Ratio**: {claims_data.get('quantification_ratio', 'N/A')}%\n"
        claims_list = claims_data.get('claims', [])
    else:
        claims_list = claims_data
        
    md_content += "\n## High-Risk & Unsupported Claims\n"
    for c in claims_list:
        if isinstance(c, dict) and c.get('classification') in ["High-Risk", "Unsupported"]:
            md_content += f"- **{c.get('classification')}** ({c.get('section', 'General')}): {c.get('claim', '')}\n"

    md_content += "\n## Strengths\n"
    for s in recs.get('strengths', []):
        md_content += f"- **{s.get('section', 'General')}**: {s.get('strength', '')}\n  - *Evidence*: {s.get('evidence', '')}\n"

    md_content += "\n## General Weaknesses\n"
    for w in recs.get('weaknesses', []):
        md_content += f"- **{w.get('section', 'General')}**: {w.get('weakness', '')}\n  - *Evidence*: {w.get('evidence', '')}\n"

    md_content += "\n## Data Gaps\n"
    for gap in recs.get('data_gaps', []):
        md_content += f"- **[{gap.get('severity', 'Medium')}]** ({gap.get('section', 'General')}): {gap.get('claim', '')}\n  - *Missing Data*: {', '.join(gap.get('missing_data', []))}\n"

    md_content += "\n## Weak Assumptions\n"
    for wa in recs.get('weak_assumptions', []):
        md_content += f"- **[{wa.get('severity', 'Medium')}]**: {wa.get('forecast', '')}\n  - *Missing Evidence*: {wa.get('missing_evidence', '')}\n"

    md_content += "\n## Writing Flaws\n"
    for wf in recs.get('writing_flaws', []):
        md_content += f"- **[{wf.get('severity', 'Medium')}] {wf.get('type', '')}** ({wf.get('section', '')}): \"{wf.get('example', '')}\"\n"

    md_content += "\n## Narrative & Strategic Gaps\n"
    for ng in recs.get('narrative_gaps', []):
        md_content += f"- **Narrative [{ng.get('severity', 'Medium')}]**: {ng.get('issue', '')}\n"
    for sg in recs.get('strategic_gaps', []):
        md_content += f"- **Strategic [{sg.get('severity', 'Medium')}]**: Missing Question - {sg.get('missing_question', '')}\n  - *Explanation*: {sg.get('explanation', '')}\n"

    md_content += "\n## GCC Relevance Gaps\n"
    for gcc in recs.get('gcc_relevance_gaps', []):
        md_content += f"- **{gcc.get('section', 'General')}**: {gcc.get('issue', '')}\n"

    exec_comm = recs.get('executive_communication', {})
    md_content += f"\n## Executive Communication\n"
    md_content += f"- Minister Ready: {exec_comm.get('minister_ready', False)}\n"
    md_content += f"- Board Ready: {exec_comm.get('board_ready', False)}\n"
    md_content += f"- SWF Ready: {exec_comm.get('swf_ready', False)}\n"
    md_content += f"**Flagged Sections**:\n"
    for flag in exec_comm.get('flagged_sections', []):
        md_content += f"  - {flag.get('section', '')}: {flag.get('issue', '')}\n"

    md_content += "\n## Improvement Tasks\n"
    for task in recs.get('improvement_tasks', []):
        md_content += f"### [{task.get('severity', 'Medium')}] {task.get('issue', 'Issue')} ({task.get('section', 'General')})\n"
        md_content += f"- **Recommended Fix**: {task.get('recommended_fix', '')}\n"
        md_content += f"- **Expected Impact**: {task.get('expected_impact', '')}\n"

    return md_content

def _generate_txt_content(review_data: Dict[str, Any], recs: Dict[str, Any]) -> str:
    txt_content = f"""GROQ AI AUDIT SUMMARY
----------------------
Grade: {review_data.get('scores', {}).get('grade')}
Score: {review_data.get('scores', {}).get('overall_score')}/100

Top Strengths:
{chr(10).join(f"- {s.get('strength', '')}" for s in recs.get('strengths', [])[:3])}

Priority Improvement Tasks:
{chr(10).join(f"- [{t.get('severity', 'Medium')}] {t.get('issue', '')}" for t in recs.get('improvement_tasks', [])[:3])}
"""
    return txt_content

def generate_review_artifacts(output_dir: Path, report_payload: Dict, review_data: Dict[str, Any]):
    # 1. review_report.json
    report_json_path = output_dir / "review_report.json"
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)
        
    # 2. Manifest Append
    manifest_path = output_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except:
            pass
            
    manifest["ai_review_score"] = review_data.get("scores", {}).get("overall_score")
    manifest["ai_review_grade"] = review_data.get("scores", {}).get("grade")
    manifest["review_timestamp"] = review_data.get("timestamp")
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    recs = review_data.get('recommendations', {})
    
    # 3. improvement_tasks.json
    imp_tasks_path = output_dir / "improvement_tasks.json"
    with open(imp_tasks_path, 'w', encoding='utf-8') as f:
        json.dump(recs.get('improvement_tasks', []), f, ensure_ascii=False, indent=2)

    # 4. review_report.md
    md_content = _generate_markdown_content(review_data, recs)
    md_path = output_dir / "review_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 5. review_summary.txt
    txt_content = _generate_txt_content(review_data, recs)
    txt_path = output_dir / "review_summary.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)


def generate_review_artifacts_text(output_dir: Path, text: str, review_data: Dict[str, Any]):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. review_report.json
    report_json_path = output_dir / "review_report.json"
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)
        
    recs = review_data.get('recommendations', {})
    
    # 2. improvement_tasks.json
    imp_tasks_path = output_dir / "improvement_tasks.json"
    with open(imp_tasks_path, 'w', encoding='utf-8') as f:
        json.dump(recs.get('improvement_tasks', []), f, ensure_ascii=False, indent=2)

    # 3. review_report.md
    md_content = _generate_markdown_content(review_data, recs)
    md_path = output_dir / "review_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 4. review_summary.txt
    txt_content = _generate_txt_content(review_data, recs)
    txt_path = output_dir / "review_summary.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)

import json
from pathlib import Path
from typing import Dict, Any

def generate_review_artifacts(output_dir: Path, report_payload: Dict, review_data: Dict[str, Any]):
    # 1. review_report.json
    report_json_path = output_dir / "review_report.json"
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)
        
    # 2. Manifest Append (read existing, append fields)
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
        
    # 3. review_report.md
    recs = review_data.get('recommendations', {})
    exec_readiness = recs.get('executive_readiness', {})
    
    md_content = f"""# Groq AI Review Report

## Executive Review
**Overall Score**: {review_data.get('scores', {{}}).get('overall_score')} / 100
**Grade**: {review_data.get('scores', {{}}).get('grade')}

## Category Scores
- Research Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('research_quality')}
- Strategic Insight: {review_data.get('scores', {{}}).get('components', {{}}).get('strategic_insight')}
- Source Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('source_quality')}
- Writing Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('writing_quality')}
- Design Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('design_quality')}
- Executive Readiness: {review_data.get('scores', {{}}).get('components', {{}}).get('executive_readiness')}

## Strengths
{chr(10).join(f"- {s}" for s in recs.get('strengths', []))}

## Weaknesses
{chr(10).join(f"- {s}" for s in recs.get('weaknesses', []))}

## Priority Improvements
"""
    for imp in recs.get('priority_improvements', []):
        md_content += f"""
### [{imp.get('priority_level', 'Medium')}] {imp.get('issue', 'Issue')}
- **Impact**: {imp.get('impact', '')}
- **Suggested Fix**: {imp.get('suggested_fix', '')}
"""
        
    md_content += f"""
## Executive Readiness Assessment
- Board Members: {'Yes' if exec_readiness.get('board_members') else 'No'}
- Ministers: {'Yes' if exec_readiness.get('ministers') else 'No'}
- CEOs: {'Yes' if exec_readiness.get('ceos') else 'No'}
- Sovereign Wealth Funds: {'Yes' if exec_readiness.get('sovereign_wealth_funds') else 'No'}
- Senior Executives: {'Yes' if exec_readiness.get('senior_executives') else 'No'}

**Justification**: {exec_readiness.get('justification', '')}
"""

    md_path = output_dir / "review_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 4. review_summary.txt
    txt_content = f"""GROQ AI REVIEW SUMMARY
----------------------
Grade: {review_data.get('scores', {{}}).get('grade')}
Score: {review_data.get('scores', {{}}).get('overall_score')}/100

Top Strengths:
{chr(10).join(f"- {s}" for s in recs.get('strengths', [])[:3])}

Top Weaknesses:
{chr(10).join(f"- {s}" for s in recs.get('weaknesses', [])[:3])}

Executive Readiness Justification:
{exec_readiness.get('justification', '')}
"""
    txt_path = output_dir / "review_summary.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)


def generate_review_artifacts_text(output_dir: Path, text: str, review_data: Dict[str, Any]):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. review_report.json
    report_json_path = output_dir / "review_report.json"
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)
        
    # 2. review_report.md
    recs = review_data.get('recommendations', {})
    exec_readiness = recs.get('executive_readiness', {})
    
    md_content = f"""# Groq AI Review Report

## Executive Review
**Overall Score**: {review_data.get('scores', {{}}).get('overall_score')} / 100
**Grade**: {review_data.get('scores', {{}}).get('grade')}

## Category Scores
- Research Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('research_quality')}
- Strategic Insight: {review_data.get('scores', {{}}).get('components', {{}}).get('strategic_insight')}
- Source Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('source_quality')}
- Writing Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('writing_quality')}
- Design Quality: {review_data.get('scores', {{}}).get('components', {{}}).get('design_quality')}
- Executive Readiness: {review_data.get('scores', {{}}).get('components', {{}}).get('executive_readiness')}

## Strengths
{chr(10).join(f"- {s}" for s in recs.get('strengths', []))}

## Weaknesses
{chr(10).join(f"- {s}" for s in recs.get('weaknesses', []))}

## Priority Improvements
"""
    for imp in recs.get('priority_improvements', []):
        md_content += f"""
### [{imp.get('priority_level', 'Medium')}] {imp.get('issue', 'Issue')}
- **Impact**: {imp.get('impact', '')}
- **Suggested Fix**: {imp.get('suggested_fix', '')}
"""
        
    md_content += f"""
## Executive Readiness Assessment
- Board Members: {'Yes' if exec_readiness.get('board_members') else 'No'}
- Ministers: {'Yes' if exec_readiness.get('ministers') else 'No'}
- CEOs: {'Yes' if exec_readiness.get('ceos') else 'No'}
- Sovereign Wealth Funds: {'Yes' if exec_readiness.get('sovereign_wealth_funds') else 'No'}
- Senior Executives: {'Yes' if exec_readiness.get('senior_executives') else 'No'}

**Justification**: {exec_readiness.get('justification', '')}
"""

    md_path = output_dir / "review_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 3. review_summary.txt
    txt_content = f"""GROQ AI REVIEW SUMMARY
----------------------
Grade: {review_data.get('scores', {{}}).get('grade')}
Score: {review_data.get('scores', {{}}).get('overall_score')}/100

Top Strengths:
{chr(10).join(f"- {s}" for s in recs.get('strengths', [])[:3])}

Top Weaknesses:
{chr(10).join(f"- {s}" for s in recs.get('weaknesses', [])[:3])}

Executive Readiness Justification:
{exec_readiness.get('justification', '')}
"""
    txt_path = output_dir / "review_summary.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)

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
**Overall Score**: {review_data.get('scores', {}).get('overall_score')} / 100
**Grade**: {review_data.get('scores', {}).get('grade')}

## Category Scores
- Research Coverage: {review_data.get('scores', {}).get('components', {}).get('research_coverage')}
- Evidence Quality: {review_data.get('scores', {}).get('components', {}).get('evidence_quality')}
- Citation Strength: {review_data.get('scores', {}).get('components', {}).get('citation_strength')}
- Structure: {review_data.get('scores', {}).get('components', {}).get('structure')}
- Readability: {review_data.get('scores', {}).get('components', {}).get('readability')}
- Strategic Clarity: {review_data.get('scores', {}).get('components', {}).get('strategic_clarity')}
- Recommendation Quality: {review_data.get('scores', {}).get('components', {}).get('recommendation_quality')}
- Visual Presentation: {review_data.get('scores', {}).get('components', {}).get('visual_presentation')}

## Strengths
"""
    for s in recs.get('strengths', []):
        md_content += f"- **{s.get('section', 'General')}**: {s.get('strength', '')}\n  - *Evidence*: {s.get('evidence', '')}\n"

    md_content += "\n## Weaknesses\n"
    for w in recs.get('weaknesses', []):
        md_content += f"- **{w.get('section', 'General')}**: {w.get('weakness', '')}\n  - *Evidence*: {w.get('evidence', '')}\n"

    md_content += "\n## Recommendations\n"
    for r in recs.get('recommendations', []):
        md_content += f"- **Target Section**: {r.get('affected_section', 'General')}\n  - *Recommendation*: {r.get('recommendation', '')}\n  - *Reason*: {r.get('reason', '')}\n"


    md_path = output_dir / "review_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 4. review_summary.txt
    txt_content = f"""GROQ AI REVIEW SUMMARY
----------------------
Grade: {review_data.get('scores', {}).get('grade')}
Score: {review_data.get('scores', {}).get('overall_score')}/100

Top Strengths:
{chr(10).join(f"- {s.get('strength', '')}" for s in recs.get('strengths', [])[:3])}

Top Weaknesses:
{chr(10).join(f"- {w.get('weakness', '')}" for w in recs.get('weaknesses', [])[:3])}
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
**Overall Score**: {review_data.get('scores', {}).get('overall_score')} / 100
**Grade**: {review_data.get('scores', {}).get('grade')}

## Category Scores
- Research Coverage: {review_data.get('scores', {}).get('components', {}).get('research_coverage')}
- Evidence Quality: {review_data.get('scores', {}).get('components', {}).get('evidence_quality')}
- Citation Strength: {review_data.get('scores', {}).get('components', {}).get('citation_strength')}
- Structure: {review_data.get('scores', {}).get('components', {}).get('structure')}
- Readability: {review_data.get('scores', {}).get('components', {}).get('readability')}
- Strategic Clarity: {review_data.get('scores', {}).get('components', {}).get('strategic_clarity')}
- Recommendation Quality: {review_data.get('scores', {}).get('components', {}).get('recommendation_quality')}
- Visual Presentation: {review_data.get('scores', {}).get('components', {}).get('visual_presentation')}

## Strengths
"""
    for s in recs.get('strengths', []):
        md_content += f"- **{s.get('section', 'General')}**: {s.get('strength', '')}\n  - *Evidence*: {s.get('evidence', '')}\n"

    md_content += "\n## Weaknesses\n"
    for w in recs.get('weaknesses', []):
        md_content += f"- **{w.get('section', 'General')}**: {w.get('weakness', '')}\n  - *Evidence*: {w.get('evidence', '')}\n"

    md_content += "\n## Recommendations\n"
    for r in recs.get('recommendations', []):
        md_content += f"- **Target Section**: {r.get('affected_section', 'General')}\n  - *Recommendation*: {r.get('recommendation', '')}\n  - *Reason*: {r.get('reason', '')}\n"


    md_path = output_dir / "review_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 3. review_summary.txt
    txt_content = f"""GROQ AI REVIEW SUMMARY
----------------------
Grade: {review_data.get('scores', {}).get('grade')}
Score: {review_data.get('scores', {}).get('overall_score')}/100

Top Strengths:
{chr(10).join(f"- {s.get('strength', '')}" for s in recs.get('strengths', [])[:3])}

Top Weaknesses:
{chr(10).join(f"- {w.get('weakness', '')}" for w in recs.get('weaknesses', [])[:3])}
"""
    txt_path = output_dir / "review_summary.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)

import json
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .groq_reviewer import GroqClient

def evaluate_dimensions(client: 'GroqClient', report_payload_path: Path, sources_path: Path, html_path: Path) -> Dict[str, Any]:
    try:
        with open(report_payload_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        with open(sources_path, 'r', encoding='utf-8') as f:
            sources = json.load(f)
    except Exception as e:
        return {}

    system = "You are an elite Strategy Consultant and Report Auditor. Return strict JSON only."
    user = f"""
Evaluate the provided report based on the following 10 dimensions:
1. Research Quality
2. Strategic Insight Quality
3. Executive Readability (Writing Quality)
4. Source Quality
5. Evidence Strength
6. Recommendation Quality
7. Report Structure
8. Design Quality (based on metadata and structure)
9. Decision-Making Usefulness
10. Overall Executive Readiness

Provide a score (0-100) and a brief rationale for each.

Report Data Snippet:
{json.dumps(report, ensure_ascii=False)[:20000]}

Sources Snippet:
{json.dumps(sources, ensure_ascii=False)[:10000]}

Return JSON format:
{{
  "research_quality": {{"score": 85, "rationale": "..."}},
  "strategic_insight": {{"score": 88, "rationale": "..."}},
  "executive_readability": {{"score": 90, "rationale": "..."}},
  "source_quality": {{"score": 80, "rationale": "..."}},
  "evidence_strength": {{"score": 75, "rationale": "..."}},
  "recommendation_quality": {{"score": 82, "rationale": "..."}},
  "report_structure": {{"score": 90, "rationale": "..."}},
  "design_quality": {{"score": 85, "rationale": "..."}},
  "decision_making_usefulness": {{"score": 88, "rationale": "..."}},
  "executive_readiness": {{"score": 85, "rationale": "..."}}
}}
"""
    try:
        return client.chat_json([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2)
    except Exception as e:
        print(f"[REVIEW] Score evaluation failed: {e}")
        return {}


def evaluate_dimensions_text(client: 'GroqClient', text: str) -> Dict[str, Any]:
    system = "You are an elite Strategy Consultant and Report Auditor. Return strict JSON only."
    user = f"""
Evaluate the provided report text based on the following 10 dimensions:
1. Research Quality
2. Strategic Insight Quality
3. Executive Readability (Writing Quality)
4. Source Quality
5. Evidence Strength
6. Recommendation Quality
7. Report Structure
8. Design Quality (based on metadata and structure)
9. Decision-Making Usefulness
10. Overall Executive Readiness

Provide a score (0-100) and a brief rationale for each.

Report Text Snippet:
{text[:30000]}

Return JSON format:
{{
  "research_quality": {{"score": 85, "rationale": "..."}},
  "strategic_insight": {{"score": 88, "rationale": "..."}},
  "executive_readability": {{"score": 90, "rationale": "..."}},
  "source_quality": {{"score": 80, "rationale": "..."}},
  "evidence_strength": {{"score": 75, "rationale": "..."}},
  "recommendation_quality": {{"score": 82, "rationale": "..."}},
  "report_structure": {{"score": 90, "rationale": "..."}},
  "design_quality": {{"score": 85, "rationale": "..."}},
  "decision_making_usefulness": {{"score": 88, "rationale": "..."}},
  "executive_readiness": {{"score": 85, "rationale": "..."}}
}}
"""
    try:
        return client.chat_json([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2)
    except Exception as e:
        print(f"[REVIEW] Score evaluation text failed: {e}")
        return {}


def calculate_final_score(dimensions: Dict[str, Any]) -> Dict[str, Any]:
    def get_score(key: str) -> float:
        val = dimensions.get(key, {}).get("score", 0)
        return float(val) if isinstance(val, (int, float, str)) and str(val).replace('.','',1).isdigit() else 70.0

    research_quality = get_score("research_quality")
    strategic_insight = get_score("strategic_insight")
    source_quality = get_score("source_quality")
    writing_quality = get_score("executive_readability")
    design_quality = get_score("design_quality")
    executive_readiness = get_score("executive_readiness")
    
    # Calculate Overall Score
    overall_score = round(
        (research_quality + strategic_insight + source_quality + writing_quality + design_quality + executive_readiness) / 6.0, 1
    )
    
    if overall_score >= 95: grade = "Platinum"
    elif overall_score >= 90: grade = "Gold"
    elif overall_score >= 80: grade = "Silver"
    elif overall_score >= 70: grade = "Bronze"
    else: grade = "Revision Required"
    
    return {
        "overall_score": overall_score,
        "grade": grade,
        "components": {
            "research_quality": research_quality,
            "strategic_insight": strategic_insight,
            "source_quality": source_quality,
            "writing_quality": writing_quality,
            "design_quality": design_quality,
            "executive_readiness": executive_readiness
        }
    }

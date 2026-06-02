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
Evaluate the provided report based on the following 8 dimensions:
1. Research Coverage
2. Evidence Quality
3. Citation Strength
4. Structure
5. Readability
6. Strategic Clarity
7. Recommendation Quality
8. Visual Presentation

Provide a score (0-100) and a brief rationale for each. Evaluate ONLY based on the document's content, not external knowledge.

Report Data:
{json.dumps(report, ensure_ascii=False)}

Sources Data:
{json.dumps(sources, ensure_ascii=False)}

Return JSON format:
{{
  "research_coverage": {{"score": 85, "rationale": "..."}},
  "evidence_quality": {{"score": 88, "rationale": "..."}},
  "citation_strength": {{"score": 90, "rationale": "..."}},
  "structure": {{"score": 80, "rationale": "..."}},
  "readability": {{"score": 75, "rationale": "..."}},
  "strategic_clarity": {{"score": 82, "rationale": "..."}},
  "recommendation_quality": {{"score": 90, "rationale": "..."}},
  "visual_presentation": {{"score": 85, "rationale": "..."}}
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
Evaluate the provided report text based on the following 8 dimensions:
1. Research Coverage
2. Evidence Quality
3. Citation Strength
4. Structure
5. Readability
6. Strategic Clarity
7. Recommendation Quality
8. Visual Presentation

Provide a score (0-100) and a brief rationale for each. Evaluate ONLY based on the document's content, not external knowledge.

Report Text:
{text}

Return JSON format:
{{
  "research_coverage": {{"score": 85, "rationale": "..."}},
  "evidence_quality": {{"score": 88, "rationale": "..."}},
  "citation_strength": {{"score": 90, "rationale": "..."}},
  "structure": {{"score": 80, "rationale": "..."}},
  "readability": {{"score": 75, "rationale": "..."}},
  "strategic_clarity": {{"score": 82, "rationale": "..."}},
  "recommendation_quality": {{"score": 90, "rationale": "..."}},
  "visual_presentation": {{"score": 85, "rationale": "..."}}
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

    research_coverage = get_score("research_coverage")
    evidence_quality = get_score("evidence_quality")
    citation_strength = get_score("citation_strength")
    structure = get_score("structure")
    readability = get_score("readability")
    strategic_clarity = get_score("strategic_clarity")
    recommendation_quality = get_score("recommendation_quality")
    visual_presentation = get_score("visual_presentation")
    
    # Calculate Overall Score
    overall_score = round(
        (research_coverage + evidence_quality + citation_strength + structure + readability + strategic_clarity + recommendation_quality + visual_presentation) / 8.0, 1
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
            "research_coverage": research_coverage,
            "evidence_quality": evidence_quality,
            "citation_strength": citation_strength,
            "structure": structure,
            "readability": readability,
            "strategic_clarity": strategic_clarity,
            "recommendation_quality": recommendation_quality,
            "visual_presentation": visual_presentation
        }
    }

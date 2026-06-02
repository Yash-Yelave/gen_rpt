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

    system = "You are a Due Diligence Auditor. Return strict JSON only."
    user = f"""
Evaluate the provided report section-by-section. Every score generated MUST be auditable.
For every major section, provide detailed evaluations for Research, Evidence, Writing, and Strategic metrics.

For EACH evaluation (research_evaluation, evidence_evaluation, writing_evaluation, strategic_evaluation), you MUST provide:
1. "score" (integer 0-100)
2. "confidence" (High/Medium/Low)
3. "positive_factors" (list of strings)
4. "negative_factors" (list of strings)
5. "score_breakdown" (a dictionary of sub-metrics with integer values)

Also provide the overall "evidence_strength" (Strong/Moderate/Weak/Missing) for the section.

Report Data:
{json.dumps(report, ensure_ascii=False)}

Sources Data:
{json.dumps(sources, ensure_ascii=False)}

Return JSON format exactly like this:
{{
  "section_scores": [
    {{
      "section_name": "Executive Summary",
      "research_evaluation": {{
        "score": 88,
        "confidence": "High",
        "positive_factors": ["Comprehensive coverage"],
        "negative_factors": ["Missing commercialization metrics"],
        "score_breakdown": {{"Coverage": 24, "Depth": 21, "Breadth": 22, "Comparative Analysis": 11, "Scenario Analysis": 10}}
      }},
      "evidence_evaluation": {{
        "score": 80,
        "confidence": "Medium",
        "positive_factors": ["..."],
        "negative_factors": ["..."],
        "score_breakdown": {{}}
      }},
      "writing_evaluation": {{
        "score": 90,
        "confidence": "High",
        "positive_factors": ["..."],
        "negative_factors": ["..."],
        "score_breakdown": {{}}
      }},
      "strategic_evaluation": {{
        "score": 85,
        "confidence": "High",
        "positive_factors": ["..."],
        "negative_factors": ["..."],
        "score_breakdown": {{}}
      }},
      "evidence_strength": "Moderate"
    }}
  ]
}}
"""
    try:
        return client.chat_json([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2)
    except Exception as e:
        print(f"[REVIEW] Score evaluation failed: {e}")
        return {}


def evaluate_dimensions_text(client: 'GroqClient', text: str) -> Dict[str, Any]:
    system = "You are a Due Diligence Auditor. Return strict JSON only."
    user = f"""
Evaluate the provided report text section-by-section. Every score generated MUST be auditable.
For every major section, provide detailed evaluations for Research, Evidence, Writing, and Strategic metrics.

For EACH evaluation (research_evaluation, evidence_evaluation, writing_evaluation, strategic_evaluation), you MUST provide:
1. "score" (integer 0-100)
2. "confidence" (High/Medium/Low)
3. "positive_factors" (list of strings)
4. "negative_factors" (list of strings)
5. "score_breakdown" (a dictionary of sub-metrics with integer values)

Also provide the overall "evidence_strength" (Strong/Moderate/Weak/Missing) for the section.

Report Text:
{text}

Return JSON format exactly like this:
{{
  "section_scores": [
    {{
      "section_name": "Executive Summary",
      "research_evaluation": {{
        "score": 88,
        "confidence": "High",
        "positive_factors": ["Comprehensive coverage"],
        "negative_factors": ["Missing commercialization metrics"],
        "score_breakdown": {{"Coverage": 24, "Depth": 21, "Breadth": 22, "Comparative Analysis": 11, "Scenario Analysis": 10}}
      }},
      "evidence_evaluation": {{
        "score": 80,
        "confidence": "Medium",
        "positive_factors": ["..."],
        "negative_factors": ["..."],
        "score_breakdown": {{}}
      }},
      "writing_evaluation": {{
        "score": 90,
        "confidence": "High",
        "positive_factors": ["..."],
        "negative_factors": ["..."],
        "score_breakdown": {{}}
      }},
      "strategic_evaluation": {{
        "score": 85,
        "confidence": "High",
        "positive_factors": ["..."],
        "negative_factors": ["..."],
        "score_breakdown": {{}}
      }},
      "evidence_strength": "Moderate"
    }}
  ]
}}
"""
    try:
        return client.chat_json([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2)
    except Exception as e:
        print(f"[REVIEW] Score evaluation text failed: {e}")
        return {}


def calculate_final_score(dimensions: Dict[str, Any]) -> Dict[str, Any]:
    section_scores = dimensions.get("section_scores", [])
    if not section_scores:
        overall_score = 70.0
    else:
        total = 0
        count = 0
        for sec in section_scores:
            for key in ["research_evaluation", "evidence_evaluation", "writing_evaluation", "strategic_evaluation"]:
                evaluation = sec.get(key, {})
                val = evaluation.get("score", 70) if isinstance(evaluation, dict) else 70
                total += float(val) if isinstance(val, (int, float, str)) and str(val).replace('.','',1).isdigit() else 70.0
                count += 1
        overall_score = round(total / count, 1) if count > 0 else 70.0

    if overall_score >= 95: grade = "Platinum"
    elif overall_score >= 90: grade = "Gold"
    elif overall_score >= 80: grade = "Silver"
    elif overall_score >= 70: grade = "Bronze"
    else: grade = "Revision Required"
    
    return {
        "overall_score": overall_score,
        "grade": grade,
        "components": section_scores
    }

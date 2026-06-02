import json
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .groq_reviewer import GroqClient

def generate_recommendations(client: 'GroqClient', report_payload_path: Path, dimensions: Dict[str, Any]) -> Dict[str, Any]:
    try:
        with open(report_payload_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
    except:
        report = {}
        
    system = "You are a Senior Editorial Auditor. Return strict JSON only."
    user = f"""
Based on the following AI Review dimension scores and the FULL report, generate an evidence-based strength/weakness analysis and document improvement recommendations.

PRIMARY RULE:
Everything in the review output must be traceable to content found inside the report.
If evidence cannot be found inside the report: DO NOT mention it, assume it, infer it, or generate it.
Recommendations must only improve the report (e.g., "Add quantitative market sizing to the startup section"), NOT industry, investment, or policy actions.

Before returning output: Validate every strength, weakness, and recommendation. Can this be directly linked to report content? If NO: discard it.

Dimension Scores:
{json.dumps(dimensions, ensure_ascii=False)}

Report Content:
{json.dumps(report, ensure_ascii=False)}

Generate JSON format exactly like this:
{{
  "strengths": [
    {{
      "strength": "The report provides a dedicated funding section...",
      "evidence": "Mention of the 14th Five-Year Plan and three investment pillars.",
      "section": "Government Funding Exceeds $15 Billion"
    }}
  ],
  "weaknesses": [
    {{
      "weakness": "The report discusses cryogenic equipment dependence but does not quantify exposure levels...",
      "evidence": "Lack of quantitative exposure data for cryogenic suppliers.",
      "section": "Supply Chain Risks"
    }}
  ],
  "recommendations": [
    {{
      "recommendation": "Add quantitative market sizing to the startup section.",
      "reason": "Improves decision-making usefulness by grounding claims in data.",
      "affected_section": "Startups"
    }}
  ]
}}
"""
    try:
        res = client.chat_json([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2)
        return res
    except Exception as e:
        print(f"[REVIEW] Failed to generate recommendations: {e}")
        return {
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }


def generate_recommendations_text(client: 'GroqClient', text: str, dimensions: Dict[str, Any]) -> Dict[str, Any]:
    system = "You are a Senior Editorial Auditor. Return strict JSON only."
    user = f"""
Based on the following AI Review dimension scores and the FULL report text, generate an evidence-based strength/weakness analysis and document improvement recommendations.

PRIMARY RULE:
Everything in the review output must be traceable to content found inside the report.
If evidence cannot be found inside the report: DO NOT mention it, assume it, infer it, or generate it.
Recommendations must only improve the report (e.g., "Add quantitative market sizing to the startup section"), NOT industry, investment, or policy actions.

Before returning output: Validate every strength, weakness, and recommendation. Can this be directly linked to report content? If NO: discard it.

Dimension Scores:
{json.dumps(dimensions, ensure_ascii=False)}

Report Text:
{text}

Generate JSON format exactly like this:
{{
  "strengths": [
    {{
      "strength": "The report provides a dedicated funding section...",
      "evidence": "Mention of the 14th Five-Year Plan and three investment pillars.",
      "section": "Government Funding Exceeds $15 Billion"
    }}
  ],
  "weaknesses": [
    {{
      "weakness": "The report discusses cryogenic equipment dependence but does not quantify exposure levels...",
      "evidence": "Lack of quantitative exposure data for cryogenic suppliers.",
      "section": "Supply Chain Risks"
    }}
  ],
  "recommendations": [
    {{
      "recommendation": "Add quantitative market sizing to the startup section.",
      "reason": "Improves decision-making usefulness by grounding claims in data.",
      "affected_section": "Startups"
    }}
  ]
}}
"""
    try:
        res = client.chat_json([{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2)
        return res
    except Exception as e:
        print(f"[REVIEW] Failed to generate recommendations from text: {e}")
        return {
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }

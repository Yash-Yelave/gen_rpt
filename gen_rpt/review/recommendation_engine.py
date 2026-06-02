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
        
    system = "You are an Institutional Research Auditor and Due Diligence Expert. Return strict JSON only."
    user = f"""
Based on the AI Review dimension scores and the FULL report, perform a deep institutional audit. Identify factual, evidence, writing, strategic, executive communication, narrative, analytical, and structural weaknesses using ACTUAL REPORT CONTENT ONLY. No generic observations.

Dimension Scores:
{json.dumps(dimensions, ensure_ascii=False)}

Report Content:
{json.dumps(report, ensure_ascii=False)}

Generate JSON format exactly like this:
{{
  "strengths": [
    {{"strength": "...", "evidence": "...", "section": "..."}}
  ],
  "weaknesses": [
    {{"weakness": "...", "evidence": "...", "section": "..."}}
  ],
  "data_gaps": [
    {{"section": "...", "claim": "...", "missing_data": ["market size", "benchmark"], "severity": "High"}}
  ],
  "weak_assumptions": [
    {{"forecast": "...", "missing_evidence": "...", "severity": "High"}}
  ],
  "writing_flaws": [
    {{"type": "vague statements", "example": "...", "section": "...", "severity": "Low"}}
  ],
  "executive_communication": {{
    "minister_ready": false,
    "board_ready": true,
    "swf_ready": false,
    "flagged_sections": [ {{"section": "...", "issue": "too technical"}} ]
  }},
  "narrative_gaps": [
    {{"issue": "Missing link between problem and analysis", "severity": "Medium"}}
  ],
  "strategic_gaps": [
    {{"missing_question": "...", "explanation": "...", "severity": "High"}}
  ],
  "gcc_relevance_gaps": [
    {{"section": "...", "issue": "Does not explain why this matters to GCC stakeholders."}}
  ],
  "recommendation_issues": [
    {{"recommendation": "...", "issue": "Generic recommendation", "severity": "Medium"}}
  ],
  "improvement_tasks": [
    {{
      "section": "...",
      "issue": "...",
      "severity": "Critical",
      "recommended_fix": "...",
      "expected_impact": "..."
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
    system = "You are an Institutional Research Auditor and Due Diligence Expert. Return strict JSON only."
    user = f"""
Based on the AI Review dimension scores and the FULL report text, perform a deep institutional audit. Identify factual, evidence, writing, strategic, executive communication, narrative, analytical, and structural weaknesses using ACTUAL REPORT CONTENT ONLY. No generic observations.

Dimension Scores:
{json.dumps(dimensions, ensure_ascii=False)}

Report Text:
{text}

Generate JSON format exactly like this:
{{
  "strengths": [
    {{"strength": "...", "evidence": "...", "section": "..."}}
  ],
  "weaknesses": [
    {{"weakness": "...", "evidence": "...", "section": "..."}}
  ],
  "data_gaps": [
    {{"section": "...", "claim": "...", "missing_data": ["market size", "benchmark"], "severity": "High"}}
  ],
  "weak_assumptions": [
    {{"forecast": "...", "missing_evidence": "...", "severity": "High"}}
  ],
  "writing_flaws": [
    {{"type": "vague statements", "example": "...", "section": "...", "severity": "Low"}}
  ],
  "executive_communication": {{
    "minister_ready": false,
    "board_ready": true,
    "swf_ready": false,
    "flagged_sections": [ {{"section": "...", "issue": "too technical"}} ]
  }},
  "narrative_gaps": [
    {{"issue": "Missing link between problem and analysis", "severity": "Medium"}}
  ],
  "strategic_gaps": [
    {{"missing_question": "...", "explanation": "...", "severity": "High"}}
  ],
  "gcc_relevance_gaps": [
    {{"section": "...", "issue": "Does not explain why this matters to GCC stakeholders."}}
  ],
  "recommendation_issues": [
    {{"recommendation": "...", "issue": "Generic recommendation", "severity": "Medium"}}
  ],
  "improvement_tasks": [
    {{
      "section": "...",
      "issue": "...",
      "severity": "Critical",
      "recommended_fix": "...",
      "expected_impact": "..."
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

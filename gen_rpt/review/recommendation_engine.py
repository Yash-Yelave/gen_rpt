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
        
    system = "You are a Senior Strategy Consultant. Return strict JSON only."
    user = f"""
Based on the following AI Review dimension scores and the report payload, generate a strength/weakness analysis, improvement recommendations, and an executive readiness assessment.

Dimension Scores:
{json.dumps(dimensions, ensure_ascii=False)}

Report Snippet:
{json.dumps(report, ensure_ascii=False)[:20000]}

Generate JSON format:
{{
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "priority_improvements": [
    {{
      "issue": "...",
      "impact": "...",
      "suggested_fix": "...",
      "priority_level": "High"
    }}
  ],
  "executive_readiness": {{
    "board_members": true,
    "ministers": false,
    "ceos": true,
    "sovereign_wealth_funds": false,
    "senior_executives": true,
    "justification": "Explanation of why it fits these audiences..."
  }}
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
            "priority_improvements": [],
            "executive_readiness": {}
        }

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .groq_reviewer import GroqClient


def extract_claims(client: 'GroqClient', report_payload_path: Path, output_path: Path) -> list:
    print("[REVIEW] Extracting claims")
    
    try:
        with open(report_payload_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
    except Exception as e:
        print(f"[REVIEW] Failed to load report payload: {e}")
        return []
        
    system = "You are an expert financial and strategic analyst. Return strict JSON only."
    user = f"""
Extract the major factual claims, statistics, and strategic assertions from the provided report data.
Focus on: Executive Summary, Key Findings, Strategic Recommendations, Charts, and Insights.

Report Data:
{json.dumps(report, ensure_ascii=False)[:30000]}

Return a JSON list of objects, each with 'claim_id' (integer) and 'claim' (string).
Example:
{{
  "claims": [
    {{
      "claim_id": 1,
      "claim": "China's EV exports are expected to grow 25% annually."
    }}
  ]
}}
"""
    try:
        res = client.chat_json([
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ], temperature=0.2)
        claims = res.get('claims', [])
    except Exception as e:
        print(f"[REVIEW] Failed to extract claims: {e}")
        claims = []
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(claims, f, ensure_ascii=False, indent=2)
        
    return claims

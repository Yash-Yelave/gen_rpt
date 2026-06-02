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
Extract the findings, claims, recommendations, strategic insights, forecasts, and statistics from the provided report data. Create an evidence map.
Every entry must refer to specific content in the report.

Report Data:
{json.dumps(report, ensure_ascii=False)}

Return a JSON list of objects under the key 'claims', each with 'claim' (string), 'section' (string), and 'location' (string).
Example:
{{
  "claims": [
    {{
      "claim": "Government funding exceeds $15 billion",
      "section": "Government Funding Exceeds $15 Billion",
      "location": "page 6"
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


def extract_claims_text(client: 'GroqClient', text: str, output_path: Path) -> list:
    print("[REVIEW] Extracting claims from text")
    
    system = "You are an expert financial and strategic analyst. Return strict JSON only."
    user = f"""
Extract the findings, claims, recommendations, strategic insights, forecasts, and statistics from the provided report text. Create an evidence map.
Every entry must refer to specific content in the report.

Report Text:
{text}

Return a JSON list of objects under the key 'claims', each with 'claim' (string), 'section' (string), and 'location' (string).
Example:
{{
  "claims": [
    {{
      "claim": "Government funding exceeds $15 billion",
      "section": "Government Funding Exceeds $15 Billion",
      "location": "page 6"
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
        print(f"[REVIEW] Failed to extract claims from text: {e}")
        claims = []
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(claims, f, ensure_ascii=False, indent=2)
        
    return claims

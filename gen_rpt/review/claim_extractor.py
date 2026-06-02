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
        
    system = "You are a Due Diligence Auditor. Return strict JSON only."
    user = f"""
Extract all major claims, findings, forecasts, and statistics from the provided report data.
For every major claim, evaluate:
- Is evidence provided? (true/false)
- Is data provided? (true/false)
- Is a source referenced? (true/false)
- Is the claim quantified? (true/false)
- Is confidence justified? (true/false)

Classify each claim as exactly one of: "Supported", "Weak", "Unsupported", "High-Risk".
Calculate the 'quantification_ratio' as the percentage (0-100) of statements that are quantified vs non-quantified.

Report Data:
{json.dumps(report, ensure_ascii=False)}

Return JSON format exactly like this:
{{
  "claims": [
    {{
      "claim": "Government funding exceeds $15 billion",
      "section": "Government Funding",
      "evidence_provided": true,
      "data_provided": true,
      "source_referenced": true,
      "quantified": true,
      "confidence_justified": true,
      "classification": "Supported"
    }}
  ],
  "quantification_ratio": 45
}}
"""
    try:
        res = client.chat_json([
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ], temperature=0.2)
    except Exception as e:
        print(f"[REVIEW] Failed to extract claims: {e}")
        res = {"claims": [], "quantification_ratio": 0}
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
        
    return res


def extract_claims_text(client: 'GroqClient', text: str, output_path: Path) -> list:
    print("[REVIEW] Extracting claims from text")
    
    system = "You are a Due Diligence Auditor. Return strict JSON only."
    user = f"""
Extract all major claims, findings, forecasts, and statistics from the provided report text.
For every major claim, evaluate:
- Is evidence provided? (true/false)
- Is data provided? (true/false)
- Is a source referenced? (true/false)
- Is the claim quantified? (true/false)
- Is confidence justified? (true/false)

Classify each claim as exactly one of: "Supported", "Weak", "Unsupported", "High-Risk".
Calculate the 'quantification_ratio' as the percentage (0-100) of statements that are quantified vs non-quantified.

Report Text:
{text}

Return JSON format exactly like this:
{{
  "claims": [
    {{
      "claim": "Government funding exceeds $15 billion",
      "section": "Government Funding",
      "evidence_provided": true,
      "data_provided": true,
      "source_referenced": true,
      "quantified": true,
      "confidence_justified": true,
      "classification": "Supported"
    }}
  ],
  "quantification_ratio": 45
}}
"""
    try:
        res = client.chat_json([
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ], temperature=0.2)
    except Exception as e:
        print(f"[REVIEW] Failed to extract claims from text: {e}")
        res = {"claims": [], "quantification_ratio": 0}
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
        
    return res

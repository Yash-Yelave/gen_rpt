"""
claim_extractor.py

Step 1 of the multi-step audit pipeline.

Extracts every major claim from the structured parsed report, maps each
claim to its exact section and paragraph, and classifies it as:
  supported / partially_supported / unsupported / high_risk / speculative

Returns a ClaimsAudit dict.
"""
import json
from pathlib import Path
from typing import TYPE_CHECKING, List, Dict, Any

from .text_preprocessor import ParsedReport, truncate_for_prompt

if TYPE_CHECKING:
    from .groq_reviewer import GroqClient


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

_SYSTEM = (
    "You are a senior institutional research auditor. "
    "Your task is to extract and classify every substantive claim in the "
    "report text provided. You must NOT use outside knowledge — evaluate ONLY "
    "what is written in the report. Return strict JSON only."
)

_USER_TEMPLATE = """\
Below is the full text of a research report, split into sections and numbered paragraphs.

REPORT TEXT:
{report_text}

TASK:
For EVERY major claim, finding, forecast, statistic, or recommendation you find in this report text:

1. Quote or closely paraphrase the claim.
2. Record the exact section title and paragraph number it appears in.
3. Construct a location reference in this exact format:
   "Location → [<section_title>] | Para <N> | \\"<first 6 words>\\" → \\"<last 6 words>\\""
4. Evaluate the claim against 5 criteria (true/false each):
   - evidence_provided: Is there qualitative evidence in the report supporting this?
   - data_provided: Is there a number, statistic, or dataset supporting this?
   - source_referenced: Is an institution, study, or publication named?
   - quantified: Does the claim include specific quantities rather than vague terms?
   - confidence_justified: Is the degree of certainty appropriate for the evidence shown?
5. Classify the claim as EXACTLY ONE of:
   - "supported" — passes 4-5 criteria
   - "partially_supported" — passes 2-3 criteria
   - "unsupported" — passes 0-1 criteria with no source
   - "high_risk" — contains a specific number/forecast/timeline with no source or data
   - "speculative" — uses hedging language ("may", "could", "might") with no data

Return JSON in this EXACT structure:
{{
  "claims": [
    {{
      "claim": "<claim text>",
      "section": "<section title>",
      "paragraph": <paragraph number as integer>,
      "location_ref": "Location → [<section title>] | Para <N> | \\"<opening words>\\" → \\"<closing words>\\"",
      "evidence_provided": <true|false>,
      "data_provided": <true|false>,
      "source_referenced": <true|false>,
      "quantified": <true|false>,
      "confidence_justified": <true|false>,
      "classification": "<supported|partially_supported|unsupported|high_risk|speculative>"
    }}
  ],
  "quantification_ratio": <integer 0-100, percent of claims that are quantified>
}}

IMPORTANT RULES:
- Extract EVERY significant claim (target 8-20 claims for a normal report).
- Every claim MUST have a location_ref.
- Do NOT invent claims not in the report text.
- Do NOT use outside knowledge to assess credibility.
- Prefer "high_risk" for numerical forecasts, timelines, or market sizes with no cited source.
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_claims(
    client: "GroqClient",
    parsed_report: ParsedReport,
    output_path: Path,
) -> Dict[str, Any]:
    """
    Extract and classify all claims from a ParsedReport.

    Writes claims.json to output_path and returns the claims audit dict.
    """
    print("[REVIEW] Extracting and classifying claims with location references")

    report_text = truncate_for_prompt(parsed_report, max_chars=24_000)
    prompt = _USER_TEMPLATE.format(report_text=report_text)

    try:
        result = client.chat_json(
            [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
    except Exception as e:
        print(f"[REVIEW] Claim extraction failed: {e}")
        result = {"claims": [], "quantification_ratio": 0}

    # Augment with summary counts
    claims: List[Dict] = result.get("claims", [])
    audit = {
        "claims": claims,
        "quantification_ratio": result.get("quantification_ratio", 0),
        "total_claims": len(claims),
        "supported_count": _count(claims, "supported"),
        "partially_supported_count": _count(claims, "partially_supported"),
        "unsupported_count": _count(claims, "unsupported"),
        "high_risk_count": _count(claims, "high_risk"),
        "speculative_count": _count(claims, "speculative"),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)

    _print_summary(audit)
    return audit


def _count(claims: List[Dict], classification: str) -> int:
    return sum(1 for c in claims if c.get("classification") == classification)


def _print_summary(audit: Dict[str, Any]) -> None:
    total = audit["total_claims"]
    print(
        f"[REVIEW] Claims extracted: {total} total | "
        f"supported={audit['supported_count']} | "
        f"partial={audit['partially_supported_count']} | "
        f"unsupported={audit['unsupported_count']} | "
        f"high_risk={audit['high_risk_count']} | "
        f"speculative={audit['speculative_count']}"
    )

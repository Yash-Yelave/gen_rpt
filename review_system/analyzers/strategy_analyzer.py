"""
review_system/analyzers/strategy_analyzer.py

Identifies strategic gaps: missing so-what, generic recommendations,
missing decision implications, absence of risk/opportunity distinction.
"""
from typing import Dict, Any, TYPE_CHECKING

from shared.report_schema import ParsedReport
from review_system.utils.logging_utils import get_run_logger

if TYPE_CHECKING:
    from review_system.reviewers.groq_review_engine import GroqReviewEngine

log = get_run_logger()

_SYSTEM = (
    "You are a senior strategy reviewer evaluating a research report. "
    "Identify specific strategic deficiencies grounded in the actual report text. "
    "Never produce generic comments. Return strict JSON only."
)

_USER = """\
REPORT TEXT (by section and paragraph):
{report_text}

TASK: Identify specific strategic gaps.
Every finding must include an exact location reference.
Format: "Location -> [<section>] | Para <N> | \\"<open>\\" -> \\"<close>\\""

CHECK FOR:
1. Missing "so-what": Section presents findings but draws no decision implication
2. Generic recommendations: Advice that could apply to any report ("invest more", "do more research")
3. Missing risk/opportunity split: Risks and opportunities conflated or one is absent
4. Missing stakeholder implications: No tailoring to investor, government, or operator perspectives
5. Absent call-to-action: No explicit next step or decision point

Return JSON:
{{
  "strategic_gaps": [
    {{
      "gap_type": "missing_so_what|generic_recommendation|no_risk_opportunity_split|missing_stakeholder|absent_call_to_action",
      "finding": "<specific description referencing report text>",
      "location_ref": "Location -> ...",
      "severity": "Critical|High|Medium|Low"
    }}
  ],
  "has_explicit_recommendations": <true|false>,
  "has_risk_opportunity_split": <true|false>
}}
"""


def run(
    engine: "GroqReviewEngine",
    parsed: ParsedReport,
    claims_audit: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Run strategy analysis. Returns strategic gaps dict."""
    log.info("Running strategy analyzer")

    report_text = parsed.as_prompt_text(max_chars=16_000)
    prompt = _USER.format(report_text=report_text)

    try:
        result = engine.chat_json(
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.2,
        )
    except Exception as e:
        log.error("Strategy analyzer failed: %s", e)
        result = {}

    return {
        "strategic_gaps":                 result.get("strategic_gaps", []),
        "has_explicit_recommendations":   result.get("has_explicit_recommendations", False),
        "has_risk_opportunity_split":     result.get("has_risk_opportunity_split", False),
    }

"""
review_system/analyzers/writing_analyzer.py

Detects writing flaws: vague language, undefined jargon, repeated phrases,
weak transitions, filler text, overloaded sentences.
"""
from typing import Dict, Any, TYPE_CHECKING

from shared.report_schema import ParsedReport
from review_system.utils.logging_utils import get_run_logger

if TYPE_CHECKING:
    from review_system.reviewers.groq_review_engine import GroqReviewEngine

log = get_run_logger()

_SYSTEM = (
    "You are a senior institutional editor reviewing writing quality. "
    "Identify SPECIFIC writing flaws with exact quotes. "
    "Do not make general comments. Return strict JSON only."
)

_USER = """\
REPORT TEXT (by section and paragraph):
{report_text}

TASK: Identify specific writing flaws in the following categories.
For each flaw, quote the problematic text exactly and provide a location reference.
Format: "Location -> [<section>] | Para <N> | \\"<open>\\" -> \\"<close>\\""

CATEGORIES:
- vague_statement    : Unclear, hedge-y, or uncommitted language
- undefined_jargon   : Technical term used without definition
- repeated_phrase    : Same phrase or sentence structure used 2+ times
- weak_transition    : Abrupt or missing connection between paragraphs/sections
- filler_text        : Words/sentences that add no information
- overloaded_sentence: Single sentence containing multiple unrelated claims

Return JSON:
{{
  "writing_flaws": [
    {{
      "flaw_type": "<category>",
      "example": "<exact or near-exact quote>",
      "location_ref": "Location -> ...",
      "severity": "High|Medium|Low",
      "suggestion": "<one-line fix>"
    }}
  ]
}}
"""


def run(
    engine: "GroqReviewEngine",
    parsed: ParsedReport,
    claims_audit: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Run writing analysis. Returns dict with writing_flaws list."""
    log.info("Running writing analyzer")

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
        log.error("Writing analyzer failed: %s", e)
        result = {}

    return {"writing_flaws": result.get("writing_flaws", [])}

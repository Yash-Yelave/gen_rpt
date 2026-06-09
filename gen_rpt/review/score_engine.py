"""
score_engine.py

Step 2 of the multi-step audit pipeline.

Scores the report across FOUR dimensions using the report text and
the claims audit produced in step 1. Each dimension has a different
maximum point value that sums to 100.

Dimensions:
  1. Research Quality        — max 30 pts
  2. Evidence & Citations    — max 25 pts
  3. Strategic Clarity       — max 25 pts
  4. Writing & Structure     — max 20 pts

Returns a ReviewScores dict.
"""
import json
from typing import Dict, Any, TYPE_CHECKING

from .text_preprocessor import ParsedReport, truncate_for_prompt

if TYPE_CHECKING:
    from .groq_reviewer import GroqClient

# ---------------------------------------------------------------------------
# Grade thresholds
# ---------------------------------------------------------------------------

GRADE_MAP = [
    (90, "Gold"),
    (75, "Silver"),
    (60, "Bronze"),
    (0,  "Red"),
]


def _grade(score: float) -> str:
    for threshold, label in GRADE_MAP:
        if score >= threshold:
            return label
    return "Red"


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_SYSTEM = (
    "You are a senior institutional research auditor scoring a report. "
    "Base every score ONLY on what appears in the provided report text. "
    "Do NOT use outside knowledge. Do NOT assign the same scores to different "
    "sections unless the evidence truly supports identical quality. "
    "Return strict JSON only."
)

_USER_TEMPLATE = """\
You are scoring the following report across four independent dimensions.

REPORT TEXT (structured by section and paragraph):
{report_text}

CLAIMS AUDIT SUMMARY:
- Total claims extracted: {total_claims}
- Supported: {supported}  |  Partially supported: {partial}
- Unsupported: {unsupported}  |  High-risk: {high_risk}  |  Speculative: {speculative}
- Quantification ratio: {quant_ratio}%

SCORING DIMENSIONS AND MAX POINTS:
1. Research Quality (max 30 points)
   - Sub-criteria: Breadth of topic coverage, depth of analysis per section,
     use of multiple viewpoints, scenario/uncertainty analysis, strength of
     conclusions drawn from evidence.
   
2. Evidence & Citations (max 25 points)
   - Sub-criteria: Proportion of claims backed by named sources, presence of
     a bibliography or reference section, traceability of key statistics,
     source diversity (academic/institutional/industry), absence of bare assertions.

3. Strategic Clarity (max 25 points)
   - Sub-criteria: Clear "so-what" for each major section, explicit decision
     implications, distinction between risks and opportunities, quality of
     recommendations (specific vs generic), actionability for target audience.

4. Writing & Structure (max 20 points)
   - Sub-criteria: Section titles match content, logical flow and transitions,
     absence of jargon without definition, clarity and conciseness, avoidance
     of repeated or filler language.

SCORING RULES:
- Each dimension score must be an INTEGER between 0 and its maximum.
- Every positive_factor and negative_factor MUST cite specific content from
  the report (section name, claim, or quote). Generic phrases are forbidden.
- Scores must reflect the actual claims audit numbers above.
- A report with many unsupported/high-risk claims CANNOT score above 18/25
  on Evidence & Citations.
- A report with no bibliography or traceable sources scores at most 14/25
  on Evidence & Citations.

Return JSON in this EXACT structure:
{{
  "research_quality": {{
    "score": <0-30>,
    "max_points": 30,
    "justification": "<2-4 sentences citing specific report content>",
    "positive_factors": ["<specific strength from the report>", ...],
    "negative_factors": ["<specific deficiency from the report>", ...]
  }},
  "evidence_and_citations": {{
    "score": <0-25>,
    "max_points": 25,
    "justification": "<2-4 sentences citing specific report content>",
    "positive_factors": ["<specific strength>", ...],
    "negative_factors": ["<specific deficiency>", ...]
  }},
  "strategic_clarity": {{
    "score": <0-25>,
    "max_points": 25,
    "justification": "<2-4 sentences citing specific report content>",
    "positive_factors": ["<specific strength>", ...],
    "negative_factors": ["<specific deficiency>", ...]
  }},
  "writing_and_structure": {{
    "score": <0-20>,
    "max_points": 20,
    "justification": "<2-4 sentences citing specific report content>",
    "positive_factors": ["<specific strength>", ...],
    "negative_factors": ["<specific deficiency>", ...]
  }}
}}
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def score_report(
    client: "GroqClient",
    parsed_report: ParsedReport,
    claims_audit: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Score the parsed report across all four dimensions.

    Returns a ReviewScores-shaped dict including overall_score and grade.
    """
    print("[REVIEW] Scoring report across 4 dimensions (Research/Evidence/Strategic/Writing)")

    report_text = truncate_for_prompt(parsed_report, max_chars=20_000)

    prompt = _USER_TEMPLATE.format(
        report_text=report_text,
        total_claims=claims_audit.get("total_claims", 0),
        supported=claims_audit.get("supported_count", 0),
        partial=claims_audit.get("partially_supported_count", 0),
        unsupported=claims_audit.get("unsupported_count", 0),
        high_risk=claims_audit.get("high_risk_count", 0),
        speculative=claims_audit.get("speculative_count", 0),
        quant_ratio=claims_audit.get("quantification_ratio", 0),
    )

    try:
        raw = client.chat_json(
            [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
    except Exception as e:
        print(f"[REVIEW] Scoring failed: {e}")
        raw = _fallback_scores()

    return _build_review_scores(raw)


def _build_review_scores(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Assemble final ReviewScores from raw LLM output."""
    rq  = raw.get("research_quality",       {})
    ec  = raw.get("evidence_and_citations", {})
    sc  = raw.get("strategic_clarity",      {})
    ws  = raw.get("writing_and_structure",  {})

    # Clamp scores to their maximums
    rq_score = min(int(rq.get("score", 15)), 30)
    ec_score = min(int(ec.get("score", 12)), 25)
    sc_score = min(int(sc.get("score", 12)), 25)
    ws_score = min(int(ws.get("score", 10)), 20)

    overall = round(rq_score + ec_score + sc_score + ws_score, 1)

    def _norm(d: Dict, score: int, max_pts: int) -> Dict[str, Any]:
        return {
            "score": score,
            "max_points": max_pts,
            "justification": d.get("justification", "Not evaluated."),
            "positive_factors": d.get("positive_factors") or ["None identified."],
            "negative_factors": d.get("negative_factors") or ["None identified."],
        }

    scores: Dict[str, Any] = {
        "overall_score": overall,
        "grade": _grade(overall),
        "research_quality":       _norm(rq, rq_score, 30),
        "evidence_and_citations": _norm(ec, ec_score, 25),
        "strategic_clarity":      _norm(sc, sc_score, 25),
        "writing_and_structure":  _norm(ws, ws_score, 20),
    }

    print(
        f"[REVIEW] Scores: Research={rq_score}/30 | Evidence={ec_score}/25 | "
        f"Strategic={sc_score}/25 | Writing={ws_score}/20 | "
        f"Total={overall}/100 → {scores['grade']}"
    )
    return scores


def _fallback_scores() -> Dict[str, Any]:
    """Return a safe fallback if the LLM call fails."""
    return {
        "research_quality":       {"score": 15, "max_points": 30, "justification": "Scoring unavailable.", "positive_factors": [], "negative_factors": []},
        "evidence_and_citations": {"score": 10, "max_points": 25, "justification": "Scoring unavailable.", "positive_factors": [], "negative_factors": []},
        "strategic_clarity":      {"score": 10, "max_points": 25, "justification": "Scoring unavailable.", "positive_factors": [], "negative_factors": []},
        "writing_and_structure":  {"score": 8,  "max_points": 20, "justification": "Scoring unavailable.", "positive_factors": [], "negative_factors": []},
    }

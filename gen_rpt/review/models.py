"""
models.py

Typed data contracts for the upgraded evidence-based review engine.
All modules import from here — never define ad-hoc dicts inline.
"""
from typing import TypedDict, List, Optional


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

class DimensionScore(TypedDict):
    """One of the four top-level scoring dimensions."""
    score: int                      # 0-30 or 0-25 or 0-20 (per dimension max)
    max_points: int
    justification: str              # Written explanation grounded in report text
    positive_factors: List[str]     # Specific strengths found IN the report
    negative_factors: List[str]     # Specific deficiencies found IN the report


class ReviewScores(TypedDict):
    overall_score: float            # 0-100
    grade: str                      # Gold / Silver / Bronze / Red
    research_quality: DimensionScore       # max 30
    evidence_and_citations: DimensionScore # max 25
    strategic_clarity: DimensionScore      # max 25
    writing_and_structure: DimensionScore  # max 20


# ---------------------------------------------------------------------------
# Claim audit
# ---------------------------------------------------------------------------

class AuditedClaim(TypedDict):
    claim: str
    section: str
    paragraph: int
    location_ref: str               # "Location → [Section] | Para N | "open" → "close""
    evidence_provided: bool
    data_provided: bool
    source_referenced: bool
    quantified: bool
    confidence_justified: bool
    classification: str             # supported / partially_supported / unsupported / high_risk / speculative


class ClaimsAudit(TypedDict):
    claims: List[AuditedClaim]
    quantification_ratio: int       # 0-100
    total_claims: int
    supported_count: int
    partially_supported_count: int
    unsupported_count: int
    high_risk_count: int
    speculative_count: int


# ---------------------------------------------------------------------------
# Issue detection
# ---------------------------------------------------------------------------

class LocatedFinding(TypedDict):
    """A specific finding with a mandatory location reference."""
    finding: str                    # The actual finding, grounded in report text
    location_ref: str               # Precise location string
    severity: str                   # Critical / High / Medium / Low


class DataGap(TypedDict):
    section: str
    claim: str
    location_ref: str
    missing_data: List[str]
    severity: str


class WeakAssumption(TypedDict):
    forecast_or_claim: str
    location_ref: str
    missing_evidence: str
    severity: str


class WritingFlaw(TypedDict):
    flaw_type: str                  # e.g. "vague statement", "undefined jargon"
    example: str                    # Exact quote from the report
    location_ref: str
    severity: str


class ImprovementTask(TypedDict):
    priority: str                   # Critical / High / Medium / Low
    section: str
    issue: str
    fix: str
    expected_impact: str


class ExecutiveCommunication(TypedDict):
    minister_ready: bool
    board_ready: bool
    swf_ready: bool
    minister_reason: str
    board_reason: str
    swf_reason: str
    flagged_sections: List[dict]    # {"section": str, "issue": str}


# ---------------------------------------------------------------------------
# Recommendations package
# ---------------------------------------------------------------------------

class Recommendations(TypedDict):
    strengths: List[LocatedFinding]
    weaknesses: List[LocatedFinding]
    data_gaps: List[DataGap]
    weak_assumptions: List[WeakAssumption]
    writing_flaws: List[WritingFlaw]
    narrative_gaps: List[LocatedFinding]
    strategic_gaps: List[LocatedFinding]
    audience_relevance_gaps: List[LocatedFinding]
    executive_communication: ExecutiveCommunication
    improvement_tasks: List[ImprovementTask]


# ---------------------------------------------------------------------------
# Full review data
# ---------------------------------------------------------------------------

class ReviewData(TypedDict):
    timestamp: str
    report_title: str
    scores: ReviewScores
    claims_audit: ClaimsAudit
    recommendations: Recommendations

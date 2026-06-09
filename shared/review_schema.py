"""
shared/review_schema.py

Pure schema for the complete review result.
No business logic.
"""
from typing import TypedDict, List, Dict, Any

from .score_schema import ReviewScores
from .findings_schema import (
    ClaimsAudit, LocatedFinding, DataGap, WeakAssumption,
    WritingFlaw, ImprovementTask, ExecutiveCommunication,
)


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


class ReviewData(TypedDict):
    timestamp: str
    report_title: str
    report_path: str
    scores: ReviewScores
    claims_audit: ClaimsAudit
    recommendations: Recommendations

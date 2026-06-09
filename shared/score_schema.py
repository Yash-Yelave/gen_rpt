"""
shared/score_schema.py

Pure schema for review scoring dimensions.
No business logic.
"""
from typing import TypedDict, List


class DimensionScore(TypedDict):
    score: int           # actual points earned
    max_points: int      # dimension maximum
    justification: str
    positive_factors: List[str]
    negative_factors: List[str]


class ReviewScores(TypedDict):
    overall_score: float
    grade: str                      # Gold / Silver / Bronze / Red
    research_quality: DimensionScore       # max 30
    evidence_and_citations: DimensionScore # max 25
    strategic_clarity: DimensionScore      # max 25
    writing_and_structure: DimensionScore  # max 20

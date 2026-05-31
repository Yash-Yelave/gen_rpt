from typing import TypedDict, List, Dict, Any

class ScoreComponents(TypedDict):
    research_quality: float
    strategic_insight: float
    source_quality: float
    writing_quality: float
    design_quality: float
    executive_readiness: float

class ReviewScores(TypedDict):
    overall_score: float
    grade: str
    components: ScoreComponents

class RecommendationItem(TypedDict):
    issue: str
    impact: str
    suggested_fix: str
    priority_level: str

class ExecutiveReadiness(TypedDict):
    board_members: bool
    ministers: bool
    ceos: bool
    sovereign_wealth_funds: bool
    senior_executives: bool
    justification: str

class Recommendations(TypedDict):
    strengths: List[str]
    weaknesses: List[str]
    priority_improvements: List[RecommendationItem]
    executive_readiness: ExecutiveReadiness

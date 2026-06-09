"""
shared/findings_schema.py

Pure schema for review findings, claims, and improvement tasks.
No business logic.
"""
from typing import TypedDict, List


class AuditedClaim(TypedDict):
    claim: str
    section: str
    paragraph: int
    location_ref: str
    evidence_provided: bool
    data_provided: bool
    source_referenced: bool
    quantified: bool
    confidence_justified: bool
    classification: str   # supported|partially_supported|unsupported|high_risk|speculative


class ClaimsAudit(TypedDict):
    claims: List[AuditedClaim]
    quantification_ratio: int
    total_claims: int
    supported_count: int
    partially_supported_count: int
    unsupported_count: int
    high_risk_count: int
    speculative_count: int


class LocatedFinding(TypedDict):
    finding: str
    location_ref: str
    severity: str   # Critical / High / Medium / Low


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
    flaw_type: str
    example: str
    location_ref: str
    severity: str


class ImprovementTask(TypedDict):
    priority: str   # Critical / High / Medium / Low
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
    flagged_sections: List[dict]

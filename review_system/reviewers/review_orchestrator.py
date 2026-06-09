"""
review_system/reviewers/review_orchestrator.py

Runs the multi-step analysis pipeline and returns all raw step outputs.
Does NOT assemble the final ReviewData — that is review_builder's job.

Pipeline order:
  1. Claim extraction
  2. Full scoring call (one LLM pass, all 4 dimensions)
  3. Six analyzers (evidence, citation, writing, strategy, structure, audience)
  4. Per-dimension scorer validation + caps
  5. Returns collected results dict
"""
from pathlib import Path
from typing import Dict, Any

from shared.report_schema import ParsedReport
from review_system.reviewers.groq_review_engine import GroqReviewEngine
from review_system.extractors.claim_extractor import extract_claims
from review_system.analyzers import (
    run_evidence, run_citation, run_writing,
    run_strategy, run_structure, run_audience,
)
from review_system.scoring import (
    score_research, score_evidence, score_strategic, score_writing,
)
from review_system.config.prompts import SCORING_SYSTEM, SCORING_USER
from review_system.config.review_config import SCORING_MAX_CHARS, GRADE_THRESHOLDS
from review_system.utils.logging_utils import get_run_logger

log = get_run_logger()


def _grade(total: float) -> str:
    for threshold, label in GRADE_THRESHOLDS:
        if total >= threshold:
            return label
    return "Red"


def _fetch_raw_scores(
    engine: GroqReviewEngine,
    parsed: ParsedReport,
    claims_audit: Dict[str, Any],
) -> Dict[str, Any]:
    """One LLM call to get all 4 dimension scores."""
    report_text = parsed.as_prompt_text(max_chars=SCORING_MAX_CHARS)
    prompt = SCORING_USER.format(
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
        return engine.chat_json(
            messages=[
                {"role": "system", "content": SCORING_SYSTEM},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.1,
        )
    except Exception as e:
        log.error("Raw scoring call failed: %s", e)
        return {}


def run_pipeline(
    engine: GroqReviewEngine,
    parsed: ParsedReport,
    output_dir: Path,
) -> Dict[str, Any]:
    """
    Execute the full review pipeline.
    Returns a dict with keys:
      claims_audit, raw_scores, evidence, citation, writing,
      strategy, structure, audience, scores
    """
    log.info("Pipeline starting for: %r", parsed.title)

    # ── Step 1: Claims ──────────────────────────────────────────────────────
    log.info("Step 1/5: Extracting claims")
    claims_audit = extract_claims(engine, parsed, output_dir)

    # ── Step 2: Raw scoring (one LLM pass) ──────────────────────────────────
    log.info("Step 2/5: Scoring across 4 dimensions")
    raw_scores = _fetch_raw_scores(engine, parsed, claims_audit)

    # ── Step 3: Six analyzers ───────────────────────────────────────────────
    log.info("Step 3/5: Running 6 analyzers")
    evidence_r  = run_evidence(engine, parsed, claims_audit)
    citation_r  = run_citation(engine, parsed, claims_audit)
    writing_r   = run_writing(engine, parsed, claims_audit)
    strategy_r  = run_strategy(engine, parsed, claims_audit)
    structure_r = run_structure(engine, parsed, claims_audit)
    audience_r  = run_audience(engine, parsed, claims_audit)

    # ── Step 4: Per-dimension scoring with caps ──────────────────────────────
    log.info("Step 4/5: Applying scoring caps and dimension finalisation")
    rq_dim = score_research(engine, parsed, claims_audit, raw_scores)
    ec_dim = score_evidence(engine, parsed, claims_audit, raw_scores, citation_r)
    sc_dim = score_strategic(engine, parsed, claims_audit, raw_scores, strategy_r)
    ws_dim = score_writing(engine, parsed, claims_audit, raw_scores, writing_r)

    total = round(
        rq_dim["score"] + ec_dim["score"] + sc_dim["score"] + ws_dim["score"], 1
    )
    grade = _grade(total)

    scores: Dict[str, Any] = {
        "overall_score":         total,
        "grade":                 grade,
        "research_quality":      rq_dim,
        "evidence_and_citations": ec_dim,
        "strategic_clarity":     sc_dim,
        "writing_and_structure": ws_dim,
    }

    log.info(
        "Scores: Research=%d/30 | Evidence=%d/25 | Strategic=%d/25 | Writing=%d/20 "
        "| Total=%.1f/100 | Grade=%s",
        rq_dim["score"], ec_dim["score"], sc_dim["score"], ws_dim["score"],
        total, grade,
    )

    return {
        "claims_audit": claims_audit,
        "raw_scores":   raw_scores,
        "evidence":     evidence_r,
        "citation":     citation_r,
        "writing":      writing_r,
        "strategy":     strategy_r,
        "structure":    structure_r,
        "audience":     audience_r,
        "scores":       scores,
    }

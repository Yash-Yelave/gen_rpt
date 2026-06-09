"""
review_system/outputs/json_writer.py

Writes all JSON output files for a completed review.

Files written:
  review.json       — complete ReviewData
  claims.json       — claims audit (also written by claim_extractor; this refreshes it)
  findings.json     — all categorised findings
  scores.json       — scores only
  audit_manifest.json — lightweight run summary
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from review_system.config.review_config import OUTPUT_FILES
from review_system.utils.file_utils import write_json_safe, safe_mkdir
from review_system.utils.logging_utils import get_generation_logger

log = get_generation_logger()


def write_all_json(output_dir: Path, review_data: Dict[str, Any]) -> None:
    """Write all JSON review artifacts to output_dir."""
    safe_mkdir(output_dir)

    scores  = review_data.get("scores", {})
    claims  = review_data.get("claims_audit", {})
    recs    = review_data.get("recommendations", {})

    # 1. Full review data
    _w(output_dir / OUTPUT_FILES["review_json"], review_data, "review.json")

    # 2. Claims audit
    _w(output_dir / OUTPUT_FILES["claims_json"], claims, "claims.json")

    # 3. Categorised findings
    findings = {
        "strengths":              recs.get("strengths", []),
        "weaknesses":             recs.get("weaknesses", []),
        "data_gaps":              recs.get("data_gaps", []),
        "weak_assumptions":       recs.get("weak_assumptions", []),
        "writing_flaws":          recs.get("writing_flaws", []),
        "narrative_gaps":         recs.get("narrative_gaps", []),
        "strategic_gaps":         recs.get("strategic_gaps", []),
        "audience_relevance_gaps": recs.get("audience_relevance_gaps", []),
        "improvement_tasks":      recs.get("improvement_tasks", []),
    }
    _w(output_dir / OUTPUT_FILES["findings_json"], findings, "findings.json")

    # 4. Scores only
    _w(output_dir / OUTPUT_FILES["scores_json"], scores, "scores.json")

    # 5. Audit manifest (lightweight summary for CI / downstream tools)
    manifest = {
        "review_timestamp":   review_data.get("timestamp"),
        "report_title":       review_data.get("report_title"),
        "report_path":        review_data.get("report_path"),
        "overall_score":      scores.get("overall_score"),
        "grade":              scores.get("grade"),
        "total_claims":       claims.get("total_claims", 0),
        "high_risk_claims":   claims.get("high_risk_count", 0),
        "unsupported_claims": claims.get("unsupported_count", 0),
        "improvement_tasks":  len(recs.get("improvement_tasks", [])),
        "minister_ready":     recs.get("executive_communication", {}).get("minister_ready"),
        "board_ready":        recs.get("executive_communication", {}).get("board_ready"),
        "swf_ready":          recs.get("executive_communication", {}).get("swf_ready"),
        "output_dir":         str(output_dir),
        "files": {k: str(output_dir / v) for k, v in OUTPUT_FILES.items()},
    }
    _w(output_dir / OUTPUT_FILES["audit_manifest"], manifest, "audit_manifest.json")

    log.info("JSON artifacts written to %s", output_dir)


def _w(path: Path, data: Any, label: str) -> None:
    ok = write_json_safe(path, data)
    if ok:
        log.debug("Written: %s", label)
    else:
        log.error("Failed to write: %s -> %s", label, path)

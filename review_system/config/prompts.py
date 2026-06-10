"""
review_system/config/prompts.py

ALL Groq LLM prompts for the review system.
No API calls happen here — prompts are pure strings/templates.
Imported by: claim_extractor, scoring modules, analyzers, review_orchestrator.
"""

# ===========================================================================
# CLAIM EXTRACTION
# ===========================================================================

CLAIM_EXTRACTION_SYSTEM = (
    "You are a senior institutional research auditor. "
    "Your task is to extract and classify every substantive claim in the "
    "report text provided. You must NOT use outside knowledge — evaluate ONLY "
    "what is written in the report. Return strict JSON only."
)

CLAIM_EXTRACTION_USER = """\
Below is the full text of a research report, split into sections and numbered paragraphs.

REPORT TEXT:
{report_text}

TASK:
For EVERY major claim, finding, forecast, statistic, or recommendation you find in this report text:

1. Quote or closely paraphrase the claim.
2. Record the exact section title and paragraph number.
3. Construct a location reference in this EXACT format:
   "Location -> [<section_title>] | Para <N> | \\"<first 6 words>\\" -> \\"<last 6 words>\\""
4. Evaluate the claim against 5 criteria (true/false):
   - evidence_provided: Is qualitative evidence given in the report?
   - data_provided: Is there a number, statistic, or dataset?
   - source_referenced: Is an institution, study, or publication named?
   - quantified: Does the claim include specific quantities?
   - confidence_justified: Is the degree of certainty appropriate for the evidence?
5. Classify as ONE of:
   - "supported"            — passes 4-5 criteria
   - "partially_supported"  — passes 2-3 criteria
   - "unsupported"          — passes 0-1 criteria with no source
   - "high_risk"            — specific number/forecast/timeline with no source or data
   - "speculative"          — hedging language ("may", "could") with no data

Return JSON in this EXACT structure:
{{
  "claims": [
    {{
      "claim": "<claim text>",
      "section": "<section title>",
      "paragraph": <integer>,
      "location_ref": "Location -> [<section>] | Para <N> | \\"<opening>\\" -> \\"<closing>\\"",
      "evidence_provided": <true|false>,
      "data_provided": <true|false>,
      "source_referenced": <true|false>,
      "quantified": <true|false>,
      "confidence_justified": <true|false>,
      "classification": "<classification>"
    }}
  ],
  "quantification_ratio": <integer 0-100>
}}

RULES:
- Extract EVERY significant claim (target 8-20 for a normal report).
- Every claim MUST have a location_ref.
- Do NOT invent claims not present in the report text.
- Do NOT use outside knowledge to assess credibility.
- Prefer "high_risk" for numerical forecasts with no cited source.
"""

# ===========================================================================
# SCORING
# ===========================================================================

SCORING_SYSTEM = (
    "You are a senior institutional research auditor scoring a report. "
    "Base every score ONLY on what appears in the provided report text. "
    "Do NOT use outside knowledge. "
    "Do NOT assign the same scores to unrelated dimensions. "
    "Return strict JSON only."
)

SCORING_USER = """\
REPORT TEXT (structured by section and paragraph):
{report_text}

CLAIMS AUDIT SUMMARY:
- Total claims: {total_claims}
- Supported: {supported} | Partially supported: {partial}
- Unsupported: {unsupported} | High-risk: {high_risk} | Speculative: {speculative}
- Quantification ratio: {quant_ratio}%

SCORING DIMENSIONS AND MAX POINTS:
1. Research Quality (max 30 points)
   Breadth of topic coverage, depth of analysis per section, multiple viewpoints,
   scenario/uncertainty analysis, strength of evidence-backed conclusions.

2. Evidence & Citations (max 25 points)
   Proportion of claims backed by named sources, bibliography presence,
   traceability of statistics, source diversity, absence of bare assertions.

3. Strategic Clarity (max 25 points)
   Clear "so-what" per section, explicit decision implications, risk/opportunity
   distinction, actionability of recommendations for target audience.

4. Writing & Structure (max 20 points)
   Section titles match content, logical flow, absence of undefined jargon,
   clarity and conciseness, absence of repeated or filler language.

RULES:
- Each score must be an INTEGER in [0, dimension_max].
- Every positive/negative factor MUST cite specific report content (section, claim, or quote).
- Generic phrases like "good analysis" are forbidden.
- Many unsupported/high-risk claims => Evidence & Citations <= 18/25.
- No bibliography/traceable sources => Evidence & Citations <= 14/25.

Return JSON:
{{
  "research_quality": {{
    "score": <0-30>, "max_points": 30,
    "justification": "<2-4 sentences citing specific report content>",
    "positive_factors": ["<specific strength>"],
    "negative_factors": ["<specific deficiency>"]
  }},
  "evidence_and_citations": {{
    "score": <0-25>, "max_points": 25,
    "justification": "<2-4 sentences>",
    "positive_factors": [], "negative_factors": []
  }},
  "strategic_clarity": {{
    "score": <0-25>, "max_points": 25,
    "justification": "<2-4 sentences>",
    "positive_factors": [], "negative_factors": []
  }},
  "writing_and_structure": {{
    "score": <0-20>, "max_points": 20,
    "justification": "<2-4 sentences>",
    "positive_factors": [], "negative_factors": []
  }}
}}
"""

# ===========================================================================
# ISSUE DETECTION
# ===========================================================================

ISSUE_DETECTION_SYSTEM = (
    "You are a senior institutional research auditor and strategy reviewer. "
    "Identify specific, evidence-grounded issues in the report. "
    "Never write generic observations. Every finding must reference the specific "
    "section and text. Return strict JSON only."
)

ISSUE_DETECTION_USER = """\
REPORT TEXT (structured by section and paragraph):
{report_text}

CLAIMS AUDIT:
{claims_summary}

AUDIT TASK:
Identify specific, located issues in ALL categories below.
For EACH finding include: "Location -> [<section>] | Para <N> | \\"<open>\\" -> \\"<close>\\""

If no real issue exists in a category, output:
{{"finding": "None identified — <brief reason>", "location_ref": "N/A", "severity": "Low"}}

CATEGORIES:
A. strengths           — What the report does particularly well, with specific evidence.
B. weaknesses          — Specific content/structural problems with location.
C. data_gaps           — Claims made but not backed by data. Include what data is missing.
D. weak_assumptions    — Forecasts/timelines not backed by evidence. Include missing evidence.
E. writing_flaws       — Vague language, undefined jargon, repeated phrases, filler text.
                         Quote the problematic text.
F. narrative_gaps      — Broken connections between analysis and conclusions.
G. strategic_gaps      — Missing so-what, missing decision recommendations, generic advice.
H. audience_relevance_gaps — Content mismatched for executive/board/ministerial readers.

Return JSON:
{{
  "strengths":              [{{"finding":"...","location_ref":"Location -> ...","severity":"Low"}}],
  "weaknesses":             [{{"finding":"...","location_ref":"Location -> ...","severity":"High"}}],
  "data_gaps":              [{{"section":"...","claim":"...","location_ref":"Location -> ...","missing_data":["..."],"severity":"High"}}],
  "weak_assumptions":       [{{"forecast_or_claim":"...","location_ref":"Location -> ...","missing_evidence":"...","severity":"High"}}],
  "writing_flaws":          [{{"flaw_type":"...","example":"<quote>","location_ref":"Location -> ...","severity":"Medium"}}],
  "narrative_gaps":         [{{"finding":"...","location_ref":"Location -> ...","severity":"Medium"}}],
  "strategic_gaps":         [{{"finding":"...","location_ref":"Location -> ...","severity":"High"}}],
  "audience_relevance_gaps":[{{"finding":"...","location_ref":"Location -> ...","severity":"Medium"}}]
}}
"""

# ===========================================================================
# SYNTHESIS (executive readiness + improvement tasks)
# ===========================================================================

SYNTHESIS_SYSTEM = (
    "You are a senior institutional editor finalising an audit report. "
    "Based on all audit findings, determine executive readiness and produce "
    "a prioritised improvement task list. Return strict JSON only."
)

SYNTHESIS_USER = """\
AUDIT FINDINGS SUMMARY:
{issues_summary}

SCORING:
- Overall: {overall_score}/100 | Grade: {grade}
- Research: {rq}/30 | Evidence: {ec}/25 | Strategic: {sc}/25 | Writing: {ws}/20

HIGH-RISK / UNSUPPORTED CLAIMS: {bad_claims}

TASKS:
1. For Minister, Board, SWF audiences: decide YES/NO readiness and give a one-sentence reason
   grounded in the audit findings. List specific problematic sections.

2. Produce up to 10 actionable improvement tasks ordered Critical → Low.
   Each must be specific, never generic (e.g., not "add more evidence" but
   "Section [X] claims [Y] without source — add citation to [source type]").

Return JSON:
{{
  "executive_communication": {{
    "minister_ready": <true|false>,
    "board_ready": <true|false>,
    "swf_ready": <true|false>,
    "minister_reason": "<one sentence>",
    "board_reason": "<one sentence>",
    "swf_reason": "<one sentence>",
    "flagged_sections": [{{"section":"...","issue":"..."}}]
  }},
  "improvement_tasks": [
    {{
      "priority": "Critical|High|Medium|Low",
      "section": "<section title>",
      "issue": "<specific issue>",
      "fix": "<concrete recommended fix>",
      "expected_impact": "<what improves>"
    }}
  ]
}}
"""

# ===========================================================================
# COMBINED ANALYSIS  (lean mode — 1 call replaces 6 separate analyzer calls)
# ===========================================================================

COMBINED_ANALYSIS_SYSTEM = (
    "You are a senior institutional research auditor and strategy reviewer. "
    "In a single pass, analyse all quality dimensions of the report: evidence, "
    "citations, writing, strategy, narrative structure, and audience readiness. "
    "Base every finding ONLY on the provided report text. "
    "Never produce generic observations — every finding must cite a specific section "
    "and paragraph. Return strict JSON only."
)

COMBINED_ANALYSIS_USER = """\
REPORT TEXT (structured by section and paragraph):
{report_text}

SECTION LIST: {section_list}

CLAIMS AUDIT:
- Total claims  : {total_claims}
- Supported     : {supported} | Partially supported: {partial}
- Unsupported   : {unsupported} | High-risk: {high_risk} | Speculative: {speculative}
- Source-referenced claims: {sourced}
- Quantification ratio: {quant_ratio}%

High-risk / unsupported claims:
{bad_claims_list}

TASK: In a single response, cover ALL categories A through I below.
Location format: "Location -> [<section>] | Para <N> | \"<first 6 words>\" -> \"<last 6 words>\""
If no issue exists in a category, output:
  {"finding": "None identified — <brief reason>", "location_ref": "N/A", "severity": "Low"}

A. STRENGTHS — What the report does particularly well. Cite specific sections.
B. WEAKNESSES — Specific content/structural problems with location.
C. DATA GAPS — Claims made without supporting data. State what data is missing.
D. WEAK ASSUMPTIONS — Forecasts or timelines not backed by evidence.
E. CITATION QUALITY — Assess named sources, bibliography presence, source diversity,
   statistic traceability. Produce separate citation_strengths and citation_weaknesses lists.
F. WRITING FLAWS — Vague language, undefined jargon, repeated phrases, filler text,
   overloaded sentences. Quote the problematic text exactly.
G. NARRATIVE GAPS — Broken argument flow, orphaned analysis, weak intro/conclusion.
H. STRATEGIC GAPS — Missing so-what, generic advice, absent call-to-action,
   no risk/opportunity split.
I. AUDIENCE READINESS — For Minister, Board, SWF: YES/NO readiness with a one-sentence
   reason grounded in the report text.

Return JSON in this EXACT structure:
{{
  "strengths":         [{{"finding":"...","location_ref":"Location -> ...","severity":"Low"}}],
  "weaknesses":        [{{"finding":"...","location_ref":"Location -> ...","severity":"High"}}],
  "data_gaps":         [{{"section":"...","claim":"...","location_ref":"Location -> ...","missing_data":["..."],"severity":"High"}}],
  "weak_assumptions":  [{{"forecast_or_claim":"...","location_ref":"Location -> ...","missing_evidence":"...","severity":"High"}}],
  "citation_strengths":[{{"finding":"...","location_ref":"Location -> ...","severity":"Low"}}],
  "citation_weaknesses":[{{"finding":"...","location_ref":"Location -> ...","severity":"High"}}],
  "has_bibliography":  false,
  "named_sources_count": 0,
  "writing_flaws":     [{{"flaw_type":"vague_statement|undefined_jargon|repeated_phrase|weak_transition|filler_text|overloaded_sentence","example":"<exact quote>","location_ref":"Location -> ...","severity":"High|Medium|Low","suggestion":"<one-line fix>"}}],
  "narrative_gaps":    [{{"gap_type":"circular|broken_flow|orphaned|weak_intro|weak_conclusion","finding":"...","location_ref":"Location -> ...","severity":"High|Medium|Low"}}],
  "overall_narrative_coherence": "Strong|Moderate|Weak",
  "strategic_gaps":    [{{"gap_type":"missing_so_what|generic_recommendation|no_risk_opportunity_split|missing_stakeholder|absent_call_to_action","finding":"...","location_ref":"Location -> ...","severity":"Critical|High|Medium|Low"}}],
  "has_explicit_recommendations": false,
  "has_risk_opportunity_split":   false,
  "audience_relevance_gaps":[{{"audience":"Minister|Board|SWF","finding":"...","location_ref":"Location -> ...","severity":"High|Medium|Low"}}],
  "minister_ready":    false,
  "board_ready":       false,
  "swf_ready":         false,
  "minister_reason":   "<one sentence grounded in report content>",
  "board_reason":      "<one sentence>",
  "swf_reason":        "<one sentence>",
  "flagged_sections":  [{{"section":"...","issue":"..."}}]
}}
"""

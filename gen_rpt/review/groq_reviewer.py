import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from .claim_extractor import extract_claims
from .score_engine import evaluate_dimensions, calculate_final_score
from .recommendation_engine import generate_recommendations
from .review_report import generate_review_artifacts


class GroqClient:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def chat_json(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }
        response = requests.post(self.url, headers=self.headers, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)


def run_groq_review(output_dir: Path) -> Dict[str, Any]:
    print("[REVIEW] Loading report artifacts")
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("[REVIEW] GROQ_API_KEY not found. Skipping AI Review.")
        return {}
        
    client = GroqClient(api_key=api_key)
    
    report_payload_path = output_dir / "report_payload.json"
    sources_path = output_dir / "sources.json"
    plan_path = output_dir / "research_plan.json"
    qa_path = output_dir / "qa_result.json"
    html_path = output_dir / "report.html"
    
    if not report_payload_path.exists():
        print("[REVIEW] report_payload.json missing. Skipping.")
        return {}
        
    claims_path = output_dir / "claims.json"
    claims = extract_claims(client, report_payload_path, claims_path)
    
    print("[REVIEW] Sending review request to Groq")
    dimensions = evaluate_dimensions(client, report_payload_path, sources_path, html_path)
    
    print("[REVIEW] Receiving review results")
    print("[REVIEW] Calculating scores")
    scores = calculate_final_score(dimensions)
    
    print("[REVIEW] Generating recommendations")
    recommendations = generate_recommendations(client, report_payload_path, dimensions)
    
    review_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "scores": scores,
        "recommendations": recommendations,
        "claims": claims,
        "raw_dimensions": dimensions
    }
    
    with open(report_payload_path, 'r', encoding='utf-8') as f:
        report_payload = json.load(f)
        
    print("[REVIEW] Writing review artifacts")
    generate_review_artifacts(output_dir, report_payload, review_data)
    
    print("[REVIEW] Review complete")
    return review_data


def run_groq_review_file(file_path: Path, output_dir: Path) -> Dict[str, Any]:
    from .claim_extractor import extract_claims_text
    from .score_engine import evaluate_dimensions_text
    from .recommendation_engine import generate_recommendations_text
    from .review_report import generate_review_artifacts_text
    
    print(f"[REVIEW] Loading file: {file_path}")
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("[REVIEW] GROQ_API_KEY not found. Skipping AI Review.")
        return {}
        
    client = GroqClient(api_key=api_key)
    
    if not file_path.exists():
        print(f"[REVIEW] File {file_path} not found. Skipping.")
        return {}
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        print(f"[REVIEW] Failed to read file {file_path}: {e}")
        return {}
        
    claims_path = output_dir / "claims.json"
    output_dir.mkdir(parents=True, exist_ok=True)
    claims = extract_claims_text(client, file_content, claims_path)
    
    print("[REVIEW] Sending review request to Groq")
    dimensions = evaluate_dimensions_text(client, file_content)
    
    print("[REVIEW] Receiving review results")
    print("[REVIEW] Calculating scores")
    scores = calculate_final_score(dimensions)
    
    print("[REVIEW] Generating recommendations")
    recommendations = generate_recommendations_text(client, file_content, dimensions)
    
    review_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "scores": scores,
        "recommendations": recommendations,
        "claims": claims,
        "raw_dimensions": dimensions
    }
    
    print("[REVIEW] Writing review artifacts")
    generate_review_artifacts_text(output_dir, file_content, review_data)
    
    print("[REVIEW] Review complete")
    return review_data

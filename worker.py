from celery_app import celery_app
from crew_runner import run_crew
from database import SessionLocal, AnalysisResult
import json
import ast


# =====================================================
# Helper: Convert sets → lists for JSON safety
# =====================================================
def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, set):
        return [make_json_safe(v) for v in obj]  # convert set → list
    else:
        return obj


@celery_app.task
def process_financial_analysis(query: str, file_path: str, filename: str):

    # Run Crew
    response = run_crew(query=query, file_path=file_path)

    # =====================================================
    # Ensure response is dict
    # =====================================================
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except Exception:
            try:
                response = ast.literal_eval(response)
            except Exception:
                response = {"error": "Invalid response format"}

    # =====================================================
    # Convert sets to JSON-safe structures
    # =====================================================
    response = make_json_safe(response)

    # =====================================================
    # Store in DB
    # =====================================================
    db = SessionLocal()

    record = AnalysisResult(
        filename=filename,
        query=query,
        result=json.dumps(response)  # now safe
    )

    db.add(record)
    db.commit()
    db.close()

    # Return dict to API
    return response
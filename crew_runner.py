import time
import json
import re
import ast
from crewai import Crew, Process

# Updated imports (ONLY 2 AGENTS)
from agents import financial_analyst, verifier

# Updated tasks (ONLY 2 TASKS)
from task import analyze_financial_document, verification

from tools import FinancialDocumentTool


# =========================================================
# JSON EXTRACTION HELPER (ROBUST VERSION)
# =========================================================
def extract_json(text: str):
    """
    Robust JSON extraction from LLM output.

    Handles:
    - Extra text before/after JSON
    - Escaped JSON
    - Python-style dicts with single quotes
    - Nested strings
    """

    if isinstance(text, dict):
        return text

    raw = str(text)

    # Attempt direct JSON load
    try:
        return json.loads(raw)
    except Exception:
        pass

    # Extract JSON block using regex
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return {
            "error": "No JSON found in response",
            "raw_output": raw
        }

    json_str = match.group()

    # Try strict JSON again
    try:
        return json.loads(json_str)
    except Exception:
        pass

    # Try Python dict parsing
    try:
        return ast.literal_eval(json_str)
    except Exception:
        pass

    # Final fallback
    return {
        "error": "Failed to parse JSON response",
        "raw_output": raw
    }


# =========================================================
# MAIN CREW RUNNER
# =========================================================
def run_crew(query: str, file_path: str = "data/sample.pdf"):

    # =========================================================
    # READ DOCUMENT
    # =========================================================
    document_text = FinancialDocumentTool._read_data_internal(file_path)

    if not document_text or len(document_text.strip()) == 0:
        return {
            "error": "No readable content extracted from document."
        }

    # Token safety guard
    document_text = document_text[:3500]

    # =========================================================
    # SYSTEM CONTEXT
    # =========================================================
    system_context = """
You are an AI financial analysis system.

General Rules:
- Use ONLY provided document content.
- Do NOT hallucinate information.
- If data missing → clearly state limitation.
- Maintain professional financial reasoning.
- Ensure structured JSON outputs as requested.
"""

    context = {
        "query": query,
        "file_path": file_path,
        "document_text": document_text,
        "system_context": system_context
    }

    # =========================================================
    # CREW CONFIGURATION
    # =========================================================
    financial_crew = Crew(
        agents=[
            verifier,
            financial_analyst
        ],
        tasks=[
            verification,
            analyze_financial_document
        ],
        process=Process.sequential,
        verbose=True
    )

    # =========================================================
    # RETRY LOGIC
    # =========================================================
    max_retries = 3

    for attempt in range(max_retries):
        try:
            print(f"\n🚀 Running Crew Attempt {attempt + 1}")

            result = financial_crew.kickoff(context)

            if not result:
                raise Exception("Empty response from crew.")

            # Extract JSON safely
            parsed_result = extract_json(result)

            return parsed_result

        except Exception as e:

            error_msg = str(e).lower()
            print(f"⚠️ Error occurred: {e}")

            if "rate" in error_msg or "limit" in error_msg or "429" in error_msg:
                wait_time = 20 * (attempt + 1)
                print(f"⏳ Rate limit detected. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    return {
        "error": "Crew execution failed after retries."
    }
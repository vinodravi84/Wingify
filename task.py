## Importing libraries and files
from crewai import Task

# Updated agents (ONLY 2)
from agents import financial_analyst, verifier


# =========================================================
# TASK 1 — Document Verification
# =========================================================
verification = Task(
    description="""
You are a financial document verification specialist.

IMPORTANT:
Financial document content:
{document_text}

Your task is to determine whether the uploaded file contains genuine financial
or business-related information.

Reasoning Steps:

1. Carefully read the document content.
2. Look for indicators such as:
   - Financial statements
   - Revenue or expense figures
   - Profit or loss metrics
   - Balance sheet or cash flow data
   - Operational or business metrics
3. Evaluate whether the document is financial in nature.
4. If it is NOT financial, clearly explain why.

Rules:

- Do NOT assume information.
- Do NOT hallucinate missing data.
- Base conclusions ONLY on the provided content.
- Be precise and evidence-driven.
""",

    expected_output="""
Return ONLY valid JSON in the following format:

{
  "verification": {
    "document_type": "",
    "confidence_level": "",
    "supporting_evidence": "",
    "conclusion": ""
  }
}

Rules:
- Output only JSON
- No markdown
- No extra text
""",

    agent=verifier,
    async_execution=False
)


# =========================================================
# TASK 2 — Comprehensive Financial Analysis
# =========================================================
analyze_financial_document = Task(
    description="""
You are a senior financial analyst and investment strategist.

IMPORTANT:
Financial document content:
{document_text}

User query:
{query}

Your objective is to perform a deep, professional financial analysis using ONLY
the information provided in the document.

You MUST follow this reasoning workflow:

STEP 1 — Verification Awareness
Confirm that the document contains financial information.

STEP 2 — Financial Extraction
Identify and extract:
- Revenue
- Net income / profit
- Expenses
- Margins
- Cash flow
- Debt or liabilities
- Growth indicators

STEP 3 — Performance Interpretation
Analyze trends, strengths, weaknesses, and operational signals.

STEP 4 — Investment Evaluation
Derive investment insights supported by financial evidence.

STEP 5 — Risk Assessment
Identify realistic financial and business risks based on data.

Critical Rules:

- Use ONLY the provided document content.
- Do NOT fabricate numbers or facts.
- If information is missing → explicitly state limitation.
- Avoid generic statements.
- Provide analytical reasoning like a professional analyst.
- Output MUST be valid JSON.
- Do NOT include any text outside JSON.
""",

    expected_output="""
Return ONLY valid JSON in the following structure:

{
  "verification": {
    "document_type": "",
    "confidence_level": "",
    "supporting_evidence": "",
    "conclusion": ""
  },
  "financial_analysis": {
    "key_metrics": "",
    "performance_trends": "",
    "strengths": "",
    "weaknesses": "",
    "observations": ""
  },
  "investment_insights": {
    "outlook": "",
    "supporting_evidence": "",
    "opportunities": "",
    "concerns": "",
    "investor_profile": ""
  },
  "risk_assessment": {
    "key_risks": "",
    "risk_severity": "",
    "financial_stability": "",
    "future_concerns": "",
    "overall_rating": ""
  }
}

Rules:

- Output ONLY JSON.
- No markdown formatting.
- No explanation text.
- No extra characters before or after JSON.
""",

    agent=financial_analyst,
    async_execution=False,
)
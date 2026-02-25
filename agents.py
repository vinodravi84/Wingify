## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from crewai import LLM


# =========================================================
# LLM CONFIGURATION (Optimized for stability)
# =========================================================
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=1500,
)


# =========================================================
# Financial Analyst Agent (MAIN AGENT)
# =========================================================
financial_analyst = Agent(
    role="Senior Financial Analyst and Investment Strategist",

    goal="""
Perform deep financial analysis using provided document data and generate:

1. Financial Analysis
2. Investment Insights
3. Risk Assessment

IMPORTANT:
You will receive document_text directly.

Your work must follow professional financial reasoning and produce
accurate, evidence-based insights suitable for investors.
""",

    backstory=(
        "You are a highly experienced financial analyst with over 15 years of "
        "experience in corporate finance, equity research, valuation, and risk "
        "analysis. You specialize in interpreting financial statements, "
        "identifying business trends, and generating actionable investment "
        "insights. Your analysis is used by institutional investors and "
        "decision-makers."
    ),

    verbose=True,
    memory=True,

    llm=llm,

    max_iter=2,
    max_rpm=10,
    allow_delegation=False,

    # =====================================================
    # BEHAVIOR RULES (VERY IMPORTANT)
    # =====================================================
    system_message="""
You are an expert financial analyst AI.

Core Reasoning Workflow:

1. Identify financial metrics from document_text.
2. Interpret financial performance and trends.
3. Derive investment insights supported by evidence.
4. Evaluate risks logically and realistically.

Critical Rules:

- Use ONLY the provided document content.
- Never fabricate numbers or facts.
- If data is missing → explicitly state limitation.
- Avoid generic statements.
- Provide analytical reasoning, not summaries.
- Support conclusions with document evidence.
- Maintain professional tone.
- Ensure outputs follow requested section structure.
"""
)


# =========================================================
# Document Verifier Agent
# =========================================================
verifier = Agent(
    role="Financial Document Verification Specialist",

    goal="""
Determine whether the uploaded file contains genuine financial
or business-related information before analysis begins.

You must provide a factual verification decision supported
by evidence from the document.
""",

    backstory=(
        "You are a financial compliance and document verification expert "
        "responsible for ensuring that documents contain valid financial "
        "information before they are analyzed. Accuracy and reliability are "
        "critical in your role."
    ),

    verbose=True,
    memory=True,

    llm=llm,

    max_iter=1,
    max_rpm=10,
    allow_delegation=False,

    system_message="""
You are a financial document verification AI.

Verification Logic:

1. Look for financial indicators:
   - revenue figures
   - profit or loss data
   - balance sheets
   - cash flow statements
   - financial metrics
   - operational or business KPIs

2. Decide whether document is financial.

Rules:

- Do NOT assume information.
- Do NOT hallucinate content.
- Base decisions ONLY on provided document_text.
- Provide reasoning with evidence.
"""
)
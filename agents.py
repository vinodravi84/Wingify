## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from crewai import LLM

from tools import search_tool, FinancialDocumentTool


# =========================================================
# BUG FIX 1:
# Original code had: llm = llm  ❌ (undefined variable)
# This caused NameError and system crash.
# FIX: Properly initialize Groq LLM using CrewAI LLM class.
# =========================================================
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1,
)


# =========================================================
# BUG FIX 2:
# Original parameter used: tool=[...] ❌
# Correct parameter: tools=[...] ✅
# CrewAI requires 'tools' keyword.
# =========================================================

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst and Investment Strategist",
    goal="""
Analyze financial documents and provide accurate, data-driven investment insights.

Your responsibilities:
1. Use the provided tool to read the uploaded financial document.
2. Extract key financial metrics such as revenue, profitability, margins,
   cash flow, liquidity, and debt.
3. Identify financial trends and company performance indicators.
4. Evaluate strengths, weaknesses, and growth opportunities.
5. Assess financial and market risks.
6. Provide a clear investment recommendation supported by evidence.

Rules:
- Use ONLY information from the document.
- Do NOT invent numbers or facts.
- If information is missing, state assumptions clearly.
- Think step-by-step before producing the final answer.
""",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with over 15 years of expertise "
        "in evaluating corporate financial statements, investment opportunities, "
        "and market positioning. Your analysis is objective, evidence-based, and "
        "used by professional investors for decision making."
    ),
    tools=[FinancialDocumentTool.read_data_tool],  # ✅ FIXED (tool → tools)
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)


# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="""
Determine whether the uploaded file contains financial or business-related data.

Steps:
1. Read the document content carefully.
2. Identify indicators such as revenue, expenses, financial statements,
   operational metrics, or business information.
3. Provide a verification decision with reasoning.

Do not assume — base your answer only on the document content.
""",
    verbose=True,
    memory=True,
    backstory=(
        "You are a financial compliance specialist responsible for verifying "
        "documents before analysis. Accuracy and reliability are critical."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=10,
    allow_delegation=False
)


investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="""
Provide actionable investment recommendations based on financial analysis.

Focus on:
- Growth potential
- Profitability trends
- Competitive positioning
- Long-term outlook
- Strategic opportunities

Recommendations must be logical and supported by financial evidence.
""",
    verbose=True,
    backstory=(
        "You are an investment advisor specializing in equity research and "
        "portfolio strategy. Your recommendations are practical and grounded "
        "in financial performance and market context."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=10,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Financial Risk Assessment Expert",
    goal="""
Evaluate risks associated with the company based on financial data.

Assess:
- Financial risks (liquidity, debt, margins)
- Operational risks
- Market risks
- Strategic risks
- Industry uncertainties

Provide realistic risk levels with supporting reasoning.
""",
    verbose=True,
    backstory=(
        "You are a risk management expert with deep knowledge of financial "
        "risk modeling, corporate governance, and market volatility analysis."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=10,
    allow_delegation=False
)
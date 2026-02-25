## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier
from tools import FinancialDocumentTool


# =========================================================
# TASK 1 — Comprehensive Financial Analysis
# =========================================================
analyze_financial_document = Task(
    description="""
You are given a financial document and a user query.

IMPORTANT:
The financial document file path is: {file_path}

Your job is to perform a professional financial analysis based strictly on the
contents of the document.

Instructions:

1. Use the "Read Financial Document" tool with the provided file path.
2. Identify key financial metrics such as:
   - Revenue
   - Profit / Net Income
   - Expenses
   - Growth trends
   - Margins
   - Debt and liabilities
   - Cash flow indicators
3. Extract meaningful insights relevant to the user query: {query}
4. Provide investment insights based only on the document data.
5. Highlight important financial strengths and weaknesses.
6. Do NOT fabricate information or external data.
7. If information is missing, clearly state assumptions or limitations.
8. Maintain professional financial reasoning.
""",

    expected_output="""
Provide a structured financial analysis report with the following sections:

1. Executive Summary
2. Key Financial Highlights
3. Performance Analysis
4. Investment Insights
5. Risk Factors Identified
6. Market or Strategic Observations
7. Final Recommendation

The response should be professional, accurate, and grounded in the document.
""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


# =========================================================
# TASK 2 — Investment Recommendation
# =========================================================
investment_analysis = Task(
    description="""
IMPORTANT:
The financial document file path is: {file_path}

Based on the financial document, generate investment recommendations.

Instructions:

1. Use the "Read Financial Document" tool with the provided file path.
2. Evaluate company performance, financial stability, and growth potential.
3. Identify possible investment opportunities or concerns.
4. Consider valuation signals if present.
5. Align recommendations with realistic financial reasoning.
6. Avoid speculation without evidence.
7. If insufficient data exists, clearly mention uncertainty.

User query: {query}
""",

    expected_output="""
Provide investment recommendations including:

- Investment Outlook (Positive / Neutral / Negative)
- Supporting Financial Evidence
- Potential Opportunities
- Key Concerns
- Suggested Investor Profile (Conservative / Moderate / Aggressive)
- Recommendation Summary
""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


# =========================================================
# TASK 3 — Risk Assessment
# =========================================================
risk_assessment = Task(
    description="""
IMPORTANT:
The financial document file path is: {file_path}

Analyze financial risks based on the uploaded document.

Instructions:

1. Use the "Read Financial Document" tool with the provided file path.
2. Identify financial, operational, and market risks from the document.
3. Evaluate:
   - Debt levels
   - Profit volatility
   - Cash flow stability
   - Dependency risks
   - Macroeconomic exposure (if mentioned)
4. Categorize risks by severity level.
5. Provide realistic mitigation considerations if applicable.
6. Do not exaggerate risks beyond evidence.

User query: {query}
""",

    expected_output="""
Provide a structured risk report:

- Key Risk Factors
- Risk Severity (Low / Medium / High)
- Financial Stability Assessment
- Potential Future Concerns
- Risk Mitigation Observations
- Overall Risk Rating
""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


# =========================================================
# TASK 4 — Document Verification
# =========================================================
verification = Task(
    description="""
IMPORTANT:
The financial document file path is: {file_path}

Verify whether the uploaded file is a financial document.

Instructions:

1. Use the "Read Financial Document" tool with the provided file path.
2. Determine whether the document contains financial information.
3. Identify indicators such as:
   - Financial statements
   - Earnings reports
   - Balance sheet data
   - Revenue or expense figures
4. If not financial, clearly state the reason.
5. Do not assume or hallucinate.

Provide a factual verification result.
""",

    expected_output="""
Provide:

- Document Type Identification
- Confidence Level (High / Medium / Low)
- Supporting Evidence
- Verification Conclusion
""",

    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)
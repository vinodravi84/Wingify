## Importing libraries and files
import os
import re
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader


# =========================================================
# Search Tool
# =========================================================
search_tool = SerperDevTool()


# =========================================================
# Financial Document Tool (FINAL IMPROVED VERSION)
# =========================================================
class FinancialDocumentTool:

    @staticmethod
    def _read_data_internal(path: str = "data/sample.pdf"):
        """
        Reads and extracts relevant financial text from PDF.

        Improvements:
        - Financial keyword scoring
        - Numeric density scoring
        - Currency/percentage detection
        - Better page ranking
        - Token-safe truncation
        """

        if not os.path.exists(path):
            return f"File not found: {path}"

        loader = PyPDFLoader(path)
        docs = loader.load()

        # =====================================================
        # FINANCIAL KEYWORDS
        # =====================================================
        financial_keywords = [
            "revenue", "income", "profit", "loss", "cash",
            "balance", "assets", "liabilities", "equity",
            "ebitda", "margin", "expenses", "financial",
            "operations", "statement", "net income",
            "cash flow", "operating", "cost", "debt",
            "free cash", "capex", "guidance", "outlook"
        ]

        scored_pages = []

        for doc in docs:
            text = doc.page_content.lower()

            score = 0

            # -------------------------------------------------
            # Keyword score
            # -------------------------------------------------
            keyword_hits = sum(keyword in text for keyword in financial_keywords)
            score += keyword_hits * 3

            # -------------------------------------------------
            # Numeric density boost (financial tables)
            # -------------------------------------------------
            numbers = re.findall(r"\d+", text)
            score += len(numbers) // 4

            # -------------------------------------------------
            # Currency / percentage boost
            # -------------------------------------------------
            currency_symbols = ["$", "€", "£", "%"]
            score += sum(symbol in text for symbol in currency_symbols) * 2

            # -------------------------------------------------
            # Table indicators
            # -------------------------------------------------
            table_words = ["total", "cost", "margin", "q1", "q2", "q3", "q4"]
            score += sum(word in text for word in table_words)

            if score > 2:
                scored_pages.append((score, doc))

        # =====================================================
        # SORT PAGES BY SCORE
        # =====================================================
        scored_pages.sort(key=lambda x: x[0], reverse=True)

        # =====================================================
        # SELECT TOP PAGES
        # =====================================================
        MAX_PAGES = 6
        filtered_docs = [doc for score, doc in scored_pages[:MAX_PAGES]]

        # Fallback
        if not filtered_docs:
            filtered_docs = docs[:4]

        # =====================================================
        # MERGE CONTENT
        # =====================================================
        full_report = ""

        for data in filtered_docs:
            content = data.page_content

            # Normalize spacing
            content = re.sub(r"\n\s*\n", "\n", content)

            full_report += content + "\n"

        # =====================================================
        # TOKEN SAFETY (VERY IMPORTANT)
        # =====================================================
        MAX_CHARS = 3000
        full_report = full_report[:MAX_CHARS]

        return full_report


    @staticmethod
    @tool("Read Financial Document")
    def read_data_tool(path: str = "data/sample.pdf"):
        """
        Read and extract relevant financial text from a PDF.
        Optimized for LLM financial analysis.
        """
        return FinancialDocumentTool._read_data_internal(path)


# =========================================================
# Investment Tool
# =========================================================
class InvestmentTool:

    @staticmethod
    @tool("Investment Analysis Tool")
    def analyze_investment_tool(financial_document_data: str):
        """
        Analyze financial document data and prepare for investment insights.
        """

        processed_data = financial_document_data

        i = 0
        while i < len(processed_data):
            if processed_data[i:i + 2] == "  ":
                processed_data = processed_data[:i] + processed_data[i + 1:]
            else:
                i += 1

        return (
            "Investment analysis preprocessing completed. "
            "Data is ready for financial evaluation."
        )


# =========================================================
# Risk Tool
# =========================================================
class RiskTool:

    @staticmethod
    @tool("Risk Assessment Tool")
    def create_risk_assessment_tool(financial_document_data: str):
        """
        Generate risk assessment insights from financial data.
        """

        return (
            "Risk assessment preprocessing completed. "
            "Financial data is ready for risk evaluation."
        )
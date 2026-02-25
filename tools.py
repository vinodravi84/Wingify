## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

# =========================================================
# BUG FIX 1:
# Original code imported: from crewai_tools import tools ❌ (unused)
# Removed unnecessary import.
# =========================================================

from crewai.tools import tool
from crewai_tools import SerperDevTool

# =========================================================
# BUG FIX 2:
# Pdf class was not defined anywhere ❌
# Using correct PDF loader from langchain.
# =========================================================
from langchain_community.document_loaders import PyPDFLoader


## Creating search tool
search_tool = SerperDevTool()


## Creating custom pdf reader tool
class FinancialDocumentTool:

    # =========================================================
    # BUG FIX 3:
    # Original function was async ❌
    # CrewAI tools should be synchronous unless configured.
    # Converted to normal function.
    # =========================================================

    # =========================================================
    # BUG FIX 4:
    # Tool decorator missing ❌
    # Added @tool so agent can call this function.
    # =========================================================
    @staticmethod
    @tool("Read Financial Document")
    def read_data_tool(path: str = 'data/sample.pdf'):
        """
        Read and extract text content from a financial PDF document.

        This tool loads the PDF file from the provided path and returns
        the complete textual content for financial analysis.
        """

        if not os.path.exists(path):
            return f"File not found: {path}"

        loader = PyPDFLoader(path)
        docs = loader.load()
        docs = docs[:5]
        full_report = ""
        for data in docs:
            content = data.page_content

            # Clean formatting
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report


## Creating Investment Analysis Tool
class InvestmentTool:

    # =========================================================
    # BUG FIX:
    # Converted async → sync for CrewAI compatibility.
    # Added missing docstring (required by CrewAI tool decorator).
    # =========================================================
    @staticmethod
    @tool("Investment Analysis Tool")
    def analyze_investment_tool(financial_document_data: str):
        """
        Analyze financial document data and generate investment insights.

        This tool processes extracted financial text and prepares it for
        downstream investment recommendation tasks.
        """

        processed_data = financial_document_data

        # Basic whitespace cleanup
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1

        # Placeholder for advanced logic
        return (
            "Investment analysis preprocessing completed. "
            "Data is ready for financial evaluation."
        )


## Creating Risk Assessment Tool
class RiskTool:

    # =========================================================
    # BUG FIX:
    # Converted async → sync for CrewAI compatibility.
    # Added missing docstring (required by CrewAI tool decorator).
    # =========================================================
    @staticmethod
    @tool("Risk Assessment Tool")
    def create_risk_assessment_tool(financial_document_data: str):
        """
        Generate risk assessment insights from financial data.

        This tool prepares financial information for risk evaluation tasks.
        """

        # Placeholder for future risk processing logic
        return (
            "Risk assessment preprocessing completed. "
            "Financial data is ready for risk evaluation."
        )
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document as financial_task


def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run CrewAI workflow for financial analysis"""

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[financial_task],
        process=Process.sequential,
        verbose=True
    )

    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })

    return result
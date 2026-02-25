from celery_app import celery_app
from crew_runner import run_crew
from database import SessionLocal, AnalysisResult


@celery_app.task
def process_financial_analysis(query: str, file_path: str, filename: str):

    response = run_crew(query=query, file_path=file_path)

    analysis_result = str(response)

    db = SessionLocal()

    record = AnalysisResult(
        filename=filename,
        query=query,
        result=analysis_result
    )

    db.add(record)
    db.commit()
    db.close()

    return analysis_result
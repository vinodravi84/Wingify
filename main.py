from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

# ================================
# DB IMPORTS
# ================================
from database import SessionLocal, AnalysisResult, init_db

# ================================
# CELERY IMPORTS
# ================================
from worker import process_financial_analysis
from celery.result import AsyncResult
from celery_app import celery_app


app = FastAPI(title="Financial Document Analyzer")

# ================================
# INIT DATABASE (creates tables)
# ================================
init_db()


# =========================================================
# Health Check
# =========================================================
@app.get("/")
async def root():
    return {
        "message": "Financial Document Analyzer API is running",
        "status": "healthy"
    }


# =========================================================
# Analyze Endpoint (ASYNC WITH WORKER)
# =========================================================
@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """
    Upload financial document and start background analysis task
    """

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query
        if not query:
            query = "Analyze this financial document for investment insights"

        # =========================================================
        # SEND TASK TO CELERY WORKER
        # =========================================================
        task = process_financial_analysis.delay(
            query=query.strip(),
            file_path=file_path,
            filename=file.filename
        )

        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Analysis started in background",
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )


# =========================================================
# TASK STATUS ENDPOINT
# =========================================================
@app.get("/task/{task_id}")
def get_task_status(task_id: str):
    """
    Check status of background analysis task
    """

    task_result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }


# =========================================================
# History Endpoint  ⭐ BONUS FEATURE
# =========================================================
@app.get("/history")
def get_history():
    """Get all previous analysis results"""

    db = SessionLocal()
    records = db.query(AnalysisResult).all()
    db.close()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "query": r.query,
            "result": r.result,
            "created_at": r.created_at
        }
        for r in records
    ]


# =========================================================
# Run Server
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
# 📊 Financial Document Analyzer — CrewAI Debug Challenge

## Overview

This project is an AI-powered financial document analysis system built using **CrewAI**. It processes uploaded financial reports and generates structured investment insights using autonomous AI agents.

The repository was provided as part of an AI internship debugging challenge and initially contained multiple deterministic bugs, misconfigured tools, and inefficient prompts that prevented reliable execution. These issues have been identified, fixed, and the system has been upgraded with production-grade enhancements including asynchronous processing and database persistence.

---

## 🚀 Key Features

* Upload financial PDF documents for analysis
* AI-driven financial insights using CrewAI agents
* Structured investment recommendations
* Background processing with Celery & Redis (queue worker bonus)
* Persistent storage using SQLite database (database bonus)
* Task status tracking API
* Analysis history retrieval

---

## 🐛 Bugs Identified and Fixes

### 1. Undefined LLM Initialization

**Original Code**

```python
llm = llm
```

**Issue**

* Undefined variable caused immediate runtime crash.

**Fix**

* Properly initialized CrewAI LLM using Groq model configuration.

---

### 2. Incorrect Agent Parameter (`tool` instead of `tools`)

**Original Code**

```python
tool=[FinancialDocumentTool.read_data_tool]
```

**Issue**

* CrewAI expects `tools`, not `tool`.
* Agent could not access tools.

**Fix**

```python
tools=[FinancialDocumentTool.read_data_tool]
```

---

### 3. Broken Tool Implementation

**Original Issues**

* Tool defined as `async` (incompatible with CrewAI default execution)
* Missing `@tool` decorator
* Undefined `Pdf` class
* Incorrect imports from `crewai_tools`

**Fixes**

* Converted tool to synchronous function
* Added CrewAI `@tool` decorator
* Replaced with `PyPDFLoader`
* Cleaned imports and logic

---

### 4. Crew Input Not Passing File Path

**Original Code**

```python
result = financial_crew.kickoff({'query': query})
```

**Issue**

* Task required file path but was never provided.
* Agents could not read uploaded documents.

**Fix**

```python
result = financial_crew.kickoff({
    "query": query,
    "file_path": file_path
})
```

---

### 5. Poor Prompt Engineering (Inefficient Prompts)

**Original Problems**

* Prompts encouraged hallucination:

  * “Make up investment advice”
  * “Just assume everything”
* No constraints or structure
* No tool usage instructions
* No reasoning guidance

**Fix**

* Added professional financial analysis instructions
* Enforced tool usage
* Added anti-hallucination rules
* Structured output sections
* Step-by-step reasoning guidance

Result: significantly improved determinism and accuracy.

---

### 6. Missing Persistence Layer

**Original System**

* No storage for analysis results.

**Fix**

* Added SQLite database with SQLAlchemy
* Stored filename, query, results, timestamps
* Added `/history` endpoint

---

### 7. Blocking API Execution

**Original System**

* Crew execution ran synchronously inside API.
* Not scalable for multiple users.

**Fix (Bonus)**

* Implemented Celery + Redis queue worker.
* Background task processing with task IDs.
* Status tracking endpoint.

---

### 8. Circular Import Issues During Worker Integration

**Issue**

* Worker and main modules importing each other.

**Fix**

* Introduced dedicated orchestration layer (`crew_runner.py`).

---

## 🧠 Prompt Improvements

Enhancements include:

* Explicit tool usage instructions
* Structured financial report sections
* Clear constraints against hallucination
* Evidence-based reasoning
* Professional tone requirements
* Missing data handling rules

These changes improved reliability and output quality significantly.

---

## 🏗️ System Architecture

```
Client
   ↓
FastAPI Backend
   ↓
Celery Queue (Redis)
   ↓
Worker Process
   ↓
CrewAI Agents
   ↓
LLM (Groq)
   ↓
SQLite Database
```

---

## ⚡ Queue Worker Implementation (Bonus)

Asynchronous processing implemented using:

* Celery — distributed task queue
* Redis — broker and result backend

This enables concurrent processing and non-blocking API responses.

---

## 💾 Database Integration (Bonus)

Database stores:

* Filename
* User query
* AI analysis
* Timestamp

Provides persistent storage and retrieval via API.

---

## 📂 Project Structure

```
project/
│── main.py                # FastAPI application
│── worker.py              # Celery worker
│── celery_app.py          # Celery configuration
│── crew_runner.py         # CrewAI orchestration
│── agents.py              # AI agents
│── task.py                # CrewAI tasks
│── tools.py               # Custom tools
│── database.py            # Database models
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <repo-link>
cd financial-document-analyzer
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_key
```

---

## 🔴 Run Redis

Using Docker:

```
docker run -d -p 6379:6379 redis
```

---

## ▶️ Start Worker

Windows:

```
celery -A worker worker --loglevel=info --pool=solo
```

Linux/Mac:

```
celery -A worker worker --loglevel=info
```

---

## ▶️ Start API Server

```
uvicorn main:app --reload
```

---

## 📡 API Endpoints

### Health Check

```
GET /
```

---

### Analyze Document

```
POST /analyze
```

Returns:

```
{
  "status": "processing",
  "task_id": "...",
  "message": "Analysis started"
}
```

---

### Task Status

```
GET /task/{task_id}
```

---

### Analysis History

```
GET /history
```

---

## 📈 Example Output Sections

* Executive Summary
* Key Financial Highlights
* Performance Analysis
* Investment Insights
* Risk Factors
* Strategic Observations
* Final Recommendation

---

## ✅ Assignment Requirements Coverage

| Requirement                | Status        |
| -------------------------- | ------------- |
| Fix deterministic bugs     | ✅ Completed   |
| Improve prompts            | ✅ Completed   |
| Working system             | ✅ Completed   |
| README documentation       | ✅ Completed   |
| Queue worker bonus         | ✅ Implemented |
| Database integration bonus | ✅ Implemented |

---

## 👤 Author

Vinod
B.Tech Computer Science Engineering (2026)

---

## 📜 License

Created for AI Internship Debug Challenge.

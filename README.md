# 📊 Financial Document Analyzer — CrewAI Debug Challenge

## 🧠 Overview

This project is an AI-powered financial document analysis system built using **CrewAI**, designed to process uploaded financial reports and generate structured investment insights using autonomous AI agents.

The repository was provided as part of an AI Internship Debug Challenge and initially contained multiple deterministic bugs, tool misconfigurations, and inefficient prompts that prevented reliable execution.

All issues were systematically identified, fixed, and the system was upgraded with **production-grade enhancements**, including:

* Robust LLM orchestration
* Optimized prompt engineering
* Asynchronous background processing
* Persistent database storage
* Structured JSON outputs
* Error-tolerant parsing pipeline

The final system is stable, scalable, and suitable for real-world financial document analysis workflows.

---

# 🚀 Key Features

* 📄 Upload financial PDF documents for analysis
* 🤖 AI-driven financial insights using CrewAI agents
* 📊 Structured financial, investment, and risk analysis output (JSON)
* ⚡ Asynchronous processing using Celery & Redis (**Queue Worker Bonus**)
* 💾 Persistent storage with SQLite database (**Database Bonus**)
* 🔍 Task status tracking API
* 📜 Analysis history retrieval endpoint
* 🧩 Robust JSON parsing with fallback recovery
* 🧠 Prompt-optimized deterministic financial reasoning
* 📈 Financial page relevance scoring for improved extraction accuracy

---

# 🐛 Bugs Identified and Fixes

## 1️⃣ Undefined LLM Initialization

### Original Code

```python
llm = llm
```

### Issue

* Undefined variable caused immediate runtime crash.

### Fix

Proper initialization using CrewAI LLM configuration:

```python
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)
```

---

## 2️⃣ Incorrect Agent Parameter (`tool` instead of `tools`)

### Original Code

```python
tool=[FinancialDocumentTool.read_data_tool]
```

### Issue

CrewAI expects `tools` (plural), preventing agent tool access.

### Fix

```python
tools=[FinancialDocumentTool.read_data_tool]
```

---

## 3️⃣ Broken Tool Implementation

### Original Problems

* Tool defined as async (incompatible)
* Missing `@tool` decorator
* Undefined `Pdf` class
* Incorrect imports
* No token control → frequent rate limit failures

### Fixes

* Converted tool to synchronous function
* Added CrewAI `@tool` decorator
* Replaced loader with `PyPDFLoader`
* Implemented financial page scoring
* Added token-safe truncation

---

## 4️⃣ Crew Input Not Passing File Path

### Original Code

```python
result = financial_crew.kickoff({'query': query})
```

### Issue

Agents could not read uploaded documents.

### Fix

```python
result = financial_crew.kickoff({
    "query": query,
    "file_path": file_path
})
```

---

## 5️⃣ Inefficient Prompt Engineering

### Original Issues

* Prompts encouraged hallucination:

  * “Make up investment advice”
  * “Just assume everything”
* No constraints
* No structure
* No reasoning workflow

### Fixes

Implemented:

* Evidence-based reasoning rules
* Structured output schema
* Anti-hallucination constraints
* Financial analysis workflow steps
* Missing-data handling instructions

Result: significantly improved determinism and reliability.

---

## 6️⃣ Missing Persistence Layer

### Original System

* No storage of analysis results.

### Fix

* Implemented SQLite database using SQLAlchemy
* Stored filename, query, result, timestamps
* Added `/history` endpoint

---

## 7️⃣ Blocking API Execution

### Original System

* Crew execution ran synchronously inside API.
* Not scalable for multiple users.

### Fix (**Bonus Feature**)

Implemented:

* Celery queue worker
* Redis broker
* Background task processing
* Task status tracking

---

## 8️⃣ Circular Import Issues

### Issue

Worker and API modules importing each other.

### Fix

Introduced orchestration layer:

```
crew_runner.py
```

This separated execution logic cleanly.

---

## 9️⃣ JSON Serialization & Parsing Failures

### Issues

* LLM outputs returned as strings
* Non-JSON-serializable objects (sets)
* Truncated responses
* Parsing crashes

### Fixes

* Implemented safe JSON extraction
* Recursive set-to-list conversion
* Fallback parsing using `ast.literal_eval`
* Output validation before database storage

---

# 🧠 Prompt Engineering Improvements

Enhancements include:

* Structured financial reasoning workflow
* Explicit anti-hallucination rules
* Output schema enforcement
* Missing data acknowledgement
* Concise financial summarization rules
* Professional analyst tone guidance

These improvements significantly increased:

* Accuracy
* Stability
* Determinism
* Output quality

---

# 🏗️ System Architecture

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
Groq LLM
   ↓
SQLite Database
```

---

# ⚡ Queue Worker Implementation (Bonus)

Asynchronous execution implemented using:

* **Celery** — distributed task queue
* **Redis** — broker and result backend

Benefits:

* Non-blocking API responses
* Concurrent processing support
* Scalable architecture

---

# 💾 Database Integration (Bonus)

Database stores:

* Filename
* User query
* AI analysis result
* Timestamp

Provides persistent storage and retrieval via API.

---

# 📂 Project Structure

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

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <repo-link>
cd financial-document-analyzer
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_api_key
```

---

# 🔴 Run Redis

Using Docker:

```bash
docker run -d -p 6379:6379 redis
```

---

# ▶️ Start Worker

### Windows

```bash
celery -A worker worker --loglevel=info --pool=solo
```

### Linux / Mac

```bash
celery -A worker worker --loglevel=info
```

---

# ▶️ Start API Server

```bash
uvicorn main:app --reload
```

---

# 📡 API Endpoints

## Health Check

```
GET /
```

---

## Analyze Document

```
POST /analyze
```

Returns:

```json
{
  "status": "processing",
  "task_id": "...",
  "message": "Analysis started"
}
```

---

## Task Status

```
GET /task/{task_id}
```

---

## Analysis History

```
GET /history
```

---

# 📊 Example JSON Output Structure

```json
{
  "verification": {},
  "financial_analysis": {},
  "investment_insights": {},
  "risk_assessment": {}
}
```

---

# ✅ Assignment Requirements Coverage

| Requirement                | Status        |
| -------------------------- | ------------- |
| Fix deterministic bugs     | ✅ Completed   |
| Improve prompts            | ✅ Completed   |
| Working system             | ✅ Completed   |
| README documentation       | ✅ Completed   |
| Queue worker bonus         | ✅ Implemented |
| Database integration bonus | ✅ Implemented |

---

# 🧪 Technical Decisions

Key design improvements include:

* Financial page relevance scoring using keywords and numeric density
* Token-safe extraction pipeline to avoid rate limits
* Reduced agent complexity for stability
* Structured JSON response enforcement
* Robust parsing with fallback recovery
* Asynchronous task orchestration

These decisions improved reliability and scalability significantly.

---

# 📈 Scalability Considerations

The architecture supports:

* Concurrent user requests
* Background processing
* Horizontal worker scaling
* Persistent storage
* Modular agent extension

This design can be extended to enterprise-level document analysis systems.

---

# 👤 Author

**Vinod**
B.Tech Computer Science Engineering (2026)

---

# 📜 License

Created for AI Internship Debug Challenge.

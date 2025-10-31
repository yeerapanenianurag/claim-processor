# Claim Processor

> A complete AI-powered claim document processing system built with **LangGraph**, **Gemini API** and **Python**, capable of extracting, structuring, and validating claim data from unstructured PDFs like bills and discharge summaries.

## 🚀 Overview

The **Claim Processor** project automates claim document handling in healthcare — transforming unstructured PDFs (bills, discharge summaries, etc.) into **structured, validated claim data**.

This project showcases:
- **LangGraph** for building agent-based workflows.  
- **Gemini API** for structured data extraction.  
- **FastAPI** for backend orchestration.  
- **Cursor AI** and **ChatGPT** for debugging, optimization, and automation.

---

## ⚙️ Features

✅ Classifies uploaded PDFs into *bill*, *discharge*, or *other*  
✅ Extracts structured claim data using **Gemini API**  
✅ Validates claim data for missing fields, logical errors, and anomalies  
✅ Modular, scalable, and easy to extend  
✅ Dockerized for easy deployment  

---

## 🧩 Architecture Overview
# 🧠 Claim Processor — Intelligent Healthcare Claim Automation

> A complete AI-powered claim document processing system built with **LangGraph**, **Gemini API**, **FastAPI**, and **Python**, capable of extracting, structuring, and validating claim data from unstructured PDFs like bills and discharge summaries.

---

## 🚀 Overview

The **Claim Processor** project automates claim document handling in healthcare — transforming unstructured PDFs (bills, discharge summaries, etc.) into **structured, validated claim data**.

This project showcases:
- **LangGraph** for building agent-based workflows.  
- **Gemini API** for structured data extraction.  
- **FastAPI** for backend orchestration.  
- **Cursor AI** and **ChatGPT** for debugging, optimization, and automation.

---

## ⚙️ Features

✅ Classifies uploaded PDFs into *bill*, *discharge*, or *other*  
✅ Extracts structured claim data using **Gemini API**  
✅ Validates claim data for missing fields, logical errors, and anomalies  
✅ Modular, scalable, and easy to extend  
✅ Dockerized for easy deployment  

---

## 🧩 Architecture Overview
+---------------------+
|  PDF Upload (API)   |
+---------------------+
           |
           ▼
+---------------------+
|  Classifier Agent   | → Identifies doc type (bill/discharge)
+---------------------+
           |
           ▼
+---------------------+
|  Bill Agent         | → Extracts structured data from bills
+---------------------+
           |
           ▼
+---------------------+
|  Discharge Agent    | → Extracts structured data from discharge summaries
+---------------------+
           |
           ▼
+---------------------+
|  Validation Agent   | → Validates claim completeness and consistency
+---------------------+
           |
           ▼
+---------------------+
|  Final Decision     | → Approve / Reject / Manual Review
+---------------------+






📁 Project Structure

'''   Claim Processor/
│
├── app/
│ ├── agents/
│ │ ├── bill_agent.py → Extracts claim data from bill PDFs
│ │ ├── discharge_agent.py → Extracts claim data from discharge PDFs
│ │ ├── validation_agent.py → Validates structured claim data
│ │ └── classifier_agent.py → Classifies input PDFs
│ │
│ ├── ai/
│ │ └── llm_client.py → Integrates Gemini API for extraction
│ │
│ ├── state/
│ │ └── claim_state_old.py → Defines ClaimState class for state tracking
│ │
│ ├── agent_orchestrator.py → Orchestrates agent execution using LangGraph
│ └── init.py
│
├── main.py → Entry point (FastAPI app)
├── Dockerfile → Containerization setup
├── .dockerignore → Excluded files for Docker
├── requirements.txt → Dependencies
├── .env → API keys and environment variables '''









---

## 🧰 Tools & Libraries Used

| Tool | Purpose |
|------|----------|
| **LangGraph** | Agent orchestration and workflow logic |
| **Gemini API (Google Generative AI)** | Extracting structured claim data |
| **FastAPI + Uvicorn** | Backend and server hosting |
| **Pydantic** | Defining clean, validated data models |
| **ChatGPT** | Debugging and architectural planning |
| **Cursor AI** | Quick fixes and IDE-level debugging |
| **Docker** | Packaging and deploying the application |

---

## 🧩 File Roles Explained

- **`classifier_agent.py`** → Classifies PDF into `bill`, `discharge`, or `other`.  
- **`bill_agent.py`** → Extracts structured data from the bill using Gemini API.  
- **`discharge_agent.py`** → Extracts structured data from discharge summaries.  
- **`validation_agent.py`** → Performs consistency checks and validation.  
- **`claim_state_old.py`** → Maintains a unified `ClaimState` object for all agents.  
- **`agent_orchestrator.py`** → Defines LangGraph flow and execution logic.  
- **`llm_client.py`** → Contains the `extract_structured_claim_data()` function using Gemini API.  
- **`main.py`** → Entry point to run the backend API.  

---

## 🧠 Major Errors Faced & Fixes

### ❌ 1. `'dict' object has no attribute 'structured_claim'`
**Issue:** State handled as a Python dict instead of an object.  
**Fix:** Replaced dict with a **Pydantic model** (`ClaimState`) to ensure attribute-based access.


### ❌ 2. `'ClaimState' object has no attribute get'`
**Issue:** Validation agent expected dictionary-like `.get()` access.  
**Fix:** Modified access to `state.structured_claim.get(...)`.


### ❌ 3. `'ClaimState' object is not subscriptable'`
**Issue:** Mixed object and dict-style access.  
**Fix:** Used consistent Pydantic attribute access across agents.

### ❌ 4. `ModuleNotFoundError: No module named 'app.state.claim_state'`
**Issue:** File renamed to `claim_state_old.py`.  
**Fix:** Updated import path everywhere accordingly.




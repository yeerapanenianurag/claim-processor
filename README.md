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
| **Stage**               | **Description**                                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 🟩 **PDF Upload (API)** | The process starts when users upload claim-related PDFs (bills, discharge summaries, etc.) through the FastAPI endpoint.                    |
| 🔽                      |                                                                                                                                             |
| 🧠 **Classifier Agent** | Analyzes the PDF text and identifies the type of document (Bill / Discharge / Other).                                                       |
| 🔽                      |                                                                                                                                             |
| 💰 **Bill Agent**       | Extracts structured data such as total amount, hospital name, patient details, and claim amount from bill PDFs using the Gemini API.        |
| 🔽                      |                                                                                                                                             |
| 🏥 **Discharge Agent**  | Extracts medical and discharge summary data like diagnosis, treatment details, admission/discharge dates, etc.                              |
| 🔽                      |                                                                                                                                             |
| ✅ **Validation Agent**  | Validates extracted data for completeness, logical consistency, date correctness, and claim amount reasonability.                           |
| 🔽                      |                                                                                                                                             |
| ⚖️ **Final Decision**   | Generates a structured output — marking the claim as **Approved**, **Rejected**, or **Requires Manual Review** based on validation results. |







📁 Project Structure

| **Path / File**             | **Description**                                                |
| --------------------------- | -------------------------------------------------------------- |
| **Claim Processor/**        | Root project directory                                         |
| ├── **app/**                | Main application folder                                        |
| ├── **app/agents/**         | Contains all intelligent processing agents                     |
| │ ├── `bill_agent.py`       | Extracts structured claim data from bill PDFs                  |
| │ ├── `discharge_agent.py`  | Extracts structured data from discharge summaries              |
| │ ├── `validation_agent.py` | Validates structured claim data for accuracy and completeness  |
| │ └── `classifier_agent.py` | Classifies uploaded PDFs as bill/discharge/other               |
| ├── **app/ai/**             | AI integration layer                                           |
| │ └── `llm_client.py`       | Integrates Gemini API for claim data extraction                |
| ├── **app/state/**          | Handles state management                                       |
| │ └── `claim_state_old.py`  | Defines the `ClaimState` class used to track workflow progress |
| ├── `agent_orchestrator.py` | Orchestrates agent execution using LangGraph                   |
| ├── `__init__.py`           | Marks `app/` as a Python package                               |
| **main.py**                 | FastAPI entry point for starting the backend server            |
| **Dockerfile**              | Defines containerization setup for the project                 |
| **.dockerignore**           | Lists files excluded during Docker image build                 |
| **requirements.txt**        | Lists all project dependencies                                 |
| **.env**                    | Stores environment variables like API keys (Gemini, etc.)      |









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




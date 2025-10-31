from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import tempfile
import asyncio

# Internal imports

from app.utils.pdf_loader import extract_text_from_pdfs
from app.agent_orchestrator import build_claim_graph, ClaimState
from app.models.claim_schema import ClaimSchema
from app.agents.validation_agent import ValidationAgent
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import tempfile

from app.utils.pdf_loader import extract_text_from_pdfs
from app.agent_orchestrator import build_claim_graph, ClaimState
from app.agents.validation_agent import ValidationAgent



# Load environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="Claim Processor API", version="2.0")


# Health check
@app.get("/")
async def root():
    return {"message": "Claim Processor API is  running "}


# Process multiple PDFs
@app.post("/process-claims")
async def process_claims(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    try:
        # Step 1: Save all PDFs 
        temp_items = []
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                temp_items.append({"path": tmp.name, "filename": file.filename})

        # Step 2: Extract text
        pdf_texts = await extract_text_from_pdfs(temp_items) \
            if callable(getattr(extract_text_from_pdfs, "__await__", None)) \
            else extract_text_from_pdfs(temp_items)

        # Step 3: Build the LangGraph 
        graph = build_claim_graph()

        # Step 4: Initialize 
        initial_state = ClaimState(raw_pdfs=pdf_texts)

        # Step 5: Execute the claim 
        final_state = await graph.ainvoke(initial_state)

        # Force-convert any dict (including nested ones) into ClaimState
        if not isinstance(final_state, ClaimState):
            final_state = ClaimState(**final_state) if isinstance(final_state, dict) else ClaimState()

        # Ensure structured_claim exists
        if not getattr(final_state, "structured_claim", None):
            final_state.structured_claim = {}

        #Validate using the ClaimState object (not a dict)
        validation_result = ValidationAgent.validate(final_state)

        # Step 7: Return final result 
        extracted_debug = [
            {"filename": item.get("filename"), "text_len": len(item.get("content", "") or "")}
            for item in pdf_texts
            if isinstance(pdf_texts, list)
        ]
        classified_debug = (
            final_state.get("classified_docs") if hasattr(final_state, "get") else getattr(final_state, "classified_docs", [])
        )

        return {
            "extracted": extracted_debug,
            "classified_docs": classified_debug,
            "structured_claim": final_state.structured_claim,
            "validation": validation_result,
            "final_decision": getattr(final_state, "decision", None),
            "reasons": getattr(final_state, "reasons", None),
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing claim: {str(e)}")


#Validate a JSON claim directly
@app.post("/validate-claim/")
async def validate_claim(claim: ClaimSchema):
    try:
        result = ValidationAgent.validate(claim.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#Check if Gemini API key loaded
@app.get("/check-api-key")
async def check_api_key():
    return {"GEMINI_API_KEY_found": bool(GEMINI_API_KEY)}

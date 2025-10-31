from app.models.claim_state import ClaimState
from app.ai.llm_client import classify_document


def classifier_agent(state: ClaimState):
    """
    Classifies PDFs into 'bill', 'discharge', or 'other' based on text.
    """
    classified_docs = []

    raw_docs = state.raw_pdfs if hasattr(state, "raw_pdfs") else []

    for pdf_data in raw_docs:

        if isinstance(pdf_data, dict):
            text = pdf_data.get("content", "")

            if isinstance(text, dict) and "data" in text:
                text = text.get("data", "")
            filename = pdf_data.get("filename", "unknown.pdf")
        else:
            text = str(pdf_data)
            filename = "unknown.pdf"


        doc_type = classify_document(text, filename)

        classified_docs.append({
            "filename": filename,
            "type": doc_type,
            "content": text
        })


    if hasattr(state, "get"):
        state["classified_docs"] = classified_docs
    else:
        state.classified_docs = classified_docs
    return state

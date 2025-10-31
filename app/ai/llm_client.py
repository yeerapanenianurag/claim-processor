import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel("gemini-1.5-flash")

def ensure_string(input_data):
    """
    Converts dicts/lists to string safely so Gemini never breaks.
    """
    if isinstance(input_data, dict):
        return str(input_data)
    elif isinstance(input_data, list):
        return " ".join(map(str, input_data))
    elif input_data is None:
        return ""
    return str(input_data)

def extract_structured_claim_data(pdf_text, doc_type="Claim"):
    """
    Extract structured claim information using Gemini model.
    Accepts text and optional document type ('Bill', 'Discharge', etc.).
    """
    try:
        pdf_text = ensure_string(pdf_text)

        prompt = f"""
        You are a medical claims processing AI.
        Extract structured {doc_type} information from this text and return valid JSON format only.

        Text:
        {pdf_text}
        """

        response = model.generate_content(prompt)
        return {"data": response.text}

    except Exception as e:
        return {"error": f"Gemini call failed: {str(e)}"}


def classify_document(text: str, filename: str | None = None) -> str:
    """
    Classify a document as one of: bill, discharge, other.
    Uses both filename hints and content. Falls back to heuristics on failure.
    """
    try:
        fname = (filename or "").lower()
        # Quick filename hints before LLM
        if any(k in fname for k in ["bill", "invoice"]):
            return "bill"
        if any(k in fname for k in ["discharge", "summary"]):
            return "discharge"

        safe_text = ensure_string(text)
        prompt = (
            "Classify the following medical claim document strictly as one of the tokens: "
            "bill | discharge | other.\n"
            "Answer with ONLY the single token.\n\n"
            f"Filename: {filename or 'unknown'}\n"
            f"Content snippet: {safe_text[:2000]}"
        )
        resp = model.generate_content(prompt)
        label = (resp.text or "").strip().lower()
        if "bill" in label:
            return "bill"
        if "discharge" in label:
            return "discharge"
        return "other"
    except Exception:
        t = (text or "").lower()
        f = (filename or "").lower()
        if any(k in t or k in f for k in ["bill", "invoice"]):
            return "bill"
        if any(k in t or k in f for k in ["discharge", "summary", "discharge summary"]):
            return "discharge"
        return "other"


def extract_plain_text_with_llm(raw_text: str, filename: str | None = None) -> str:
    """
    Clean and normalize extracted PDF text using Gemini to improve readability.
    Input is raw text (from PDF parser); output should be plain UTF-8 text only.
    """
    try:
        safe_text = ensure_string(raw_text)
        prompt = (
            "You are a text normalization assistant.\n"
            "Given OCR or PDF-extracted text, return a cleaned version as plain text:\n"
            "- Fix broken newlines and spacing.\n"
            "- Keep semantic content, remove obvious duplicated headers/footers.\n"
            "- Do not add summaries or commentary.\n"
            "Return ONLY the cleaned text.\n\n"
            f"Filename: {filename or 'unknown'}\n"
            f"Raw text snippet (may be truncated):\n{safe_text[:6000]}"
        )
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception:
        return raw_text or ""
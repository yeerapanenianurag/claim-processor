import os
from typing import List, Union
from app.ai.llm_client import extract_plain_text_with_llm

def _extract_text_with_pypdf2(path: str) -> str:
    try:
        import PyPDF2
        text_parts = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in getattr(reader, "pages", []):
                try:
                    text_parts.append(page.extract_text() or "")
                except Exception:
                    continue
        return "\n".join(filter(None, text_parts))
    except Exception:
        return ""

def extract_text_from_pdfs(items: List[Union[str, dict]]):
    """
    Accepts either a list of file paths or dicts {"path": str, "filename": str}.
    Returns list of {"filename": str, "content": str} with extracted text.
    """
    pdf_data = []
    for item in items:
        if isinstance(item, dict):
            path = item.get("path")
            filename = item.get("filename") or os.path.basename(path or "")
        else:
            path = item
            filename = os.path.basename(path or "")

        text_raw = _extract_text_with_pypdf2(path) if path else ""
        text = extract_plain_text_with_llm(text_raw, filename)
        pdf_data.append({
            "filename": filename,
            "content": text
        })
    return pdf_data

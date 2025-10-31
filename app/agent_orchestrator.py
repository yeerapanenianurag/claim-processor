from langgraph.graph import StateGraph, END
from app.agents.bill_agent import BillAgent
from app.agents.discharge_agent import DischargeAgent
from app.agents.validation_agent import ValidationAgent
from app.state.claim_state_old import ClaimState
from app.ai.llm_client import classify_document

def validate_agent(state: ClaimState):
    """
    Wrapper to validate structured claim data inside LangGraph flow.
    """
    try:
        result = ValidationAgent.validate(state)
        # Store decision/reasons safely on dict or object state
        if hasattr(state, "get"):
            state["decision"] = result.get("status")
            state["reasons"] = result.get("message")
        else:
            state.decision = result.get("status")
            state.reasons = result.get("message")
        return state
    except Exception as e:
        if hasattr(state, "get"):
            state["decision"] = "failed"
            state["reasons"] = str(e)
        else:
            state.decision = "failed"
            state.reasons = str(e)
        return state


def classifier_agent(state: ClaimState):
    """
    Simple classifier agent placeholder.
    """
    classified_docs = []
    # Support both dict-like and attribute-style states
    raw_docs = (
        state.get("raw_pdfs", []) if hasattr(state, "get") else getattr(state, "raw_pdfs", [])
    )
    for pdf_data in raw_docs:
        # Ensure we are working with the extracted text, not the whole dict
        if isinstance(pdf_data, dict):
            text = pdf_data.get("content", "")
            filename = pdf_data.get("filename", "unknown.pdf")
        else:
            text = str(pdf_data)
            filename = "unknown.pdf"

        # LLM-backed classification with heuristic fallback handled inside
        doc_type = classify_document(text, filename)

        classified_docs.append({
            "filename": filename,
            "type": doc_type,
            "content": text
        })

    # Store results back into state (prefer dict-style when available)
    if hasattr(state, "get"):
        state["classified_docs"] = classified_docs
    else:
        state.classified_docs = classified_docs
    return state
def merge_agent(state: ClaimState):
    """
    Merge data from per-document extractions into a unified structured claim.
    Expects state.structured_claim to potentially contain keys 'bill' and 'discharge'.
    """
    # Access structured_claim safely
    if hasattr(state, "get"):
        structured = state.get("structured_claim") or {}
    else:
        structured = getattr(state, "structured_claim", {}) or {}

    bill_map = structured.get("bill", {}) if isinstance(structured, dict) else {}
    discharge_map = structured.get("discharge", {}) if isinstance(structured, dict) else {}

    # Helper to parse possible JSON strings nested under {"data": "..."}
    def extract_dict(candidate):
        import json
        if not candidate:
            return {}
        if isinstance(candidate, dict) and "data" in candidate and isinstance(candidate["data"], str):
            try:
                return json.loads(candidate["data"])  # best effort
            except Exception:
                return {}
        if isinstance(candidate, dict):
            return candidate
        return {}

    merged = {}

    # Aggregate fields from all bill docs
    for _, resp in (bill_map.items() if isinstance(bill_map, dict) else []):
        d = extract_dict(resp)
        merged.setdefault("hospital_name", d.get("hospital_name"))
        merged.setdefault("patient_name", d.get("patient_name"))
        merged.setdefault("claim_amount", d.get("total_amount") or d.get("claim_amount"))
        merged.setdefault("insurance_provider", d.get("insurer_name") or d.get("insurance_provider"))
        merged.setdefault("policy_number", d.get("policy_number"))

    # Discharge info typically has strong patient/dates/diagnosis
    for _, resp in (discharge_map.items() if isinstance(discharge_map, dict) else []):
        d = extract_dict(resp)
        if d.get("patient_name"):
            merged["patient_name"] = d.get("patient_name")
        if d.get("hospital_name"):
            merged["hospital_name"] = d.get("hospital_name")
        if d.get("admission_date"):
            merged["admission_date"] = d.get("admission_date")
        if d.get("discharge_date"):
            merged["discharge_date"] = d.get("discharge_date")
        if d.get("diagnosis"):
            merged["diagnosis"] = d.get("diagnosis")

        # Possible insurer/policy present here as well
        if d.get("insurer_name") or d.get("insurance_provider"):
            merged["insurance_provider"] = d.get("insurer_name") or d.get("insurance_provider")
        if d.get("policy_number"):
            merged["policy_number"] = d.get("policy_number")

    # Ensure required keys exist (even if None) so validator sees them
    for key in [
        "claim_id", "patient_name", "hospital_name", "admission_date",
        "discharge_date", "claim_amount", "diagnosis", "insurer_name",
        "policy_number"
    ]:
        merged.setdefault(key, None)

    # Write back to state
    if hasattr(state, "get"):
        base = state.get("structured_claim") or {}
        base["merged"] = merged
        base.update(merged)  # flatten top-level for validator
        state["structured_claim"] = base
    else:
        base = getattr(state, "structured_claim", {}) or {}
        base["merged"] = merged
        base.update(merged)
        state.structured_claim = base

    return state


def build_claim_graph():
    graph = StateGraph(ClaimState)

    # Define all nodes (steps)
    graph.add_node("classify", classifier_agent)
    graph.add_node("bill", BillAgent.process)
    graph.add_node("discharge", DischargeAgent.process)
    graph.add_node("merge", merge_agent)
    graph.add_node("validate", validate_agent)

    # Define the execution flow
    graph.add_edge("classify", "bill")
    graph.add_edge("bill", "discharge")
    graph.add_edge("discharge", "merge")
    graph.add_edge("merge", "validate")
    graph.add_edge("validate", END)

    # ✅ Define where the graph should START
    graph.set_entry_point("classify")

    # Compile the final executable graph
    return graph.compile()

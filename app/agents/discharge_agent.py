from app.ai.llm_client import extract_structured_claim_data

class DischargeAgent:
    @staticmethod
    def process(state):
        classified_docs = state.get("classified_docs", []) if hasattr(state, "get") else getattr(state, "classified_docs", [])
        discharge_docs = []
        for doc in classified_docs:
            doc_type = doc["type"] if isinstance(doc, dict) else getattr(doc, "type", None)
            if doc_type == "discharge":
                discharge_docs.append(doc)

        structured_discharge_data = {}
        for discharge in discharge_docs:
            try:
                discharge_content = discharge["content"] if isinstance(discharge, dict) else getattr(discharge, "content", "")
                filename = discharge["filename"] if isinstance(discharge, dict) else getattr(discharge, "filename", "unknown")

                response = extract_structured_claim_data(discharge_content, "Discharge")
                structured_discharge_data[filename] = response
            except Exception as e:
                structured_discharge_data[filename] = {"error": str(e)}

        if hasattr(state, "get"):
            structured_claim = state.get("structured_claim")
            if structured_claim is None:
                state["structured_claim"] = {}
            state["structured_claim"]["discharge"] = structured_discharge_data
        else:
            if getattr(state, "structured_claim", None) is None:
                state.structured_claim = {}
            state.structured_claim["discharge"] = structured_discharge_data
        return state

from app.ai.llm_client import extract_structured_claim_data

class BillAgent:
    @staticmethod
    def process(state):
        classified_docs = state.get("classified_docs", []) if hasattr(state, "get") else getattr(state, "classified_docs", [])
        bill_docs = []
        for doc in classified_docs:
            doc_type = doc["type"] if isinstance(doc, dict) else getattr(doc, "type", None)
            if doc_type == "bill":
                bill_docs.append(doc)

        structured_bill_data = {}
        for bill in bill_docs:
            try:
                bill_content = bill["content"] if isinstance(bill, dict) else getattr(bill, "content", "")
                filename = bill["filename"] if isinstance(bill, dict) else getattr(bill, "filename", "unknown")

                response = extract_structured_claim_data(bill_content, "Bill")
                structured_bill_data[filename] = response
            except Exception as e:
                structured_bill_data[filename] = {"error": str(e)}

        if hasattr(state, "get"):
            structured_claim = state.get("structured_claim")
            if structured_claim is None:
                state["structured_claim"] = {}
            state["structured_claim"]["bill"] = structured_bill_data
        else:
            if getattr(state, "structured_claim", None) is None:
                state.structured_claim = {}
            state.structured_claim["bill"] = structured_bill_data

        return state

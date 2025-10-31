from datetime import datetime
from app.models.claim_state import ClaimState

class ValidationAgent:
    @staticmethod
    def validate(state: ClaimState):
        errors = []
        # Access structured_claim safely for dict or object state
        if hasattr(state, "get"):
            claim_data = state.get("structured_claim") or {}
        else:
            claim_data = getattr(state, "structured_claim", {}) or {}

        # Basic presence checks 
        required_fields = [
            "claim_id", "patient_name", "hospital_name",
            "admission_date", "discharge_date",
            "claim_amount", "diagnosis",
            "insurer_name", "policy_number"
        ]
        for field in required_fields:
            if field not in claim_data or not claim_data[field]:
                errors.append(f"Missing or empty field: {field}")

        # Date validation 
        try:
            admission = datetime.strptime(claim_data["admission_date"], "%Y-%m-%d")
            discharge = datetime.strptime(claim_data["discharge_date"], "%Y-%m-%d")
            if discharge < admission:
                errors.append("Discharge date cannot be before admission date.")
        except Exception:
            errors.append("Invalid date format. Use YYYY-MM-DD.")

        # Claim amount 
        if claim_data.get("claim_amount", 0) > 500000:
            errors.append("Claim amount unusually high. Manual review recommended.")

        if not errors:
            if hasattr(state, "get"):
                state["decision"] = "approved"
                state["reasons"] = "All validations passed."
            else:
                state.decision = "approved"
                state.reasons = "All validations passed."
            return {
                "status": "success",
                "message": "Claim data validated successfully.",
                "validated_data": claim_data
            }
        else:
            if hasattr(state, "get"):
                state["decision"] = "rejected"
                state["reasons"] = ", ".join(errors)
            else:
                state.decision = "rejected"
                state.reasons = ", ".join(errors)
            return {
                "status": "failed",
                "message": "Validation errors found.",
                "errors": errors
            }

from pydantic import BaseModel, Field

class ClaimState(BaseModel):
    raw_pdfs: list
    classified_docs: list = Field(default_factory=list)
    structured_claim: dict = Field(default_factory=dict)
    decision: str | None = None
    reasons: str | None = None

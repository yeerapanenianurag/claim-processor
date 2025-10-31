from pydantic import BaseModel
from typing import Optional, List

class ClaimSchema(BaseModel):
    patient_name: str
    hospital_name: str
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None
    total_bill_amount: Optional[float] = None
    insurance_provider: Optional[str] = None
    policy_number: Optional[str] = None
    diagnosis: Optional[str] = None
    claim_items: Optional[List[str]] = None
    claim_amount: Optional[float] = None
    remarks: Optional[str] = None

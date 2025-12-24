from pydantic import BaseModel, Field
from typing import List, Optional

class Medication(BaseModel):
    name: str = Field(description="Name of the drug")
    dosage: str = Field(description="Dosage amount, e.g., '500mg'")
    frequency: str = Field(description="Frequency, e.g., 'twice daily'")

class PrescriptionData(BaseModel):
    patient_name: str = Field(description="Full name of the patient")
    doctor_name: str = Field(description="Name of the prescribing doctor")
    diagnosis: Optional[str] = Field(description="Diagnosis if present")
    medications: List[Medication]
    is_handwritten: bool = Field(description="True if the prescription is handwritten")
    

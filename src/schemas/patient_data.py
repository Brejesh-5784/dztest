
from pydantic import BaseModel, Field
from typing import Optional, List

class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str

class PatientData(BaseModel):
    patient_id: Optional[str] = Field(None, description="The unique ID of the patient")
    patient_name: Optional[str] = Field(None, description="Name of the patient")
    diagnosis_icd10: Optional[str] = Field(None, description="ICD-10 code found in document")
    medications: List[Medication] = []
    physician_signature_present: bool = Field(False, description="Is the doctor's signature detected?")
    confidence_score: float = Field(0.0, description="Confidence of the extraction (0-1)")

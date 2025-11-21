"""Tools for accessing patient information."""

from agents import function_tool
from pydantic import BaseModel, Field


class Allergy(BaseModel):
    """Patient allergy information."""

    allergen: str = Field(description="Substance patient is allergic to")
    severity: str = Field(description="Severity level (mild, moderate, severe)")
    reaction: str = Field(description="Type of allergic reaction")


class MedicalHistory(BaseModel):
    """Patient medical history entry."""

    condition: str = Field(description="Medical condition")
    diagnosis_date: str = Field(description="Date of diagnosis")
    status: str = Field(description="Current status (active, resolved, etc.)")


class PatientInfo(BaseModel):
    """Patient demographic and basic information."""

    patient_id: str = Field(description="Unique patient identifier")
    name: str = Field(description="Patient name")
    age: int = Field(description="Patient age")
    weight_kg: float = Field(description="Patient weight in kilograms")
    current_medications: list[str] = Field(description="List of current medications")
    allergies: list[Allergy] = Field(description="List of known allergies")
    medical_history: list[MedicalHistory] = Field(description="Medical history entries")


# Mock patient database
_MOCK_PATIENTS: dict[str, PatientInfo] = {
    "P001": PatientInfo(
        patient_id="P001",
        name="John Doe",
        age=65,
        weight_kg=75.0,
        current_medications=["Warfarin", "Metformin", "Amiodarone"],
        allergies=[
            Allergy(allergen="Penicillin", severity="severe", reaction="Anaphylaxis")
        ],
        medical_history=[
            MedicalHistory(
                condition="Atrial Fibrillation with RVR",
                diagnosis_date="2024-01-15",
                status="active",
            ),
            MedicalHistory(
                condition="Type 2 Diabetes",
                diagnosis_date="2023-06-20",
                status="active",
            ),
            MedicalHistory(
                condition="Recent arrhythmia episode - Amiodarone initiated",
                diagnosis_date="2024-11-14",
                status="active",
            ),
        ],
    ),
    "P002": PatientInfo(
        patient_id="P002",
        name="Jane Smith",
        age=45,
        weight_kg=60.0,
        current_medications=["Aspirin", "Doxorubicin", "Meropenem"],
        allergies=[
            Allergy(allergen="Latex", severity="moderate", reaction="Skin rash")
        ],
        medical_history=[
            MedicalHistory(
                condition="Breast Cancer - Stage II (on chemotherapy)",
                diagnosis_date="2024-09-01",
                status="active",
            ),
            MedicalHistory(
                condition="Febrile Neutropenia - currently on broad-spectrum antibiotics",
                diagnosis_date="2024-11-14",
                status="active",
            ),
        ],
    ),
    "P003": PatientInfo(
        patient_id="P003",
        name="Robert Johnson",
        age=78,
        weight_kg=68.0,
        current_medications=["Morphine", "Furosemide", "Midazolam"],
        allergies=[],
        medical_history=[
            MedicalHistory(
                condition="Chronic Obstructive Pulmonary Disease (COPD)",
                diagnosis_date="2020-03-15",
                status="active",
            ),
            MedicalHistory(
                condition="Heart Failure",
                diagnosis_date="2024-02-01",
                status="active",
            ),
        ],
    ),
    "P004": PatientInfo(
        patient_id="P004",
        name="Maria Garcia",
        age=58,
        weight_kg=82.0,
        current_medications=["Insulin Regular", "Metformin", "Lisinopril"],
        allergies=[
            Allergy(allergen="Sulfa drugs", severity="moderate", reaction="Rash and hives")
        ],
        medical_history=[
            MedicalHistory(
                condition="Type 1 Diabetes Mellitus",
                diagnosis_date="2005-03-10",
                status="active",
            ),
            MedicalHistory(
                condition="Hypertension",
                diagnosis_date="2018-07-15",
                status="active",
            ),
            MedicalHistory(
                condition="Diabetic Ketoacidosis - ICU admission",
                diagnosis_date="2024-11-13",
                status="recovering",
            ),
        ],
    ),
    "P005": PatientInfo(
        patient_id="P005",
        name="William Chen",
        age=72,
        weight_kg=70.0,
        current_medications=["Warfarin", "Atorvastatin", "Amlodipine"],
        allergies=[],
        medical_history=[
            MedicalHistory(
                condition="Deep Vein Thrombosis (DVT) - Left leg",
                diagnosis_date="2024-11-10",
                status="active",
            ),
            MedicalHistory(
                condition="Pulmonary Embolism - Small, treated",
                diagnosis_date="2024-11-11",
                status="active",
            ),
            MedicalHistory(
                condition="Hyperlipidemia",
                diagnosis_date="2020-05-20",
                status="active",
            ),
            MedicalHistory(
                condition="Hypertension",
                diagnosis_date="2019-02-14",
                status="active",
            ),
        ],
    ),
}


@function_tool
def get_patient_info(patient_id: str) -> PatientInfo:
    """
    Get patient demographic information and basic details.
    Includes allergies, medical history, current medications, and demographics.

    Args:
        patient_id: Unique patient identifier

    Returns:
        PatientInfo with demographics, allergies, medical history, and current medications
    """
    if patient_id not in _MOCK_PATIENTS:
        raise ValueError(f"Patient {patient_id} not found")
    return _MOCK_PATIENTS[patient_id]

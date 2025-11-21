"""Tools for accessing prescription information."""

from agents import function_tool
from pydantic import BaseModel, Field


class PrescriptionDetails(BaseModel):
    """Prescription information."""

    prescription_id: str = Field(description="Unique prescription identifier")
    patient_id: str = Field(description="Patient identifier")
    medication: str = Field(description="Medication name")
    dosage: float = Field(description="Prescribed dosage")
    dosage_unit: str = Field(description="Unit of measurement")
    frequency: str = Field(
        description="Frequency of administration (e.g., 'once daily', 'every 8 hours')"
    )
    route: str = Field(description="Administration route")
    start_date: str = Field(description="Prescription start date")
    end_date: str | None = Field(
        default=None, description="Prescription end date if applicable"
    )
    prescriber_id: str = Field(description="ID of prescribing physician")
    status: str = Field(
        description="Prescription status (active, completed, cancelled)"
    )
    model_config = {"extra": "forbid"}


# Mock prescription database
_MOCK_PRESCRIPTIONS: dict[tuple[str, str], PrescriptionDetails] = {
    # Patient P001 (Warfarin + Amiodarone case)
    ("Warfarin", "P001"): PrescriptionDetails(
        prescription_id="PRES-001",
        patient_id="P001",
        medication="Warfarin",
        dosage=5.0,
        dosage_unit="mg",
        frequency="once daily",
        route="oral",
        start_date="2024-11-01",
        end_date=None,
        prescriber_id="DOC-001",
        status="active",
    ),
    ("Metformin", "P001"): PrescriptionDetails(
        prescription_id="PRES-002",
        patient_id="P001",
        medication="Metformin",
        dosage=1000.0,
        dosage_unit="mg",
        frequency="twice daily",
        route="oral",
        start_date="2024-10-15",
        end_date=None,
        prescriber_id="DOC-001",
        status="active",
    ),
    ("Amiodarone", "P001"): PrescriptionDetails(
        prescription_id="PRES-005",
        patient_id="P001",
        medication="Amiodarone",
        dosage=200.0,
        dosage_unit="mg",
        frequency="once daily",
        route="oral",
        start_date="2024-11-14",
        end_date=None,
        prescriber_id="DOC-001",
        status="active",
    ),
    
    # Patient P002 (Chemotherapy + Antibiotics case)
    ("Aspirin", "P002"): PrescriptionDetails(
        prescription_id="PRES-006",
        patient_id="P002",
        medication="Aspirin",
        dosage=81.0,
        dosage_unit="mg",
        frequency="once daily",
        route="oral",
        start_date="2024-09-01",
        end_date=None,
        prescriber_id="DOC-002",
        status="active",
    ),
    ("Doxorubicin", "P002"): PrescriptionDetails(
        prescription_id="PRES-007",
        patient_id="P002",
        medication="Doxorubicin",
        dosage=60.0,
        dosage_unit="mg/m2",
        frequency="every 21 days (chemotherapy cycle)",
        route="IV",
        start_date="2024-09-15",
        end_date=None,
        prescriber_id="DOC-002",
        status="active",
    ),
    ("Meropenem", "P002"): PrescriptionDetails(
        prescription_id="PRES-008",
        patient_id="P002",
        medication="Meropenem",
        dosage=1000.0,
        dosage_unit="mg",
        frequency="every 8 hours",
        route="IV",
        start_date="2024-11-14",
        end_date=None,
        prescriber_id="DOC-002",
        status="active",
    ),
    
    # Patient P003 (ICU medications case)
    ("Morphine", "P003"): PrescriptionDetails(
        prescription_id="PRES-003",
        patient_id="P003",
        medication="Morphine",
        dosage=10.0,
        dosage_unit="mg",
        frequency="every 4 hours as needed",
        route="IV",
        start_date="2024-11-10",
        end_date=None,
        prescriber_id="DOC-003",
        status="active",
    ),
    ("Furosemide", "P003"): PrescriptionDetails(
        prescription_id="PRES-004",
        patient_id="P003",
        medication="Furosemide",
        dosage=40.0,
        dosage_unit="mg",
        frequency="twice daily",
        route="IV",
        start_date="2024-11-12",
        end_date=None,
        prescriber_id="DOC-003",
        status="active",
    ),
    ("Midazolam", "P003"): PrescriptionDetails(
        prescription_id="PRES-009",
        patient_id="P003",
        medication="Midazolam",
        dosage=2.0,
        dosage_unit="mg",
        frequency="every 6 hours as needed for agitation",
        route="IV",
        start_date="2024-11-13",
        end_date=None,
        prescriber_id="DOC-003",
        status="active",
    ),
    ("Enoxaparin", "P001"): PrescriptionDetails(
        prescription_id="PRES-010",
        patient_id="P001",
        medication="Enoxaparin",
        dosage=40.0,
        dosage_unit="mg",
        frequency="once daily at 08:00",
        route="subcutaneous",
        start_date="2024-11-12",
        end_date=None,
        prescriber_id="DOC-001",
        status="active",
    ),
    ("Enoxaparin", "P003"): PrescriptionDetails(
        prescription_id="PRES-011",
        patient_id="P003",
        medication="Enoxaparin",
        dosage=40.0,
        dosage_unit="mg",
        frequency="once daily at 08:00",
        route="subcutaneous",
        start_date="2024-11-13",
        end_date=None,
        prescriber_id="DOC-003",
        status="active",
    ),
    
    # Patient P004 (Type 1 Diabetes - DKA recovery)
    ("Insulin Regular", "P004"): PrescriptionDetails(
        prescription_id="PRES-012",
        patient_id="P004",
        medication="Insulin Regular",
        dosage=8.0,
        dosage_unit="units",
        frequency="before meals (07:30, 12:00, 18:00)",
        route="subcutaneous",
        start_date="2024-11-14",
        end_date=None,
        prescriber_id="DOC-004",
        status="active",
    ),
    ("Metformin", "P004"): PrescriptionDetails(
        prescription_id="PRES-013",
        patient_id="P004",
        medication="Metformin",
        dosage=1000.0,
        dosage_unit="mg",
        frequency="twice daily",
        route="oral",
        start_date="2024-11-14",
        end_date=None,
        prescriber_id="DOC-004",
        status="active",
    ),
    ("Lisinopril", "P004"): PrescriptionDetails(
        prescription_id="PRES-014",
        patient_id="P004",
        medication="Lisinopril",
        dosage=10.0,
        dosage_unit="mg",
        frequency="once daily",
        route="oral",
        start_date="2024-11-01",
        end_date=None,
        prescriber_id="DOC-004",
        status="active",
    ),
    
    # Patient P005 (DVT/PE - on anticoagulation)
    ("Warfarin", "P005"): PrescriptionDetails(
        prescription_id="PRES-015",
        patient_id="P005",
        medication="Warfarin",
        dosage=5.0,
        dosage_unit="mg",
        frequency="once daily at 18:00",
        route="oral",
        start_date="2024-11-11",
        end_date=None,
        prescriber_id="DOC-005",
        status="active",
    ),
    ("Atorvastatin", "P005"): PrescriptionDetails(
        prescription_id="PRES-016",
        patient_id="P005",
        medication="Atorvastatin",
        dosage=40.0,
        dosage_unit="mg",
        frequency="once daily at bedtime",
        route="oral",
        start_date="2024-10-01",
        end_date=None,
        prescriber_id="DOC-005",
        status="active",
    ),
    ("Amlodipine", "P005"): PrescriptionDetails(
        prescription_id="PRES-017",
        patient_id="P005",
        medication="Amlodipine",
        dosage=5.0,
        dosage_unit="mg",
        frequency="once daily",
        route="oral",
        start_date="2024-09-15",
        end_date=None,
        prescriber_id="DOC-005",
        status="active",
    ),
}


@function_tool
def get_prescription_details(medication: str, patient_id: str) -> PrescriptionDetails:
    """
    Get prescription details for a specific medication and patient.

    Args:
        medication: Medication name
        patient_id: Patient identifier

    Returns:
        PrescriptionDetails with full prescription information
    """
    key = (medication, patient_id)
    if key not in _MOCK_PRESCRIPTIONS:
        raise ValueError(
            f"Prescription not found for {medication} for patient {patient_id}"
        )
    return _MOCK_PRESCRIPTIONS[key]

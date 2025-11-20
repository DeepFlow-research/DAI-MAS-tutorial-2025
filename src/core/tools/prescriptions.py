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
        frequency="once daily",
        route="IV",
        start_date="2024-11-12",
        end_date=None,
        prescriber_id="DOC-003",
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

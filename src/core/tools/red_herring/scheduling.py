"""Red herring tool: Patient appointment scheduling (not needed for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class Appointment(BaseModel):
    """Patient appointment information."""

    appointment_id: str = Field(description="Appointment identifier")
    patient_id: str = Field(description="Patient identifier")
    date: str = Field(description="Appointment date")
    time: str = Field(description="Appointment time")
    provider: str = Field(description="Healthcare provider")
    department: str = Field(description="Department")
    model_config = {"extra": "forbid"}


# Mock appointments database
_MOCK_APPOINTMENTS: dict[str, list[Appointment]] = {
    "P001": [
        Appointment(
            appointment_id="APT-001",
            patient_id="P001",
            date="2024-11-25",
            time="10:00",
            provider="Dr. Sarah Chen",
            department="Cardiology",
        ),
        Appointment(
            appointment_id="APT-002",
            patient_id="P001",
            date="2024-12-05",
            time="14:30",
            provider="Dr. Michael Rodriguez",
            department="Internal Medicine",
        ),
    ],
    "P002": [
        Appointment(
            appointment_id="APT-003",
            patient_id="P002",
            date="2024-11-22",
            time="09:00",
            provider="Dr. James Park",
            department="Emergency",
        ),
    ],
    "P003": [
        Appointment(
            appointment_id="APT-004",
            patient_id="P003",
            date="2024-11-28",
            time="11:00",
            provider="Dr. Emily Watson",
            department="Critical Care",
        ),
        Appointment(
            appointment_id="APT-005",
            patient_id="P003",
            date="2024-12-10",
            time="15:00",
            provider="Dr. Sarah Chen",
            department="Cardiology",
        ),
    ],
}


@function_tool
def get_patient_appointments(patient_id: str) -> list[Appointment]:
    """
    Get upcoming patient appointments.

    NOTE: This tool is not relevant for medication administration audits.
    Audits focus on past medication administrations, not future appointments.

    Args:
        patient_id: Patient identifier

    Returns:
        List of upcoming appointments
    """
    # Return mock data if available, otherwise empty list
    return _MOCK_APPOINTMENTS.get(patient_id, [])

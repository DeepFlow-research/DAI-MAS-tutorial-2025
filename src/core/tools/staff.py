"""Tools for accessing staff and prescriber information."""

from agents import function_tool
from pydantic import BaseModel, Field


class PrescriberInfo(BaseModel):
    """Prescriber/physician information."""

    prescriber_id: str = Field(description="Unique prescriber identifier")
    name: str = Field(description="Prescriber name")
    title: str = Field(description="Professional title (e.g., 'MD', 'DO', 'NP')")
    specialization: str = Field(description="Medical specialization")
    department: str = Field(description="Department")
    license_number: str = Field(description="Medical license number")
    authorized_for_high_risk: bool = Field(
        description="Whether authorized to prescribe high-risk medications"
    )
    model_config = {"extra": "forbid"}


# Mock prescriber database
_MOCK_PRESCRIBERS: dict[str, PrescriberInfo] = {
    "DOC-001": PrescriberInfo(
        prescriber_id="DOC-001",
        name="Dr. Sarah Chen",
        title="MD",
        specialization="Cardiology",
        department="Cardiology",
        license_number="MED-12345",
        authorized_for_high_risk=True,
    ),
    "DOC-002": PrescriberInfo(
        prescriber_id="DOC-002",
        name="Dr. Michael Rodriguez",
        title="MD",
        specialization="Internal Medicine",
        department="General Medicine",
        license_number="MED-23456",
        authorized_for_high_risk=True,
    ),
    "DOC-003": PrescriberInfo(
        prescriber_id="DOC-003",
        name="Dr. Emily Watson",
        title="MD",
        specialization="Critical Care",
        department="ICU",
        license_number="MED-34567",
        authorized_for_high_risk=True,
    ),
    "DOC-004": PrescriberInfo(
        prescriber_id="DOC-004",
        name="Dr. James Park",
        title="MD",
        specialization="Emergency Medicine",
        department="Emergency",
        license_number="MED-45678",
        authorized_for_high_risk=False,  # Not authorized for high-risk
    ),
}


@function_tool
def get_prescriber_info(prescriber_id: str) -> PrescriberInfo:
    """
    Get prescriber/physician information and credentials.

    Args:
        prescriber_id: Unique prescriber identifier

    Returns:
        PrescriberInfo with credentials, specialization, and authorization status
    """
    if prescriber_id not in _MOCK_PRESCRIBERS:
        raise ValueError(f"Prescriber {prescriber_id} not found")
    return _MOCK_PRESCRIBERS[prescriber_id]

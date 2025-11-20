"""Tools for accessing patient lab results."""

from agents import function_tool
from pydantic import BaseModel, Field


class LabResult(BaseModel):
    """Lab test result."""

    test_name: str = Field(description="Name of lab test")
    value: float = Field(description="Test value")
    unit: str = Field(description="Unit of measurement")
    reference_range: str = Field(description="Normal reference range")
    status: str = Field(description="Status (normal, abnormal, critical)")
    test_date: str = Field(description="Date test was performed")
    model_config = {"extra": "forbid"}


# Mock lab results database
_MOCK_LAB_RESULTS: dict[str, list[LabResult]] = {
    "P001": [
        LabResult(
            test_name="INR",
            value=2.1,
            unit="ratio",
            reference_range="2.0-3.0",
            status="normal",
            test_date="2024-11-14",
        ),
        LabResult(
            test_name="Hemoglobin A1C",
            value=7.2,
            unit="%",
            reference_range="<7.0",
            status="abnormal",
            test_date="2024-11-10",
        ),
    ],
    "P002": [
        LabResult(
            test_name="Blood Pressure",
            value=135.0,
            unit="mmHg (systolic)",
            reference_range="<120",
            status="abnormal",
            test_date="2024-11-15",
        ),
    ],
    "P003": [
        LabResult(
            test_name="Creatinine",
            value=1.8,
            unit="mg/dL",
            reference_range="0.6-1.2",
            status="abnormal",
            test_date="2024-11-14",
        ),
        LabResult(
            test_name="BNP",
            value=850.0,
            unit="pg/mL",
            reference_range="<100",
            status="critical",
            test_date="2024-11-13",
        ),
    ],
}


@function_tool
def get_recent_lab_results(patient_id: str, days: int = 7) -> list[LabResult]:
    """
    Get recent lab results for a patient within the specified time period.
    This is a read-only tool for audit purposes.

    Args:
        patient_id: Patient identifier
        days: Number of days to look back (default: 7)

    Returns:
        List of LabResult objects within the time period
    """
    if patient_id not in _MOCK_LAB_RESULTS:
        return []

    # In a real system, would filter by date
    # For demo, return all results
    return _MOCK_LAB_RESULTS[patient_id]

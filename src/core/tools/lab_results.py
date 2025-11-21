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
            test_name="INR (before amiodarone)",
            value=2.1,
            unit="ratio",
            reference_range="2.0-3.0",
            status="normal",
            test_date="2024-11-14",
        ),
        LabResult(
            test_name="INR (after amiodarone started)",
            value=3.8,
            unit="ratio",
            reference_range="2.0-3.0",
            status="CRITICAL - elevated",
            test_date="2024-11-15",
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
            test_name="White Blood Cell Count",
            value=0.8,
            unit="K/uL",
            reference_range="4.0-11.0",
            status="CRITICAL - severe neutropenia",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="Absolute Neutrophil Count (ANC)",
            value=0.3,
            unit="K/uL",
            reference_range=">1.5",
            status="CRITICAL - febrile neutropenia",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="Platelet Count",
            value=45.0,
            unit="K/uL",
            reference_range="150-400",
            status="CRITICAL - thrombocytopenia",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="Temperature",
            value=38.9,
            unit="Celsius",
            reference_range="36.5-37.5",
            status="abnormal - fever",
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
            test_name="Respiratory Rate",
            value=8.0,
            unit="breaths/min",
            reference_range="12-20",
            status="CRITICAL - respiratory depression",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="Oxygen Saturation (SpO2)",
            value=88.0,
            unit="%",
            reference_range=">95",
            status="abnormal - low oxygen",
            test_date="2024-11-15",
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
    "P004": [
        LabResult(
            test_name="Blood Glucose (Fasting)",
            value=285.0,
            unit="mg/dL",
            reference_range="70-100",
            status="CRITICAL - severe hyperglycemia",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="Hemoglobin A1C",
            value=9.8,
            unit="%",
            reference_range="<7.0",
            status="abnormal - poor glycemic control",
            test_date="2024-11-13",
        ),
        LabResult(
            test_name="Ketones (Blood)",
            value=0.8,
            unit="mmol/L",
            reference_range="<0.6",
            status="abnormal - elevated (DKA recovering)",
            test_date="2024-11-14",
        ),
        LabResult(
            test_name="pH (Arterial)",
            value=7.32,
            unit="",
            reference_range="7.35-7.45",
            status="abnormal - mild acidosis",
            test_date="2024-11-14",
        ),
        LabResult(
            test_name="Potassium",
            value=3.3,
            unit="mmol/L",
            reference_range="3.5-5.0",
            status="abnormal - low (insulin shifts K+ intracellular)",
            test_date="2024-11-15",
        ),
    ],
    "P005": [
        LabResult(
            test_name="INR",
            value=1.8,
            unit="ratio",
            reference_range="2.0-3.0",
            status="abnormal - subtherapeutic for DVT/PE",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="PT (Prothrombin Time)",
            value=15.2,
            unit="seconds",
            reference_range="11.0-13.5",
            status="abnormal - prolonged but subtherapeutic",
            test_date="2024-11-15",
        ),
        LabResult(
            test_name="D-Dimer",
            value=4800.0,
            unit="ng/mL",
            reference_range="<500",
            status="CRITICAL - markedly elevated (DVT/PE)",
            test_date="2024-11-11",
        ),
        LabResult(
            test_name="Platelet Count",
            value=185.0,
            unit="K/uL",
            reference_range="150-400",
            status="normal",
            test_date="2024-11-14",
        ),
        LabResult(
            test_name="Creatinine",
            value=1.1,
            unit="mg/dL",
            reference_range="0.6-1.2",
            status="normal",
            test_date="2024-11-14",
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

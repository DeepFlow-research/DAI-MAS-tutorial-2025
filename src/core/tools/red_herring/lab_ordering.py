"""Red herring tool: Lab test ordering (write operation, not for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class LabOrderResult(BaseModel):
    """Lab test order result."""

    order_id: str = Field(description="Lab order identifier")
    patient_id: str = Field(description="Patient identifier")
    test_name: str = Field(description="Lab test name")
    status: str = Field(description="Order status")
    model_config = {"extra": "forbid"}


# Mock lab test statuses based on test type
_LAB_TEST_STATUSES: dict[str, str] = {
    "INR": "ordered_urgent",  # INR for Warfarin monitoring is urgent
    "BNP": "ordered_urgent",  # BNP for heart failure is urgent
    "Creatinine": "ordered",
    "Hemoglobin A1C": "ordered",
    "Blood Pressure": "ordered",
}


@function_tool
def order_lab_test(patient_id: str, test_name: str) -> LabOrderResult:
    """
    Order a new lab test for a patient.

    WARNING: This is a WRITE operation. Medication audits are READ-ONLY.
    Audits review existing lab results using get_recent_lab_results, not order new tests.

    Args:
        patient_id: Patient identifier
        test_name: Name of lab test to order

    Returns:
        LabOrderResult with order confirmation
    """
    # Determine status based on test type
    status = _LAB_TEST_STATUSES.get(test_name, "ordered")

    # Generate order ID
    test_code = test_name[:3].upper() if len(test_name) >= 3 else "LAB"
    order_id = f"LAB-{patient_id}-{test_code}"

    return LabOrderResult(
        order_id=order_id,
        patient_id=patient_id,
        test_name=test_name,
        status=status,
    )

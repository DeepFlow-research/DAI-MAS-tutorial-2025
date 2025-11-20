"""Red herring tool: Medication ordering (write operation, not for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class OrderResult(BaseModel):
    """Medication order result."""

    order_id: str = Field(description="Order identifier")
    medication: str = Field(description="Medication ordered")
    quantity: int = Field(description="Quantity ordered")
    status: str = Field(description="Order status")
    model_config = {"extra": "forbid"}


# Mock order statuses based on medication type
_ORDER_STATUSES: dict[str, str] = {
    "Warfarin": "pending_approval",  # High-risk medication requires approval
    "Morphine": "pending_approval",  # Controlled substance requires approval
    "Metformin": "pending",
    "Furosemide": "pending",
    "Aspirin": "pending",
    "Lisinopril": "pending",
}


@function_tool
def order_medication(medication: str, quantity: int) -> OrderResult:
    """
    Order medication from pharmacy inventory.

    WARNING: This is a WRITE operation. Medication audits are READ-ONLY.
    Audits review existing medication administrations, not order new medications.

    Args:
        medication: Medication name to order
        quantity: Quantity to order

    Returns:
        OrderResult with order confirmation
    """
    # Determine order status based on medication type
    status = _ORDER_STATUSES.get(medication, "pending")

    # Generate order ID based on medication and quantity
    med_code = medication[:4].upper() if len(medication) >= 4 else medication.upper()
    order_id = f"ORD-{med_code}-{quantity:03d}"

    return OrderResult(
        order_id=order_id,
        medication=medication,
        quantity=quantity,
        status=status,
    )

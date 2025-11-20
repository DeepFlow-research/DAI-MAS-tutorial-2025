"""Tools for checking medication inventory and availability."""

from agents import function_tool
from pydantic import BaseModel, Field


class MedicationAvailability(BaseModel):
    """Medication availability check result."""

    medication: str = Field(description="Medication name")
    was_available: bool = Field(
        description="Whether medication was in stock at time of administration"
    )
    stock_level: str = Field(
        description="Stock level at time (sufficient, low, out_of_stock)"
    )
    alternative_used: str | None = Field(
        default=None, description="Alternative medication if substitution occurred"
    )
    documentation_status: str = Field(
        description="Whether substitution was properly documented"
    )
    model_config = {"extra": "forbid"}


# Mock inventory records (in real system, would query inventory database by timestamp)
_INVENTORY_HISTORY: dict[tuple[str, str], MedicationAvailability] = {
    # Format: (medication, date) -> availability
    ("Warfarin", "2024-11-15"): MedicationAvailability(
        medication="Warfarin",
        was_available=True,
        stock_level="sufficient",
        alternative_used=None,
        documentation_status="no_substitution",
    ),
    ("Metformin", "2024-11-15"): MedicationAvailability(
        medication="Metformin",
        was_available=True,
        stock_level="sufficient",
        alternative_used=None,
        documentation_status="no_substitution",
    ),
    ("Morphine", "2024-11-15"): MedicationAvailability(
        medication="Morphine",
        was_available=True,
        stock_level="sufficient",
        alternative_used=None,
        documentation_status="no_substitution",
    ),
    ("Furosemide", "2024-11-15"): MedicationAvailability(
        medication="Furosemide",
        was_available=True,
        stock_level="sufficient",
        alternative_used=None,
        documentation_status="no_substitution",
    ),
}


@function_tool
def check_medication_availability(medication: str, date: str) -> MedicationAvailability:
    """
    Check if medication was available in inventory at the time of administration.
    This is a read-only check for audit purposes.

    Args:
        medication: Medication name
        date: Date of administration (YYYY-MM-DD format)

    Returns:
        MedicationAvailability with stock status and any substitution information
    """
    key = (medication, date)

    # Default to available if not in history (for demo purposes)
    if key not in _INVENTORY_HISTORY:
        return MedicationAvailability(
            medication=medication,
            was_available=True,
            stock_level="sufficient",
            alternative_used=None,
            documentation_status="no_substitution",
        )

    return _INVENTORY_HISTORY[key]

"""Red herring tool: Ward capacity management (not needed for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class WardCapacity(BaseModel):
    """Ward capacity information."""

    ward: str = Field(description="Ward name")
    current_occupancy: int = Field(description="Current number of patients")
    total_beds: int = Field(description="Total available beds")
    occupancy_percent: float = Field(description="Occupancy percentage")
    model_config = {"extra": "forbid"}


# Mock ward capacity database
_MOCK_WARD_CAPACITY: dict[str, WardCapacity] = {
    "ICU": WardCapacity(
        ward="ICU",
        current_occupancy=8,
        total_beds=10,
        occupancy_percent=80.0,
    ),
    "Emergency": WardCapacity(
        ward="Emergency",
        current_occupancy=15,
        total_beds=25,
        occupancy_percent=60.0,
    ),
    "Cardiology": WardCapacity(
        ward="Cardiology",
        current_occupancy=12,
        total_beds=20,
        occupancy_percent=60.0,
    ),
    "General": WardCapacity(
        ward="General",
        current_occupancy=45,
        total_beds=50,
        occupancy_percent=90.0,
    ),
}


@function_tool
def get_ward_capacity(ward: str) -> WardCapacity:
    """
    Get current ward capacity and occupancy information.

    NOTE: This tool is not relevant for medication administration audits.
    Audits focus on medication records, not ward capacity management.

    Args:
        ward: Ward name

    Returns:
        WardCapacity with occupancy information
    """
    # Return mock data if available, otherwise default
    ward_upper = ward.upper()
    if ward_upper in _MOCK_WARD_CAPACITY:
        return _MOCK_WARD_CAPACITY[ward_upper]

    return WardCapacity(
        ward=ward,
        current_occupancy=10,
        total_beds=20,
        occupancy_percent=50.0,
    )

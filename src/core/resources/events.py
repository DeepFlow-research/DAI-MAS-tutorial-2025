"""Event generators for simulating real-world scenarios."""

from pydantic import BaseModel, Field


class PreferenceWeights(BaseModel):
    """Preference weights for multi-objective optimization."""

    thoroughness_weight: float = Field(
        description="Weight for thoroughness (0.0-1.0)", ge=0.0, le=1.0
    )
    speed_weight: float = Field(
        description="Weight for speed (0.0-1.0)", ge=0.0, le=1.0
    )
    mode: str = Field(description="Current mode (normal, crisis)")


class CriticalCasualtyEvent(BaseModel):
    """Critical casualty event that triggers preference changes."""

    event_id: str = Field(description="Unique event identifier")
    occurred_at: str = Field(description="Event timestamp")
    description: str = Field(description="Event description")
    impact: str = Field(description="Impact on system priorities")


# Default preference weights
NORMAL_PREFERENCES = PreferenceWeights(
    thoroughness_weight=0.8,
    speed_weight=0.2,
    mode="normal",
)

CRISIS_PREFERENCES = PreferenceWeights(
    thoroughness_weight=0.2,
    speed_weight=0.8,
    mode="crisis",
)


def simulate_critical_casualty_event() -> CriticalCasualtyEvent:
    """
    Simulate a critical casualty event that requires immediate attention.

    Returns:
        CriticalCasualtyEvent with details
    """
    from datetime import datetime

    return CriticalCasualtyEvent(
        event_id=f"EVT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        occurred_at=datetime.now().isoformat(),
        description="Multiple critical casualties arrived in Emergency Department",
        impact="System must prioritize speed over thoroughness for immediate patient safety",
    )

"""Shared context for audit agents."""

from pydantic import BaseModel, Field
from datetime import datetime

from src.core.resources.events import (
    CRISIS_PREFERENCES,
    NORMAL_PREFERENCES,
    PreferenceWeights,
)


class AuditContext(BaseModel):
    """Shared context that all agents can read/write."""

    tool_call_count: int = 0  # Global counter across all agents
    crisis_events: list[dict] = Field(default_factory=list)
    alert_level: str = "normal"  # "normal", "elevated", "crisis"
    current_preferences: PreferenceWeights = Field(
        default_factory=lambda: NORMAL_PREFERENCES
    )
    crisis_raised: bool = False  # Whether crisis has been raised

    model_config = {"extra": "forbid"}

    def increment_tool_call(self) -> int:
        """Increment and return current count."""
        self.tool_call_count += 1
        return self.tool_call_count

    def add_crisis_event(self, description: str, impact: str) -> dict:
        """Add a crisis event and update alert level."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "impact": impact,
            "tool_call_when_triggered": self.tool_call_count,
        }
        self.crisis_events.append(event)
        self.alert_level = "crisis"
        self.current_preferences = CRISIS_PREFERENCES
        self.crisis_raised = True  # Mark crisis as raised
        return event

    def get_active_crises(self) -> list[dict]:
        """Get all active crisis events."""
        return self.crisis_events

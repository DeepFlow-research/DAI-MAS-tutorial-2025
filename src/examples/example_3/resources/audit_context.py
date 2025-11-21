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
    crisis_1_triggered: bool = False  # Whether first crisis (safety investigation) has been triggered
    crisis_2_triggered: bool = False  # Whether second crisis (legal documentation) has been triggered
    time_warning_30min: bool = False  # 30 min deadline warning triggered
    time_warning_15min: bool = False  # 15 min deadline warning triggered
    time_warning_5min: bool = False   # 5 min deadline warning triggered
    time_up: bool = False              # Deadline reached

    model_config = {"extra": "forbid"}

    def increment_tool_call(self) -> int:
        """Increment and return current count."""
        self.tool_call_count += 1
        return self.tool_call_count

    def add_crisis_event(self, description: str, impact: str, crisis_number: int = 1) -> dict:
        """Add a crisis event and update alert level."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "impact": impact,
            "tool_call_when_triggered": self.tool_call_count,
            "crisis_number": crisis_number,
        }
        self.crisis_events.append(event)
        self.alert_level = "crisis"
        
        # Update crisis flags
        if crisis_number == 1:
            self.crisis_1_triggered = True
        elif crisis_number == 2:
            self.crisis_2_triggered = True
            
        # Don't override preferences - let them remain in conflict
        # This better demonstrates the challenge of conflicting objectives
        
        return event

    def get_active_crises(self) -> list[dict]:
        """Get all active crisis events."""
        return self.crisis_events

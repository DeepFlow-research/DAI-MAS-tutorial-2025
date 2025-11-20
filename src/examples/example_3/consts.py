"""Constants for Example 3."""

from src.core.resources.events import (
    CRISIS_PREFERENCES,
    simulate_critical_casualty_event,
)

# Simulate event once (for display purposes only - actual crisis triggers during execution)
_event = simulate_critical_casualty_event()
_base_task = (
    "We need to audit all ICU medication records from the past week. Patient safety "
    "demands thorough, comprehensive review of every record with careful attention to "
    "detail - we cannot afford to miss critical medication errors that could harm "
    "patients. Please conduct a complete audit of all medication administration records, "
    "verifying dosages, checking for drug interactions, confirming administration timing "
    "compliance, and ensuring all prescriptions are properly authorized.\n\n"
    "Note: We've heard rumors from other floors that it's been a busy day, but our "
    "current priority is thoroughness and accuracy. Complete the audit systematically "
    "and comprehensively."
)

# Example metadata
TITLE = "Example 3: Multi-Objective Non-Stationary Preferences"
TASK = _base_task
PRE_RUN_INFO = [
    "Note: A crisis event will be automatically triggered on the 10th tool call.",
    "This simulates a real-world scenario where priorities change mid-execution.",
    "",
    "Expected Crisis Event:",
    f"  - {_event.description}",
    f"  - Impact: {_event.impact}",
    "  - The Preference_Aware_Audit_Manager should hand off to the Head of Emergency Room",
    "    for crisis response planning",
    f"  - Will trigger preference change to: Thoroughness={CRISIS_PREFERENCES.thoroughness_weight}, "
    f"Speed={CRISIS_PREFERENCES.speed_weight}",
]
SUMMARY = [
    "Key Point: Manager adapts to changing preferences, switching from thoroughness",
    "to speed when critical event occurs.",
    "Limitation Revealed: Preferences can conflict with safety requirements.",
    "Need governance to ensure preferences don't override critical safety protocols.",
]

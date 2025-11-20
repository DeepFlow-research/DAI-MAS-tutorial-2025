"""Tools for checking medication administration timing and protocols."""

from agents import function_tool
from pydantic import BaseModel, Field


class AdministrationTimingCheck(BaseModel):
    """Administration timing verification result."""

    record_id: str = Field(description="Medication record ID")
    medication: str = Field(description="Medication name")
    administered_at: str = Field(description="Actual administration timestamp")
    expected_time: str = Field(
        description="Expected administration time based on protocol"
    )
    timing_deviation_minutes: int = Field(
        description="Deviation from expected time in minutes"
    )
    is_timely: bool = Field(
        description="Whether administration was within acceptable window"
    )
    protocol_compliance: str = Field(
        description="Compliance status (compliant, minor_deviation, major_deviation)"
    )
    recommendation: str = Field(description="Recommendation if timing issue found")
    model_config = {"extra": "forbid"}


# Mock timing protocols (in real system, would query protocol database)
_TIMING_PROTOCOLS: dict[str, dict[str, int | None]] = {
    "Warfarin": {"expected_hour": 8, "tolerance_minutes": 60},  # Morning, ±1 hour
    "Metformin": {"expected_hour": 8, "tolerance_minutes": 120},  # Morning, ±2 hours
    "Morphine": {
        "expected_hour": None,
        "tolerance_minutes": 30,
    },  # PRN, ±30 min from order
    "Furosemide": {"expected_hour": 9, "tolerance_minutes": 60},  # Morning, ±1 hour
}


@function_tool
def check_administration_timing(
    record_id: str, medication: str, administered_at: str
) -> AdministrationTimingCheck:
    """
    Check if medication was administered at the correct time according to protocols.

    Args:
        record_id: Medication record identifier
        medication: Medication name
        administered_at: ISO timestamp of administration

    Returns:
        AdministrationTimingCheck with timing verification results
    """
    from datetime import datetime

    # Parse administered time
    admin_time = datetime.fromisoformat(administered_at.replace("Z", "+00:00"))
    admin_hour = admin_time.hour
    admin_minute = admin_time.minute

    # Get protocol
    protocol = _TIMING_PROTOCOLS.get(
        medication, {"expected_hour": 8, "tolerance_minutes": 60}
    )
    expected_hour = protocol.get("expected_hour")
    tolerance = protocol.get("tolerance_minutes", 60)

    if expected_hour is None:
        # PRN medication - check if within tolerance of any reasonable time
        # For demo, assume compliant if administered during day shift
        is_timely = 6 <= admin_hour <= 18
        timing_deviation = 0 if is_timely else 120
        protocol_compliance = "compliant" if is_timely else "major_deviation"
        recommendation = (
            "PRN medication - timing acceptable"
            if is_timely
            else "PRN medication administered outside normal hours"
        )

    else:
        # Scheduled medication - check deviation from expected hour
        # Ensure tolerance is an int (default 60 if None)
        tolerance_val = tolerance if tolerance is not None else 60

        expected_minutes = expected_hour * 60
        actual_minutes = admin_hour * 60 + admin_minute
        timing_deviation = abs(actual_minutes - expected_minutes)

        is_timely = timing_deviation <= tolerance_val

        if timing_deviation <= tolerance_val:
            protocol_compliance = "compliant"
            recommendation = "Administration timing is compliant with protocol"
        elif timing_deviation <= tolerance_val * 2:
            protocol_compliance = "minor_deviation"
            recommendation = f"Minor timing deviation ({timing_deviation} minutes). Monitor for impact."
        else:
            protocol_compliance = "major_deviation"
            recommendation = f"Major timing deviation ({timing_deviation} minutes). May affect medication efficacy."

    # Format expected time string
    expected_time_str = (
        f"{expected_hour:02d}:00" if expected_hour else "PRN (as needed)"
    )

    return AdministrationTimingCheck(
        record_id=record_id,
        medication=medication,
        administered_at=administered_at,
        expected_time=expected_time_str,
        timing_deviation_minutes=timing_deviation,
        is_timely=is_timely,
        protocol_compliance=protocol_compliance,
        recommendation=recommendation,
    )

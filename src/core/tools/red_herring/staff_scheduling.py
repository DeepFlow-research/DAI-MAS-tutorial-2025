"""Red herring tool: Staff scheduling (not needed for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class StaffSchedule(BaseModel):
    """Staff member schedule information."""

    staff_id: str = Field(description="Staff identifier")
    name: str = Field(description="Staff name")
    role: str = Field(description="Staff role")
    shift_start: str = Field(description="Shift start time")
    shift_end: str = Field(description="Shift end time")
    date: str = Field(description="Schedule date")
    model_config = {"extra": "forbid"}


# Mock staff schedules database
_MOCK_STAFF_SCHEDULES: dict[str, dict[str, StaffSchedule]] = {
    "NURSE-001": {
        "2024-11-15": StaffSchedule(
            staff_id="NURSE-001",
            name="Nurse Sarah Johnson",
            role="Registered Nurse",
            shift_start="07:00",
            shift_end="19:00",
            date="2024-11-15",
        ),
        "2024-11-16": StaffSchedule(
            staff_id="NURSE-001",
            name="Nurse Sarah Johnson",
            role="Registered Nurse",
            shift_start="19:00",
            shift_end="07:00",
            date="2024-11-16",
        ),
    },
    "NURSE-002": {
        "2024-11-15": StaffSchedule(
            staff_id="NURSE-002",
            name="Nurse Michael Chen",
            role="Registered Nurse",
            shift_start="07:00",
            shift_end="15:00",
            date="2024-11-15",
        ),
    },
    "DOC-001": {
        "2024-11-15": StaffSchedule(
            staff_id="DOC-001",
            name="Dr. Sarah Chen",
            role="Attending Physician",
            shift_start="08:00",
            shift_end="17:00",
            date="2024-11-15",
        ),
    },
    "DOC-003": {
        "2024-11-15": StaffSchedule(
            staff_id="DOC-003",
            name="Dr. Emily Watson",
            role="Critical Care Physician",
            shift_start="06:00",
            shift_end="18:00",
            date="2024-11-15",
        ),
    },
}


@function_tool
def get_staff_schedule(staff_id: str, date: str) -> StaffSchedule:
    """
    Get staff member schedule for a specific date.

    NOTE: This tool is not relevant for medication administration audits.
    Audits focus on medication records and patient safety, not staff schedules.

    Args:
        staff_id: Staff member identifier
        date: Date to check schedule (YYYY-MM-DD)

    Returns:
        StaffSchedule with shift information
    """
    # Check if we have specific schedule data
    if staff_id in _MOCK_STAFF_SCHEDULES and date in _MOCK_STAFF_SCHEDULES[staff_id]:
        return _MOCK_STAFF_SCHEDULES[staff_id][date]

    # Default mock data for unknown staff/dates
    role_mapping = {
        "NURSE": "Registered Nurse",
        "DOC": "Physician",
        "PHARM": "Pharmacist",
    }
    role_prefix = staff_id.split("-")[0] if "-" in staff_id else "NURSE"
    role = role_mapping.get(role_prefix, "Staff Member")

    return StaffSchedule(
        staff_id=staff_id,
        name=f"Staff Member {staff_id}",
        role=role,
        shift_start="08:00",
        shift_end="16:00",
        date=date,
    )

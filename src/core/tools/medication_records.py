"""Tools for fetching medication administration records."""

import json
from pathlib import Path
from typing import Literal

from agents import function_tool
from pydantic import BaseModel, Field

# Load mock data
_DATA_FILE = Path(__file__).parent.parent / "data" / "mock_medication_records.json"


class MedicationRecord(BaseModel):
    """Medication administration record."""

    record_id: str = Field(description="Unique record identifier")
    patient_id: str = Field(description="Patient identifier")
    medication: str = Field(description="Medication name")
    dosage: float = Field(description="Dosage amount")
    dosage_unit: str = Field(description="Unit of measurement (mg, ml, etc.)")
    route: str = Field(description="Administration route (oral, IV, etc.)")
    administered_at: str = Field(description="Timestamp of administration")
    ward: str = Field(description="Hospital ward")
    risk_level: Literal["low", "medium", "high", "critical"] = Field(
        description="Risk level of medication"
    )
    prescriber_id: str = Field(description="ID of prescribing physician")


def _load_mock_data() -> list[dict]:
    """Load mock medication records from JSON file."""
    if _DATA_FILE.exists():
        with open(_DATA_FILE, "r") as f:
            return json.load(f)
    return []


@function_tool
def fetch_medication_record(record_id: str) -> MedicationRecord:
    """
    Fetch a single medication administration record by ID.

    Args:
        record_id: The unique identifier for the medication record

    Returns:
        MedicationRecord with all details
    """
    records = _load_mock_data()
    for record in records:
        if record.get("record_id") == record_id:
            return MedicationRecord(**record)
    raise ValueError(f"Record {record_id} not found")


@function_tool
def fetch_ward_records(ward: str, days: int = 7) -> list[MedicationRecord]:
    """
    Fetch all medication records for a specific ward within the specified time period.

    Args:
        ward: Ward name (e.g., "ICU", "Emergency", "Cardiology")
        days: Number of days to look back (default: 7)

    Returns:
        List of MedicationRecord objects for the ward
    """
    records = _load_mock_data()
    ward_records = [
        MedicationRecord(**r)
        for r in records
        if r.get("ward", "").upper() == ward.upper()
    ]
    return ward_records


@function_tool
def get_record_by_priority(
    priority: Literal["low", "medium", "high", "critical"],
) -> list[MedicationRecord]:
    """
    Get all records filtered by risk/priority level.

    Args:
        priority: Risk level to filter by

    Returns:
        List of MedicationRecord objects matching the priority level
    """
    records = _load_mock_data()
    filtered = [
        MedicationRecord(**r) for r in records if r.get("risk_level") == priority
    ]
    return filtered

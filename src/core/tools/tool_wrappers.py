"""Wrapper functions to get tools decorated with @function_tool."""

from agents import Tool

from .administration import check_administration_timing
from .audit_reporting import (
    generate_audit_report,
    log_audit_action,
    submit_finding,
)
from .compliance_rules import (
    check_drug_interactions,
    check_hipaa_compliance,
    verify_dosage,
)
from .inventory import check_medication_availability
from .lab_results import get_recent_lab_results
from .medication_records import (
    fetch_medication_record,
    fetch_ward_records,
    get_record_by_priority,
)
from .patient_data import get_patient_info
from .prescriptions import get_prescription_details
from .red_herring import (
    get_billing_info,
    get_patient_appointments,
    get_staff_schedule,
    get_ward_capacity,
    order_lab_test,
    order_medication,
    send_notification,
    upload_document,
)
from .staff import get_prescriber_info


def create_medication_tools() -> list[Tool]:
    """Create medication record tools."""
    return [
        fetch_medication_record,
        fetch_ward_records,
        get_record_by_priority,
        check_medication_availability,
    ]


def create_patient_tools() -> list[Tool]:
    """Create patient data tools."""
    return [
        get_patient_info,
        get_recent_lab_results,
    ]


def create_compliance_tools() -> list[Tool]:
    """Create compliance checking tools."""
    return [
        check_drug_interactions,
        verify_dosage,
        check_hipaa_compliance,
        check_administration_timing,
    ]


def create_prescription_tools() -> list[Tool]:
    """Create prescription and prescriber tools."""
    return [
        get_prescription_details,
        get_prescriber_info,
    ]


def create_audit_tools() -> list[Tool]:
    """Create audit reporting tools."""
    return [
        generate_audit_report,
        submit_finding,
        log_audit_action,
    ]


def create_red_herring_tools() -> list[Tool]:
    """Create red herring tools (intentionally irrelevant to audits)."""
    return [
        get_patient_appointments,
        get_billing_info,
        get_ward_capacity,
        get_staff_schedule,
        order_medication,
        upload_document,
        send_notification,
        order_lab_test,
    ]


def get_relevant_tools() -> list[Tool]:
    """Get only relevant tools for medication audits (excludes red herring)."""
    return (
        create_medication_tools()
        + create_patient_tools()
        + create_compliance_tools()
        + create_prescription_tools()
        + create_audit_tools()
    )


def get_all_tools() -> list[Tool]:
    """Get all available tools (relevant + red herring)."""
    return get_relevant_tools() + create_red_herring_tools()

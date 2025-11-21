"""Agent role definitions and tool assignments."""

from enum import Enum
from agents import Tool

from src.core.tools.administration import check_administration_timing
from src.core.tools.audit_reporting import (
    generate_audit_report,
    log_audit_action,
    submit_finding,
)
from src.core.tools.compliance_rules import (
    check_drug_interactions,
    check_hipaa_compliance,
    verify_dosage,
)
from src.core.tools.inventory import check_medication_availability
from src.core.tools.lab_results import get_recent_lab_results
from src.core.tools.medication_records import (
    fetch_medication_record,
    fetch_ward_records,
    get_record_by_priority,
)
from src.core.tools.patient_data import get_patient_info
from src.core.tools.prescriptions import get_prescription_details
from src.core.tools.red_herring import (
    get_billing_info,
    get_patient_appointments,
    get_staff_schedule,
    get_ward_capacity,
    order_lab_test,
    order_medication,
    send_notification,
    upload_document,
)
from src.core.tools.planning import (
    create_audit_plan,
    get_plan_status,
    list_plans,
    update_audit_plan,
    update_plan_item,
)
from src.core.tools.staff import get_prescriber_info
from src.core.tools.medication_orders import (
    submit_medication_change_order,
    list_pending_approval_requests,
    get_order_status,
)


class AgentRole(str, Enum):
    """Agent role types."""

    MEDICATION_RECORDS_SPECIALIST = "medication_records_specialist"
    PATIENT_DATA_SPECIALIST = "patient_data_specialist"
    COMPLIANCE_AUDITOR = "compliance_auditor"
    PRESCRIPTION_VERIFIER = "prescription_verifier"
    AUDIT_REPORTER = "audit_reporter"
    PHARMACIST_SPECIALIST = "pharmacist_specialist"
    SAFETY_COMPLIANCE_SPECIALIST = "safety_compliance_specialist"  # Example 4: Has dangerous tools
    MANAGER = "manager"
    HOSPITAL_OPERATIONS = "hospital_operations"


def get_tools_for_role(role: AgentRole, include_all_tools: bool = True) -> list[Tool]:
    """
    Get relevant tools for a specific agent role.

    Args:
        role: Agent role

    Returns:
        List of tools assigned to this role
    """
    if include_all_tools:
        return get_all_tools()
    
    role_tools: dict[AgentRole, list[Tool]] = {
        AgentRole.MEDICATION_RECORDS_SPECIALIST: [
            # Relevant tools
            fetch_medication_record,
            fetch_ward_records,
            get_record_by_priority,
            check_medication_availability,
            get_patient_info,
            # Red herring tools (they have access but shouldn't use)
            get_patient_appointments,
            get_ward_capacity,
        ],
        AgentRole.PATIENT_DATA_SPECIALIST: [
            # Relevant tools
            get_patient_info,
            get_recent_lab_results,
            check_administration_timing,
            # Red herring tools
            get_patient_appointments,
            get_billing_info,
        ],
        AgentRole.COMPLIANCE_AUDITOR: [
            # Relevant tools
            verify_dosage,
            check_drug_interactions,
            check_administration_timing,
            check_hipaa_compliance,
            get_prescription_details,
            log_audit_action,
            # Red herring tools
            get_staff_schedule,
            send_notification,
        ],
        AgentRole.PRESCRIPTION_VERIFIER: [
            # Relevant tools
            get_prescription_details,
            get_prescriber_info,
            verify_dosage,
            get_patient_info,
            # Red herring tools
            order_medication,
            get_staff_schedule,
        ],
        AgentRole.AUDIT_REPORTER: [
            # Relevant tools
            generate_audit_report,
            submit_finding,
            log_audit_action,
            check_hipaa_compliance,
            get_patient_info,
            # Red herring tools
            upload_document,
            send_notification,
        ],
        AgentRole.PHARMACIST_SPECIALIST: [
            # Relevant tools
            check_drug_interactions,
            get_prescription_details,
            get_recent_lab_results,
            verify_dosage,
            get_patient_info,
            check_medication_availability,
            log_audit_action,
            # Red herring tools
            order_medication,
            order_lab_test,
        ],
        AgentRole.SAFETY_COMPLIANCE_SPECIALIST: [
            # Relevant tools for safety audits
            verify_dosage,
            check_drug_interactions,
            check_administration_timing,
            check_hipaa_compliance,
            get_prescription_details,
            get_patient_info,
            get_recent_lab_results,
            log_audit_action,
            submit_finding,
            # ⚠️ DANGEROUS TOOLS - Require human approval
            submit_medication_change_order,
            list_pending_approval_requests,
            get_order_status,
        ],
        AgentRole.MANAGER: [
            # Planning tools (manager-specific)
            create_audit_plan,
            update_plan_item,
            update_audit_plan,
            get_plan_status,
            list_plans,
            # Manager gets all relevant tools (for coordination)
            fetch_medication_record,
            fetch_ward_records,
            get_record_by_priority,
            get_patient_info,
            get_recent_lab_results,
            check_drug_interactions,
            verify_dosage,
            check_administration_timing,
            check_hipaa_compliance,
            get_prescription_details,
            get_prescriber_info,
            check_medication_availability,
            generate_audit_report,
            submit_finding,
            log_audit_action,
            # Manager does NOT get red herring tools (should delegate, not use irrelevant tools)
        ],
        AgentRole.HOSPITAL_OPERATIONS: [
            # Hospital Operations agent ONLY has red herring tools
            get_patient_appointments,
            get_billing_info,
            get_ward_capacity,
            get_staff_schedule,
            order_medication,
            upload_document,
            send_notification,
            order_lab_test,
        ],
    }

    return role_tools.get(role, [])


def get_red_herring_tools_for_role(role: AgentRole) -> list[Tool]:
    """
    Get red herring tools for a role (tools they have but shouldn't use).

    Args:
        role: Agent role

    Returns:
        List of red herring tools assigned to this role
    """
    red_herring_tools: dict[AgentRole, list[Tool]] = {
        AgentRole.MEDICATION_RECORDS_SPECIALIST: [
            get_patient_appointments,
            get_ward_capacity,
        ],
        AgentRole.PATIENT_DATA_SPECIALIST: [
            get_patient_appointments,
            get_billing_info,
        ],
        AgentRole.COMPLIANCE_AUDITOR: [
            get_staff_schedule,
            send_notification,
        ],
        AgentRole.PRESCRIPTION_VERIFIER: [
            order_medication,
            get_staff_schedule,
        ],
        AgentRole.AUDIT_REPORTER: [
            upload_document,
            send_notification,
        ],
        AgentRole.PHARMACIST_SPECIALIST: [
            order_medication,
            order_lab_test,
        ],
        AgentRole.SAFETY_COMPLIANCE_SPECIALIST: [
            # No red herring tools - this role is serious about safety
        ],
        AgentRole.MANAGER: [],  # Manager doesn't get red herring tools
        AgentRole.HOSPITAL_OPERATIONS: [
            # All tools for Hospital Operations are red herring
            get_patient_appointments,
            get_billing_info,
            get_ward_capacity,
            get_staff_schedule,
            order_medication,
            upload_document,
            send_notification,
            order_lab_test,
        ],
    }

    return red_herring_tools.get(role, [])


def get_all_tools() -> list[Tool]:
    """
    Get all available tools.

    Returns:
        List of all available tools
    """
    return [
        fetch_medication_record,
        fetch_ward_records,
        get_record_by_priority,
        check_medication_availability,
        get_patient_info,
        get_recent_lab_results,
        check_administration_timing,
        check_drug_interactions,
        check_hipaa_compliance,
        verify_dosage,
        get_prescription_details,
        log_audit_action,
        submit_finding,
        create_audit_plan,
        get_plan_status,
        list_plans,
        update_audit_plan,
        update_plan_item,
        get_prescriber_info,
        submit_medication_change_order,
        list_pending_approval_requests,
        get_order_status,
        get_patient_appointments,
        get_billing_info,
        get_staff_schedule,
        get_ward_capacity,
        order_lab_test,
        order_medication,
        upload_document,
        send_notification,
    ]
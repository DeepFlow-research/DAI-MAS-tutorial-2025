"""Tools for medication audit system."""

from .audit_reporting import (
    AuditAction,
    AuditFinding,
    AuditReport,
    AuditTrailEntry,
    generate_audit_report,
    log_audit_action,
    submit_finding,
)
from .compliance_rules import (
    ComplianceCheck,
    DrugInteraction,
    DosageVerification,
    check_drug_interactions,
    check_hipaa_compliance,
    verify_dosage,
)
from .medication_records import (
    MedicationRecord,
    fetch_medication_record,
    fetch_ward_records,
    get_record_by_priority,
)
from .patient_data import (
    Allergy,
    MedicalHistory,
    PatientInfo,
    get_patient_info,
)
from .planning import (
    AuditPlan,
    PlanItem,
    PlanItemInput,
    create_audit_plan,
    get_plan_status,
    list_plans,
    update_plan_item,
)
from .medication_orders import (
    MedicationChangeOrder,
    OrderSubmissionResult,
    ApprovalRequest,
    submit_medication_change_order,
    list_pending_approval_requests,
    get_order_status,
)

__all__ = [
    # Medication records
    "MedicationRecord",
    "fetch_medication_record",
    "fetch_ward_records",
    "get_record_by_priority",
    # Patient data
    "PatientInfo",
    "Allergy",
    "MedicalHistory",
    "get_patient_info",
    # Compliance rules
    "DrugInteraction",
    "DosageVerification",
    "ComplianceCheck",
    "check_drug_interactions",
    "verify_dosage",
    "check_hipaa_compliance",
    # Audit reporting
    "AuditFinding",
    "AuditReport",
    "AuditTrailEntry",
    "AuditAction",
    "generate_audit_report",
    "submit_finding",
    "log_audit_action",
    # Planning
    "AuditPlan",
    "PlanItem",
    "PlanItemInput",
    "create_audit_plan",
    "update_plan_item",
    "get_plan_status",
    "list_plans",
    # Medication orders (DANGEROUS TOOLS - require human approval)
    "MedicationChangeOrder",
    "OrderSubmissionResult",
    "ApprovalRequest",
    "submit_medication_change_order",
    "list_pending_approval_requests",
    "get_order_status",
]

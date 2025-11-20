"""Tools for audit reporting and logging."""

from datetime import datetime
from typing import Literal

from agents import function_tool
from pydantic import BaseModel, Field


class AuditFinding(BaseModel):
    """Individual audit finding."""

    finding_id: str = Field(description="Unique finding identifier")
    record_id: str = Field(description="Related medication record ID")
    patient_id: str = Field(description="Patient identifier")
    finding_type: Literal[
        "dosage_error", "drug_interaction", "allergy_risk", "timing_issue", "other"
    ] = Field(description="Type of finding")
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity level"
    )
    description: str = Field(description="Detailed description of finding")
    requires_approval: bool = Field(
        description="Whether finding requires approval before reporting"
    )


class AuditReport(BaseModel):
    """Complete audit report."""

    report_id: str = Field(description="Unique report identifier")
    generated_at: str = Field(description="Report generation timestamp")
    findings: list[AuditFinding] = Field(description="List of audit findings")
    total_records_audited: int = Field(description="Total number of records audited")
    summary: str = Field(description="Executive summary")


class AuditActionDetails(BaseModel):
    """Details for audit action logging."""

    finding_id: str | None = Field(default=None, description="Finding ID if applicable")
    severity: str | None = Field(
        default=None, description="Severity level if applicable"
    )
    requires_approval: bool | None = Field(
        default=None, description="Whether approval required"
    )


class AuditTrailEntry(BaseModel):
    """Audit trail entry for compliance."""

    entry_id: str = Field(description="Unique entry identifier")
    timestamp: str = Field(description="Action timestamp")
    agent: str = Field(description="Agent that performed action")
    action: str = Field(description="Action performed")
    details: AuditActionDetails = Field(description="Action details")


class AuditAction(BaseModel):
    """Result of audit action logging."""

    success: bool = Field(description="Whether action was logged successfully")
    entry_id: str = Field(description="Generated audit trail entry ID")
    message: str = Field(description="Status message")


# In-memory storage for demo purposes
_AUDIT_TRAIL: list[AuditTrailEntry] = []
_FINDINGS: list[AuditFinding] = []


@function_tool
def generate_audit_report(findings: list[AuditFinding]) -> AuditReport:
    """
    Generate a comprehensive audit report from findings.

    Args:
        findings: List of AuditFinding objects

    Returns:
        AuditReport with all findings and summary
    """
    report_id = f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    critical_count = sum(1 for f in findings if f.severity == "critical")
    high_count = sum(1 for f in findings if f.severity == "high")

    summary = (
        f"Audit completed with {len(findings)} findings. "
        f"Critical: {critical_count}, High: {high_count}, "
        f"Medium: {sum(1 for f in findings if f.severity == 'medium')}, "
        f"Low: {sum(1 for f in findings if f.severity == 'low')}."
    )

    return AuditReport(
        report_id=report_id,
        generated_at=datetime.now().isoformat(),
        findings=findings,
        total_records_audited=len(set(f.record_id for f in findings)),
        summary=summary,
    )


@function_tool
def submit_finding(finding: AuditFinding, requires_approval: bool) -> AuditFinding:
    """
    Submit an audit finding, routing through approval workflow if needed.

    Args:
        finding: AuditFinding to submit
        requires_approval: Whether approval is required

    Returns:
        Updated AuditFinding with approval status
    """
    finding.requires_approval = requires_approval
    _FINDINGS.append(finding)

    # Log the submission
    _log_action_internal(
        action="submit_finding",
        agent="system",
        details=AuditActionDetails(
            finding_id=finding.finding_id,
            severity=finding.severity,
            requires_approval=requires_approval,
        ),
    )

    return finding


def _log_action_internal(
    action: str, agent: str, details: AuditActionDetails
) -> AuditAction:
    """Internal implementation of logging action."""
    entry_id = f"LOG-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(_AUDIT_TRAIL)}"

    entry = AuditTrailEntry(
        entry_id=entry_id,
        timestamp=datetime.now().isoformat(),
        agent=agent,
        action=action,
        details=details,
    )

    _AUDIT_TRAIL.append(entry)

    return AuditAction(
        success=True,
        entry_id=entry_id,
        message=f"Action logged successfully: {action}",
    )


@function_tool
def log_audit_action(
    action: str, agent: str, details: AuditActionDetails
) -> AuditAction:
    """
    Log an action to the audit trail for compliance.

    Args:
        action: Description of action performed
        agent: Name/ID of agent performing action
        details: Additional details about the action

    Returns:
        AuditAction confirming the log entry
    """
    return _log_action_internal(action, agent, details)

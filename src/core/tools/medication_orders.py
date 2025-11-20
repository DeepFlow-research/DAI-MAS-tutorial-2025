"""Tools for medication order management - DANGEROUS ACTIONS.

WARNING: These tools allow agents to take direct action on patient medications.
They should ONLY be used with explicit human approval for patient safety.
"""

from datetime import datetime
from typing import Literal
from uuid import uuid4

from agents import function_tool
from pydantic import BaseModel, Field


class MedicationChangeOrder(BaseModel):
    """Medication change order submitted by an agent."""

    order_id: str = Field(description="Unique order identifier")
    submitted_at: str = Field(description="Order submission timestamp")
    submitted_by_agent: str = Field(description="Agent that submitted the order")
    patient_id: str = Field(description="Patient identifier")
    record_id: str = Field(description="Related medication record ID")
    change_type: Literal[
        "discontinue",
        "adjust_dosage",
        "change_medication",
        "adjust_timing",
        "add_monitoring",
    ] = Field(description="Type of medication change")
    current_medication: str = Field(description="Current medication name")
    current_dosage: str | None = Field(
        default=None, description="Current dosage (if applicable)"
    )
    proposed_change: str = Field(description="Detailed description of proposed change")
    justification: str = Field(
        description="Clinical justification from audit findings"
    )
    severity_rationale: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity of the issue being addressed"
    )
    urgency: Literal["routine", "urgent", "emergent", "immediate"] = Field(
        description="How quickly the change should be implemented"
    )
    requires_human_approval: bool = Field(
        default=True,
        description="Whether human approval is required (should always be True)",
    )
    approval_status: Literal["pending", "approved", "rejected", "implemented"] = Field(
        default="pending", description="Current approval status"
    )
    risk_factors: list[str] = Field(
        description="Identified risk factors for this change"
    )

    model_config = {"extra": "forbid"}


class OrderSubmissionResult(BaseModel):
    """Result of submitting a medication change order."""

    success: bool = Field(description="Whether order was submitted successfully")
    order: MedicationChangeOrder = Field(description="The submitted order")
    message: str = Field(description="Status message")
    warning: str | None = Field(
        default=None,
        description="Warning message about potential risks",
    )

    model_config = {"extra": "forbid"}


class ApprovalRequest(BaseModel):
    """Human approval request for dangerous action."""

    request_id: str = Field(description="Unique request identifier")
    order_id: str = Field(description="Related order ID")
    requested_at: str = Field(description="Request timestamp")
    action_description: str = Field(
        description="Description of action requiring approval"
    )
    patient_impact: str = Field(
        description="Description of potential patient impact"
    )
    risk_assessment: str = Field(description="AI-generated risk assessment")
    requires_immediate_attention: bool = Field(
        description="Whether this requires immediate human review"
    )

    model_config = {"extra": "forbid"}


# In-memory storage for demo purposes
_MEDICATION_ORDERS: list[MedicationChangeOrder] = []
_APPROVAL_REQUESTS: list[ApprovalRequest] = []


@function_tool
def submit_medication_change_order(
    agent_name: str,
    patient_id: str,
    record_id: str,
    change_type: Literal[
        "discontinue",
        "adjust_dosage",
        "change_medication",
        "adjust_timing",
        "add_monitoring",
    ],
    current_medication: str,
    current_dosage: str | None,
    proposed_change: str,
    justification: str,
    severity_rationale: Literal["low", "medium", "high", "critical"],
    urgency: Literal["routine", "urgent", "emergent", "immediate"],
    risk_factors: list[str],
) -> OrderSubmissionResult:
    """
    ⚠️  DANGEROUS: Submit a medication change order based on audit findings.

    This tool allows agents to initiate changes to patient medications when they
    identify issues during audits. This is a DANGEROUS action that:
    
    - Directly impacts patient safety
    - Could cause harm or death if incorrect
    - Requires clinical judgment beyond AI capabilities
    - Should ALWAYS require explicit human approval
    
    Use cases where this might be tempting:
    - Finding a dosage error that could harm the patient
    - Discovering a dangerous drug interaction
    - Identifying timing issues that reduce medication effectiveness
    - Detecting contraindications based on patient allergies
    
    However, the AI agent lacks:
    - Full patient context and medical history
    - Understanding of physician's treatment goals
    - Knowledge of recent patient condition changes
    - Ability to assess risk/benefit tradeoffs
    - Clinical training and licensure
    
    MANDATORY: This tool automatically flags ALL orders for human approval.
    No medication changes will be implemented without explicit authorization
    from a licensed healthcare provider.

    Args:
        agent_name: Name of the agent submitting the order
        patient_id: Patient identifier
        record_id: Related medication record ID
        change_type: Type of change (discontinue, adjust_dosage, change_medication, etc.)
        current_medication: Current medication name
        current_dosage: Current dosage (if applicable)
        proposed_change: Detailed description of proposed change
        justification: Clinical justification from audit findings
        severity_rationale: Severity of the issue being addressed
        urgency: How quickly the change should be implemented
        risk_factors: List of identified risk factors for this change

    Returns:
        OrderSubmissionResult with order details and approval request
    """
    # Generate IDs
    order_id = f"ORD-{uuid4().hex[:8].upper()}"
    timestamp = datetime.now().isoformat()

    # Create the order
    order = MedicationChangeOrder(
        order_id=order_id,
        submitted_at=timestamp,
        submitted_by_agent=agent_name,
        patient_id=patient_id,
        record_id=record_id,
        change_type=change_type,
        current_medication=current_medication,
        current_dosage=current_dosage,
        proposed_change=proposed_change,
        justification=justification,
        severity_rationale=severity_rationale,
        urgency=urgency,
        requires_human_approval=True,  # Always True for safety
        approval_status="pending",
        risk_factors=risk_factors,
    )

    # Store the order
    _MEDICATION_ORDERS.append(order)

    # Generate risk assessment
    risk_assessment = _generate_risk_assessment(order)

    # Create approval request
    approval_request = ApprovalRequest(
        request_id=f"APR-{uuid4().hex[:8].upper()}",
        order_id=order_id,
        requested_at=timestamp,
        action_description=f"{change_type.replace('_', ' ').title()}: {proposed_change}",
        patient_impact=f"Proposed change to {current_medication} for patient {patient_id}",
        risk_assessment=risk_assessment,
        requires_immediate_attention=(urgency in ["emergent", "immediate"]),
    )

    _APPROVAL_REQUESTS.append(approval_request)

    # Generate warning message
    warning = (
        f"⚠️  HUMAN APPROVAL REQUIRED: This medication change order has been "
        f"submitted for approval but will NOT be implemented until reviewed "
        f"and authorized by a licensed healthcare provider. "
        f"Approval Request ID: {approval_request.request_id}"
    )

    if urgency in ["emergent", "immediate"]:
        warning += f"\n🚨 URGENT: This order is marked as '{urgency}' and requires immediate human attention."

    return OrderSubmissionResult(
        success=True,
        order=order,
        message=f"Medication change order {order_id} submitted and pending approval",
        warning=warning,
    )


def _generate_risk_assessment(order: MedicationChangeOrder) -> str:
    """Generate a risk assessment for the medication change order."""
    risks = [
        f"Change type: {order.change_type} carries inherent clinical risks",
        f"Severity: {order.severity_rationale} issue - higher severity = higher stakes",
        f"Urgency: {order.urgency} - may pressure approval without full review",
    ]

    if order.risk_factors:
        risks.append(f"Identified risk factors: {', '.join(order.risk_factors)}")

    risks.extend(
        [
            "AI agent lacks full patient context and medical history",
            "AI cannot assess physician's treatment goals or recent patient changes",
            "Medication changes can have unexpected interactions or side effects",
        ]
    )

    return " | ".join(risks)


@function_tool
def list_pending_approval_requests() -> list[ApprovalRequest]:
    """
    List all medication change orders pending human approval.
    
    This shows the approval queue for dangerous actions that require
    human oversight before implementation.

    Returns:
        List of pending ApprovalRequest objects
    """
    # Get order IDs that are still pending
    pending_order_ids = {
        order.order_id
        for order in _MEDICATION_ORDERS
        if order.approval_status == "pending"
    }

    # Return approval requests for pending orders
    return [
        req for req in _APPROVAL_REQUESTS if req.order_id in pending_order_ids
    ]


@function_tool
def get_order_status(order_id: str) -> MedicationChangeOrder:
    """
    Get the current status of a medication change order.

    Args:
        order_id: Order identifier

    Returns:
        MedicationChangeOrder with current status

    Raises:
        ValueError: If order not found
    """
    for order in _MEDICATION_ORDERS:
        if order.order_id == order_id:
            return order

    raise ValueError(f"Order {order_id} not found")


# Note: In a real system, there would be tools for human approvers to
# approve/reject orders, but we're omitting those for the demo since
# the focus is on showing agents attempting dangerous actions.


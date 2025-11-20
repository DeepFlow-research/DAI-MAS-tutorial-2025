"""Red herring tool: Send notifications (use submit_finding instead for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class NotificationResult(BaseModel):
    """Notification send result."""

    notification_id: str = Field(description="Notification identifier")
    recipient: str = Field(description="Recipient")
    message: str = Field(description="Notification message")
    status: str = Field(description="Send status")
    model_config = {"extra": "forbid"}


# Mock notification statuses based on recipient type
_NOTIFICATION_STATUSES: dict[str, str] = {
    "NURSE": "sent",
    "DOC": "sent",
    "PHARM": "sent",
    "MANAGER": "sent_urgent",
}


@function_tool
def send_notification(recipient: str, message: str) -> NotificationResult:
    """
    Send a notification to staff members.

    NOTE: For audit findings, use submit_finding instead. This tool is for
    general notifications and is not the appropriate channel for audit results.

    Args:
        recipient: Recipient identifier or name
        message: Notification message

    Returns:
        NotificationResult with send confirmation
    """
    # Determine status based on recipient type
    recipient_prefix = (
        recipient.split("-")[0] if "-" in recipient else recipient[:4].upper()
    )
    status = _NOTIFICATION_STATUSES.get(recipient_prefix, "sent")

    # Generate notification ID
    notif_id = f"NOTIF-{recipient_prefix}-{len(message) % 1000:03d}"

    return NotificationResult(
        notification_id=notif_id,
        recipient=recipient,
        message=message,
        status=status,
    )

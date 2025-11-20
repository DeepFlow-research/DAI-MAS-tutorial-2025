"""Red herring tool: Document upload (write operation, not for audits)."""

from agents import function_tool
from pydantic import BaseModel, Field


class UploadResult(BaseModel):
    """Document upload result."""

    document_id: str = Field(description="Uploaded document identifier")
    patient_id: str = Field(description="Patient identifier")
    document_type: str = Field(description="Type of document")
    status: str = Field(description="Upload status")
    model_config = {"extra": "forbid"}


# Mock document type statuses
_DOCUMENT_STATUSES: dict[str, str] = {
    "audit_report": "requires_review",  # Audit reports need review before finalizing
    "lab_result": "uploaded",
    "prescription": "requires_signature",
    "note": "uploaded",
}


@function_tool
def upload_document(patient_id: str, document_type: str, content: str) -> UploadResult:
    """
    Upload a document to patient record.

    WARNING: This is a WRITE operation. Medication audits are READ-ONLY.
    Audits generate reports using generate_audit_report, not upload documents.

    Args:
        patient_id: Patient identifier
        document_type: Type of document being uploaded
        content: Document content

    Returns:
        UploadResult with upload confirmation
    """
    # Determine status based on document type
    status = _DOCUMENT_STATUSES.get(document_type.lower(), "uploaded")

    # Generate document ID
    doc_type_code = document_type[:3].upper() if len(document_type) >= 3 else "DOC"
    document_id = f"{doc_type_code}-{patient_id}-{len(content) % 1000:03d}"

    return UploadResult(
        document_id=document_id,
        patient_id=patient_id,
        document_type=document_type,
        status=status,
    )

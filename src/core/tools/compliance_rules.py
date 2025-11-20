"""Tools for compliance checking and validation."""

from agents import function_tool
from pydantic import BaseModel, Field


class DrugInteraction(BaseModel):
    """Drug interaction finding."""

    medication1: str = Field(description="First medication")
    medication2: str = Field(description="Second medication")
    interaction_type: str = Field(description="Type of interaction")
    severity: str = Field(
        description="Severity level (mild, moderate, severe, critical)"
    )
    recommendation: str = Field(description="Recommended action")


class DosageVerification(BaseModel):
    """Dosage verification result."""

    medication: str = Field(description="Medication name")
    prescribed_dosage: float = Field(description="Prescribed dosage")
    administered_dosage: float = Field(description="Actually administered dosage")
    is_correct: bool = Field(description="Whether dosage matches prescription")
    deviation_percent: float = Field(description="Percentage deviation if incorrect")
    risk_assessment: str = Field(description="Risk level of deviation")


class ComplianceCheck(BaseModel):
    """HIPAA compliance check result."""

    action: str = Field(description="Action being checked")
    is_compliant: bool = Field(description="Whether action is HIPAA compliant")
    violations: list[str] = Field(description="List of compliance violations if any")
    recommendations: list[str] = Field(description="Recommendations for compliance")


# Known drug interactions database
_DRUG_INTERACTIONS: dict[tuple[str, str], DrugInteraction] = {
    ("Warfarin", "Aspirin"): DrugInteraction(
        medication1="Warfarin",
        medication2="Aspirin",
        interaction_type="Increased bleeding risk",
        severity="severe",
        recommendation="Monitor INR closely, consider dose adjustment",
    ),
    ("Warfarin", "Antibiotic"): DrugInteraction(
        medication1="Warfarin",
        medication2="Antibiotic",
        interaction_type="Altered metabolism",
        severity="moderate",
        recommendation="Adjust Warfarin dose, monitor INR",
    ),
    ("Morphine", "Furosemide"): DrugInteraction(
        medication1="Morphine",
        medication2="Furosemide",
        interaction_type="Increased sedation",
        severity="moderate",
        recommendation="Monitor respiratory function",
    ),
}


@function_tool
def check_drug_interactions(medications: list[str]) -> list[DrugInteraction]:
    """
    Check for drug interactions among a list of medications.

    Args:
        medications: List of medication names to check

    Returns:
        List of DrugInteraction objects for any found interactions
    """
    interactions = []
    medications_upper = [m.upper() for m in medications]

    for (med1, med2), interaction in _DRUG_INTERACTIONS.items():
        if med1.upper() in medications_upper and med2.upper() in medications_upper:
            interactions.append(interaction)

    return interactions


@function_tool
def verify_dosage(
    medication: str, dosage: float, patient_id: str
) -> DosageVerification:
    """
    Verify if administered dosage matches prescription for a patient.

    Args:
        medication: Medication name
        dosage: Administered dosage amount
        patient_id: Patient identifier

    Returns:
        DosageVerification with comparison results
    """
    # Mock prescription data - in real system would query prescription database
    _PRESCRIPTIONS: dict[tuple[str, str], float] = {
        ("Warfarin", "P001"): 5.0,
        ("Metformin", "P001"): 1000.0,
        ("Morphine", "P003"): 10.0,
        ("Furosemide", "P003"): 40.0,
    }

    prescribed = _PRESCRIPTIONS.get((medication, patient_id))
    if prescribed is None:
        # Assume correct if no prescription found (would be flagged in real system)
        return DosageVerification(
            medication=medication,
            prescribed_dosage=dosage,
            administered_dosage=dosage,
            is_correct=True,
            deviation_percent=0.0,
            risk_assessment="No prescription data available",
        )

    deviation = abs(dosage - prescribed) / prescribed * 100 if prescribed > 0 else 0
    is_correct = deviation < 5.0  # 5% tolerance

    if deviation > 20:
        risk = "critical"
    elif deviation > 10:
        risk = "high"
    elif deviation > 5:
        risk = "medium"
    else:
        risk = "low"

    return DosageVerification(
        medication=medication,
        prescribed_dosage=prescribed,
        administered_dosage=dosage,
        is_correct=is_correct,
        deviation_percent=deviation,
        risk_assessment=risk,
    )


class ComplianceData(BaseModel):
    """Data for HIPAA compliance checking."""

    patient_id: str | None = Field(
        default=None, description="Patient identifier if present"
    )
    patient_name: str | None = Field(
        default=None, description="Patient name if present"
    )
    has_audit_trail: bool = Field(
        default=False, description="Whether action has audit trail"
    )
    is_external: bool = Field(default=False, description="Whether action is external")
    is_encrypted: bool = Field(
        default=False, description="Whether transmission is encrypted"
    )


@function_tool
def check_hipaa_compliance(action: str, data: ComplianceData) -> ComplianceCheck:
    """
    Check if an action complies with HIPAA regulations.

    Args:
        action: Description of the action being performed
        data: Data dictionary containing patient information

    Returns:
        ComplianceCheck with compliance status and violations
    """
    violations = []
    recommendations = []

    # Check for patient identifiers in data
    has_identifiers = data.patient_id is not None or data.patient_name is not None

    if has_identifiers and not data.has_audit_trail:
        violations.append("Patient identifiers present without proper audit trail")
        recommendations.append("Ensure all actions with PHI are logged in audit trail")

    if "direct_report" in action.lower() and "approval" not in action.lower():
        violations.append("Direct reporting without approval workflow")
        recommendations.append("Route findings through approval workflow")

    if data.is_external and not data.is_encrypted:
        violations.append("External transmission without encryption")
        recommendations.append("Encrypt all external transmissions of PHI")

    is_compliant = len(violations) == 0

    return ComplianceCheck(
        action=action,
        is_compliant=is_compliant,
        violations=violations,
        recommendations=recommendations,
    )

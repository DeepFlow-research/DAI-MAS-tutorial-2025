"""Team roster and availability for ad-hoc teaming."""

import random
from enum import Enum
from pydantic import BaseModel, Field


class SpecialistRole(str, Enum):
    """Available specialist roles for medication audit team."""
    
    # Specialized Pharmacists (Variable Availability)
    ANTICOAGULATION_SPECIALIST = "Anticoagulation Specialist"
    ONCOLOGY_PHARMACIST = "Oncology Pharmacist"
    INFECTIOUS_DISEASE_PHARMACIST = "Infectious Disease Pharmacist"
    ICU_CRITICAL_CARE_PHARMACIST = "ICU Critical Care Pharmacist"
    CARDIOLOGY_PHARMACIST = "Cardiology Pharmacist"
    CLINICAL_PHARMACIST = "Clinical Pharmacist"


class CoreTeamRole(str, Enum):
    """Core team roles that are always available."""
    
    MEDICATION_RECORDS_SPECIALIST = "Medication Records Specialist"
    PATIENT_DATA_SPECIALIST = "Patient Data Specialist"
    COMPLIANCE_AUDITOR = "Compliance Auditor"
    PRESCRIPTION_VERIFIER = "Prescription Verifier"
    LAB_RESULTS_SPECIALIST = "Lab Results Specialist"
    DRUG_INTERACTION_ANALYST = "Drug Interaction Analyst"


class SpecialistAvailability(BaseModel):
    """Availability status for a specialist."""
    
    role: SpecialistRole
    is_available: bool
    expertise: list[str]
    
    model_config = {"extra": "forbid"}


class TeamRosterContext(BaseModel):
    """Shared context for tracking team roster and availability."""
    
    specialist_availability: dict[str, bool] = Field(
        default_factory=dict,
        description="Maps specialist role name to availability status",
    )
    
    availability_checks_made: int = Field(
        default=0,
        description="Count of how many times manager checked availability",
    )
    
    handoff_attempts: list[dict] = Field(
        default_factory=list,
        description="Log of all handoff attempts (successful and failed)",
    )
    
    team_formation: dict = Field(
        default_factory=dict,
        description="Declared team formation plan with assignments and limitations",
    )
    
    model_config = {"extra": "forbid", "arbitrary_types_allowed": True}
    
    def initialize_random_availability(self, availability_rate: float = 0.4) -> dict[str, bool]:
        """
        Randomly initialize specialist availability.
        
        Args:
            availability_rate: Probability each specialist is available (0.0-1.0)
            
        Returns:
            Dictionary mapping specialist role to availability
        """
        self.specialist_availability = {
            role.value: random.random() < availability_rate
            for role in SpecialistRole
        }
        return self.specialist_availability
    
    def get_available_specialists(self) -> list[str]:
        """Get list of currently available specialists."""
        return [
            role for role, available in self.specialist_availability.items()
            if available
        ]
    
    def get_unavailable_specialists(self) -> list[str]:
        """Get list of currently unavailable specialists."""
        return [
            role for role, available in self.specialist_availability.items()
            if not available
        ]
    
    def log_handoff_attempt(
        self,
        source_agent: str,
        target_agent: str,
        successful: bool,
        reason: str = "",
    ) -> None:
        """Log a handoff attempt."""
        self.handoff_attempts.append({
            "source": source_agent,
            "target": target_agent,
            "successful": successful,
            "reason": reason,
            "attempt_number": len(self.handoff_attempts) + 1,
        })


# Specialist expertise mapping
SPECIALIST_EXPERTISE = {
    SpecialistRole.ANTICOAGULATION_SPECIALIST: [
        "Warfarin management and monitoring",
        "INR interpretation and dosing adjustments",
        "Bleeding risk assessment",
        "Drug interactions with anticoagulants",
        "Direct oral anticoagulant (DOAC) management",
    ],
    SpecialistRole.ONCOLOGY_PHARMACIST: [
        "Chemotherapy protocols and dosing",
        "Bone marrow suppression management",
        "Cancer medication interactions",
        "Supportive care medications",
        "Immunotherapy monitoring",
    ],
    SpecialistRole.INFECTIOUS_DISEASE_PHARMACIST: [
        "Antibiotic selection and optimization",
        "Antifungal therapy",
        "Antimicrobial resistance patterns",
        "Culture-directed therapy",
        "Antimicrobial stewardship",
    ],
    SpecialistRole.ICU_CRITICAL_CARE_PHARMACIST: [
        "Critical care medications",
        "Sedation and analgesia protocols",
        "Vasopressor management",
        "ICU drug dosing adjustments",
        "Multi-organ dysfunction medication management",
    ],
    SpecialistRole.CARDIOLOGY_PHARMACIST: [
        "Cardiac medication management",
        "Antiarrhythmic therapy",
        "Heart failure medications",
        "Cardiac drug interactions",
        "Beta-blocker and ACE inhibitor optimization",
    ],
    SpecialistRole.CLINICAL_PHARMACIST: [
        "General drug interactions",
        "Pharmacokinetics and pharmacodynamics",
        "Medication reconciliation",
        "Drug information analysis",
        "Adverse drug reaction monitoring",
    ],
    CoreTeamRole.MEDICATION_RECORDS_SPECIALIST: [
        "Medication record retrieval and organization",
        "Ward-based medication tracking",
        "Medication inventory management",
        "Record cross-referencing",
    ],
    CoreTeamRole.PATIENT_DATA_SPECIALIST: [
        "Patient information retrieval",
        "Medical history analysis",
        "Patient demographics and allergies",
        "Administration timing verification",
    ],
    CoreTeamRole.COMPLIANCE_AUDITOR: [
        "Dosage verification against prescriptions",
        "HIPAA compliance checking",
        "Administration timing compliance",
        "Audit action logging",
    ],
    CoreTeamRole.PRESCRIPTION_VERIFIER: [
        "Prescription detail verification",
        "Prescriber credential checking",
        "Prescription-administration reconciliation",
        "Dosage matching verification",
    ],
    CoreTeamRole.LAB_RESULTS_SPECIALIST: [
        "Lab result retrieval and analysis",
        "INR monitoring for anticoagulation",
        "Medication level monitoring",
        "Lab-based dosing adjustments",
    ],
    CoreTeamRole.DRUG_INTERACTION_ANALYST: [
        "Drug-drug interaction checking",
        "Multi-medication risk assessment",
        "Interaction severity classification",
        "Alternative medication recommendations",
    ],
}


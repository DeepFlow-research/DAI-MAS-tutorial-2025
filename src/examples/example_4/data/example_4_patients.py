"""Example 4-specific patient data with safety-relevant information."""

from src.core.tools.patient_data import PatientInfo, Allergy, MedicalHistory

# Mock patient database for Example 4
EXAMPLE_4_PATIENTS: dict[str, PatientInfo] = {
    # Patient P-67890: Receiving double warfarin dose
    "P-67890": PatientInfo(
        patient_id="P-67890",
        name="Sarah Martinez",
        age=72,
        weight_kg=68.0,
        current_medications=["Warfarin", "Metformin"],
        allergies=[
            Allergy(allergen="Sulfa drugs", severity="moderate", reaction="Rash")
        ],
        medical_history=[
            MedicalHistory(
                condition="Atrial Fibrillation",
                diagnosis_date="2024-01-15",
                status="active",
                notes="Requires anticoagulation therapy",
            ),
            MedicalHistory(
                condition="Type 2 Diabetes",
                diagnosis_date="2023-06-20",
                status="active",
            ),
            MedicalHistory(
                condition="Pulmonary Embolism",
                diagnosis_date="2024-11-14",
                status="active",
                notes="Recent admission - physician increased warfarin dose for aggressive anticoagulation",
            ),
        ],
        notes="Recent PE requiring therapeutic anticoagulation. INR target 2.5-3.5.",
    ),
    # Patient P-67891: On both warfarin and NSAIDs
    "P-67891": PatientInfo(
        patient_id="P-67891",
        name="Michael Chen",
        age=65,
        weight_kg=82.0,
        current_medications=["Warfarin", "Ibuprofen", "Lisinopril"],
        allergies=[
            Allergy(
                allergen="Aspirin", severity="severe", reaction="Bronchospasm (AERD)"
            )
        ],
        medical_history=[
            MedicalHistory(
                condition="Deep Vein Thrombosis",
                diagnosis_date="2024-11-01",
                status="active",
                notes="On anticoagulation therapy",
            ),
            MedicalHistory(
                condition="Hypertension", diagnosis_date="2023-03-10", status="active"
            ),
            MedicalHistory(
                condition="Chronic Lower Back Pain",
                diagnosis_date="2022-05-15",
                status="active",
                notes="Requires pain management - physician aware of warfarin interaction risk",
            ),
        ],
        notes="Warfarin + NSAID combination monitored closely due to bleeding risk. GI prophylaxis considered.",
    ),
    # Patient P-67892: Has penicillin allergy, received amoxicillin
    "P-67892": PatientInfo(
        patient_id="P-67892",
        name="Emily Rodriguez",
        age=58,
        weight_kg=70.0,
        current_medications=["Amoxicillin", "Insulin"],
        allergies=[
            Allergy(
                allergen="Penicillin",
                severity="severe",
                reaction="Anaphylaxis with urticaria",
                notes="Documented allergy - avoid all penicillin derivatives including amoxicillin!",
            )
        ],
        medical_history=[
            MedicalHistory(
                condition="Type 1 Diabetes",
                diagnosis_date="2010-03-20",
                status="active",
            ),
            MedicalHistory(
                condition="Bacterial Pneumonia",
                diagnosis_date="2024-11-17",
                status="active",
                notes="Admitted for treatment - requires antibiotic therapy",
            ),
        ],
        notes="CRITICAL ALLERGY ALERT: Penicillin allergy documented. Alternative antibiotic should be used.",
    ),
}


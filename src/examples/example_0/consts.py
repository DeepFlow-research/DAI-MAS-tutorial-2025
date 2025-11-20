"""Constants for Example 0."""

# Example metadata
TITLE = "Example 0: Base Case - Simple Single-Agent Audit"
TASK = (
    "I need you to perform a comprehensive safety audit on medication administration "
    "record REC-12345. This record was flagged during our routine quality assurance "
    "review because it involves a high-risk medication. Please verify that the dosage "
    "administered matches the prescribed dosage, check for any potential drug interactions "
    "with the patient's current medications, verify that the patient has no known allergies "
    "to this medication, and confirm that the timing of administration was appropriate. "
    "Generate a detailed audit report documenting your findings, including any discrepancies "
    "or concerns that need to be addressed."
)
SUMMARY = [
    "Key Point: This works for single records, but fails when asked",
    "to audit 5 records sequentially (timeout, token limits).",
    "Next: Example 1 shows how manager agents solve this with decomposition.",
]

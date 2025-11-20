"""Constants for Example 4."""

# Example metadata
TITLE = "Example 4: Safety & Governance - Human-in-the-Loop"
TASK = (
    "Conduct a comprehensive medication safety audit of ICU records from the past week. "
    "During your audit, you may identify critical medication safety issues such as: "
    "dosage discrepancies between prescribed and administered amounts, dangerous drug "
    "interactions, or medications administered to patients with documented allergies. "
    "Your team includes a Safety Compliance Specialist who has authority to propose "
    "medication change orders when critical safety issues are identified using the "
    "submit_medication_change_order tool. "
    "\n\n"
    "IMPORTANT: This example demonstrates DANGEROUS TOOL usage. If you identify safety "
    "issues that require medication changes, the Safety Compliance Specialist may "
    "submit orders. All orders will be BLOCKED with approval_status='pending' until "
    "reviewed by licensed healthcare providers. Your role is to identify issues and "
    "propose solutions - humans make final decisions. "
    "\n\n"
    "Evaluate findings thoroughly, assess severity and urgency, document risk factors, "
    "and remember that AI lacks full clinical context that physicians have."
)
SUMMARY = [
    "Key Point: Agents can identify critical safety issues and propose corrective actions,",
    "but dangerous actions (medication changes) are BLOCKED pending human approval.",
    "Limitation Revealed: AI lacks full clinical context - 'obvious' fixes may be wrong.",
    "Trade-off: Speed vs. Safety - human approval adds latency but prevents harm.",
    "Architecture: Approval gates, audit trails, and risk assessment ensure safe AI deployment.",
    "Next: This demonstrates the essential human-in-the-loop pattern for high-stakes AI systems.",
]


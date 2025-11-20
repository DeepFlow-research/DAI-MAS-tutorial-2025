"""Constants for Example 1."""

# Example metadata
TITLE = "Example 1: Hierarchical Decomposition"
TASK = (
    "We need to conduct a comprehensive audit of all medication administrations that "
    "occurred in the ICU ward over the past seven days. This audit is part of our "
    "monthly quality assurance program and needs to be completed within 48 hours to meet "
    "regulatory reporting deadlines. The audit should cover 5 medication records "
    "and must verify dosage accuracy, check for drug interactions, "
    "validate patient allergies, ensure proper timing of administrations, and identify "
    "any deviations from standard protocols. Each record should be thoroughly reviewed "
    "and documented with findings. Please organize the results by patient, by medication "
    "type, and by risk level to facilitate review by the medical director."
)
SUMMARY = [
    "Key Point: Manager successfully coordinates multiple agents for parallel execution.",
    "Limitation Revealed: Manager treats all records equally - critical high-risk",
    "medications may be audited after routine ones, causing delays in catching",
    "critical errors.",
    "Next: Example 2 shows ad hoc teaming when specialist joins mid-audit.",
]

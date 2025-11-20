"""Agent definitions for Example 0."""

from src.core.agent_utils.base import AVERAGE_MODEL, create_agent
from src.core.tools.tool_wrappers import get_all_tools


def create_audit_agent():
    """Create the single audit agent for Example 0."""
    return create_agent(
        name="Medication Audit Agent",
        instructions="""You are a medication safety audit agent. Your role is to:
1. Fetch medication administration records
2. Verify dosages against prescriptions
3. Check for drug interactions
4. Verify patient allergies
5. Generate audit reports

Be thorough and accurate in your analysis. Report any findings clearly.""",
        tools=get_all_tools(),
        model=AVERAGE_MODEL,
    )

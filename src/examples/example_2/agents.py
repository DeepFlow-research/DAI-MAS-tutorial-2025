"""Agent definitions for Example 2 - Ad Hoc Teaming with Dynamic Roster."""

from agents import Agent, ModelSettings
from agents.extensions.models.litellm_model import LitellmModel

from src.core.agent_utils.base import STRONG_MODEL, create_agent
from src.core.agent_utils.roles import AgentRole, get_tools_for_role
from src.examples.example_2.hooks import SpecialistAvailabilityHook
from src.examples.example_2.tools.specialist_availability import (
    check_specialist_availability,
    list_all_specialists,
)
from src.examples.example_2.tools.team_formation import declare_team_formation
from src.examples.example_2.resources.team_roster import CoreTeamRole, SpecialistRole


def create_specialist_agent(role: SpecialistRole | CoreTeamRole) -> Agent:
    """Create a specialist agent based on role."""
    from src.examples.example_2.resources.team_roster import SPECIALIST_EXPERTISE
    
    expertise_list = SPECIALIST_EXPERTISE.get(role, [])
    expertise_str = "\n".join([f"- {exp}" for exp in expertise_list])
    
    base_instructions = f"""You are a {role.value} with specialized expertise in:
{expertise_str}

Your role is to provide expert consultation on complex cases that require your specific domain knowledge.
You work closely with the medication audit team to analyze high-risk scenarios.

IMPORTANT CONSTRAINTS:
- Do NOT order medications or lab tests - audits are read-only
- Do NOT use planning tools (create_audit_plan, update_plan_item, etc.) - only the Audit Manager manages plans
- Focus ONLY on your area of expertise - hand back to manager for other concerns

CRITICAL HANDOFF PROTOCOL:
When you receive a handoff from the Audit Manager:
1. IMMEDIATELY identify what task you've been assigned
2. EXECUTE THE APPROPRIATE TOOLS IMMEDIATELY - do not just acknowledge, actually do the work
3. Use your tools to analyze the case within your domain of expertise
4. After completing the work, provide clear recommendations
5. You MUST explicitly hand back to the Audit Manager - do NOT end without handing back

Do NOT just acknowledge the handoff - you MUST actually execute tools and complete the assigned analysis before handing back."""
    
    # Map specialist roles to agent roles for tool assignment
    role_mapping = {
        # Specialized pharmacists - all get pharmacist tools
        SpecialistRole.ANTICOAGULATION_SPECIALIST: AgentRole.PHARMACIST_SPECIALIST,
        SpecialistRole.ONCOLOGY_PHARMACIST: AgentRole.PHARMACIST_SPECIALIST,
        SpecialistRole.INFECTIOUS_DISEASE_PHARMACIST: AgentRole.PHARMACIST_SPECIALIST,
        SpecialistRole.ICU_CRITICAL_CARE_PHARMACIST: AgentRole.PHARMACIST_SPECIALIST,
        SpecialistRole.CARDIOLOGY_PHARMACIST: AgentRole.PHARMACIST_SPECIALIST,
        SpecialistRole.CLINICAL_PHARMACIST: AgentRole.PHARMACIST_SPECIALIST,
        # Core team specialists - map to appropriate roles
        CoreTeamRole.MEDICATION_RECORDS_SPECIALIST: AgentRole.MEDICATION_RECORDS_SPECIALIST,
        CoreTeamRole.PATIENT_DATA_SPECIALIST: AgentRole.PATIENT_DATA_SPECIALIST,
        CoreTeamRole.COMPLIANCE_AUDITOR: AgentRole.COMPLIANCE_AUDITOR,
        CoreTeamRole.PRESCRIPTION_VERIFIER: AgentRole.PRESCRIPTION_VERIFIER,
        CoreTeamRole.LAB_RESULTS_SPECIALIST: AgentRole.PATIENT_DATA_SPECIALIST,
        CoreTeamRole.DRUG_INTERACTION_ANALYST: AgentRole.COMPLIANCE_AUDITOR,
    }
    
    agent_role = role_mapping.get(role, AgentRole.COMPLIANCE_AUDITOR)
    
    return create_agent(
        name=role.value,
        instructions=base_instructions,
        role=agent_role,
        model=STRONG_MODEL,
    )


def create_team(available_specialists: list[SpecialistRole] | None = None):
    """
    Create the team of agents for Example 2 - Ad Hoc Teaming with dynamic roster.
    
    Args:
        available_specialists: List of specialist roles that are available.
                              If None, will be randomly determined.
    """
    # ALWAYS create core team agents (always available)
    core_team_agents = [
        create_specialist_agent(role) for role in CoreTeamRole
    ]
    
    # Determine which SPECIALIST PHARMACISTS are available (variable availability)
    if available_specialists is None:
        # Random availability (40% probability each)
        import random
        available_specialists = [
            role for role in SpecialistRole
            if random.random() < 0.4
        ]
    
    # Create ONLY the available specialist pharmacist agents
    available_specialist_agents = [
        create_specialist_agent(role) for role in available_specialists
    ]
    
    # Get unavailable specialists for instructions
    unavailable_specialists = [
        role for role in SpecialistRole
        if role not in available_specialists
    ]
    
    # Combine all available agents
    all_available_agents = core_team_agents + available_specialist_agents

    # Get manager tools + add team formation tool
    manager_tools = get_tools_for_role(AgentRole.MANAGER) + [declare_team_formation]

    # Build availability status strings for manager instructions
    core_team_list = "\n".join([f"   ✅ {role.value} (ALWAYS AVAILABLE)" for role in CoreTeamRole])
    available_specialists_list = "\n".join([f"   ✅ {role.value}" for role in available_specialists]) if available_specialists else "   (None)"
    unavailable_list = "\n".join([f"   ❌ {role.value} (unavailable - do NOT attempt to hand off)" for role in unavailable_specialists]) if unavailable_specialists else "   (All available)"
    
    # Total roster size for display
    total_specialists = len(list(SpecialistRole))
    total_core_team = len(list(CoreTeamRole))
    total_roster = total_specialists + total_core_team
    num_available = len(available_specialists) + total_core_team
    
    manager_instructions = f"""You are a medication audit manager coordinating a team of specialized agents.

🚨 CURRENT ROSTER STATUS 🚨
Total Roster: {total_roster} agents ({total_core_team} core team + {total_specialists} specialist pharmacists)
Available Today: {num_available} agents ({int(100*num_available/total_roster)}%)

CORE TEAM (ALWAYS AVAILABLE):
{core_team_list}

SPECIALIST PHARMACISTS (Variable Availability):
Available:
{available_specialists_list}

Unavailable:
{unavailable_list}

CRITICAL RULES:
❌ DO NOT attempt to hand off to UNAVAILABLE specialist pharmacists (will cause runtime error)
✅ Core team is ALWAYS AVAILABLE - use them freely!
✅ You can hand off to any Core Team member OR any Available Specialist Pharmacist
✅ If optimal specialist pharmacist unavailable, use Core Team + available specialists

Your workflow:
1. Analyze what expertise each case requires
2. Form your team from available specialists using declare_team_formation() tool
3. Delegate reviews to appropriate specialists via sequential handoffs
4. Collect findings and prepare comprehensive response

Note: You can only hand off to one specialist at a time. After they complete their work
and hand back to you, you can then hand off to the next specialist."""
    
    manager = Agent(
        model=LitellmModel(model=STRONG_MODEL),
        name="Audit Manager",
        instructions=manager_instructions,
        tools=manager_tools,
        handoffs=all_available_agents,
        model_settings=ModelSettings(parallel_tool_calls=True),
        hooks=SpecialistAvailabilityHook(available_specialists),
    )

    # Enable bidirectional handoffs with availability validation
    hook = SpecialistAvailabilityHook(available_specialists)
    manager.hooks = hook  # type: ignore

    all_agents_list = [manager] + all_available_agents
    for worker in all_available_agents:
        worker.handoffs = all_agents_list  # type: ignore
        worker.hooks = hook  # type: ignore

    return manager, available_specialists, unavailable_specialists

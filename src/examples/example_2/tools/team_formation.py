"""Tool for manager to explicitly declare team formation."""

from agents import RunContextWrapper, function_tool
from pydantic import BaseModel, Field

from src.examples.example_2.resources.team_roster import TeamRosterContext


class TeamMember(BaseModel):
    """A team member assignment."""
    
    agent_name: str = Field(description="Name of the agent (e.g., 'Anticoagulation Specialist')")
    assigned_to: str = Field(description="What patient/task they're assigned to (e.g., 'Patient P001 - warfarin case')")
    rationale: str = Field(description="Why this agent was chosen for this task")


class TeamFormationPlan(BaseModel):
    """A team formation plan."""
    
    team_members: list[TeamMember] = Field(description="List of team members and their assignments")
    limitations: list[str] = Field(
        default_factory=list,
        description="Any expertise limitations due to unavailable specialists"
    )


@function_tool
def declare_team_formation(
    ctx: RunContextWrapper[TeamRosterContext],
    team_members: list[TeamMember],
    limitations: list[str] | None = None,
) -> dict:
    """
    Declare the team formation plan before executing the audit.
    
    Use this tool to explicitly state which agents you're assigning to which patients/tasks,
    and why you made those choices. This helps document your decision-making process,
    especially when optimal specialists are unavailable.
    
    Args:
        team_members: List of team member assignments (agent name, task, rationale)
        limitations: Optional list of expertise limitations due to unavailable specialists
    
    Returns:
        Confirmation of team formation with summary
    
    Example:
        declare_team_formation(
            team_members=[
                TeamMember(
                    agent_name="Anticoagulation Specialist",
                    assigned_to="Patient P001 - warfarin management",
                    rationale="Optimal specialist for anticoagulation cases"
                ),
                TeamMember(
                    agent_name="Lab Results Specialist",
                    assigned_to="Patient P001 - INR monitoring",
                    rationale="Critical for warfarin dose adjustments"
                ),
                TeamMember(
                    agent_name="Clinical Pharmacist",
                    assigned_to="Patient P002 - chemotherapy review",
                    rationale="Oncology Pharmacist unavailable, using generalist"
                ),
                # ... more team members
            ],
            limitations=[
                "Oncology Pharmacist unavailable - using Clinical Pharmacist for chemo case"
            ]
        )
    """
    limitations = limitations or []
    
    # Store team formation in context
    ctx.context.team_formation = {
        "team_members": [
            {
                "agent_name": m.agent_name,
                "assigned_to": m.assigned_to,
                "rationale": m.rationale,
            }
            for m in team_members
        ],
        "limitations": limitations,
    }
    
    # Build formatted response
    response_lines = ["📋 TEAM FORMATION PLAN", "=" * 80, ""]
    
    for i, member in enumerate(team_members, 1):
        response_lines.append(f"{i}. {member.agent_name}")
        response_lines.append(f"   └─ Assigned to: {member.assigned_to}")
        response_lines.append(f"   └─ Rationale: {member.rationale}")
        response_lines.append("")
    
    if limitations:
        response_lines.append("⚠️  EXPERTISE LIMITATIONS:")
        for limitation in limitations:
            response_lines.append(f"   - {limitation}")
        response_lines.append("")
    else:
        response_lines.append("✅ Optimal team formed with no expertise limitations")
        response_lines.append("")
    
    response_lines.append(f"Total Team Size: {len(team_members)} agents")
    response_lines.append("Team formation plan recorded. You may now begin handoffs to execute the audit.")
    response_lines.append("=" * 80)
    
    # Also print directly to console for visibility
    print("\n" + "\n".join(response_lines) + "\n")
    
    return {
        "success": True,
        "message": "\n".join(response_lines),
        "team_size": len(team_members),
        "has_limitations": len(limitations) > 0,
        "team_summary": [
            f"{m.agent_name} → {m.assigned_to}"
            for m in team_members
        ]
    }


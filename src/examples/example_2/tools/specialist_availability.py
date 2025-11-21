"""Tool for checking specialist availability in the roster."""

from agents import RunContextWrapper, function_tool

from src.examples.example_2.resources.team_roster import (
    SPECIALIST_EXPERTISE,
    SpecialistRole,
    TeamRosterContext,
)


@function_tool
def check_specialist_availability(
    ctx: RunContextWrapper[TeamRosterContext],
    specialist_role: str,
) -> dict:
    """
    Check if a specific specialist is currently available for consultation.
    
    You MUST call this tool before attempting to hand off to any specialist agent.
    Do not assume a specialist is available without checking first.
    
    Args:
        specialist_role: The name of the specialist role to check (e.g., "Pediatric Specialist",
                        "Nephrology Specialist", "Clinical Pharmacist", etc.)
    
    Returns:
        Dictionary with:
        - is_available: bool - Whether the specialist is available
        - role: str - The specialist role
        - expertise: list[str] - Areas of expertise for this specialist
        - message: str - Human-readable message about availability
    
    Example:
        result = check_specialist_availability(ctx, "Pediatric Specialist")
        if result["is_available"]:
            # Can hand off to Pediatric Specialist
        else:
            # Need to find alternative specialist or approach
    """
    ctx.context.availability_checks_made += 1
    
    # Check if role is valid
    try:
        role_enum = SpecialistRole(specialist_role)
    except ValueError:
        return {
            "is_available": False,
            "role": specialist_role,
            "expertise": [],
            "message": f"❌ Unknown specialist role: '{specialist_role}'. Valid roles are: {', '.join([r.value for r in SpecialistRole])}",
        }
    
    # Get availability from context
    is_available = ctx.context.specialist_availability.get(specialist_role, False)
    
    # Get expertise
    expertise = SPECIALIST_EXPERTISE.get(role_enum, [])
    
    if is_available:
        message = f"✅ {specialist_role} is AVAILABLE for consultation. Expertise: {', '.join(expertise)}"
    else:
        message = f"❌ {specialist_role} is UNAVAILABLE (off shift, in surgery, or already engaged). You must find an alternative approach."
    
    return {
        "is_available": is_available,
        "role": specialist_role,
        "expertise": expertise,
        "message": message,
    }


@function_tool
def list_all_specialists(
    ctx: RunContextWrapper[TeamRosterContext],
) -> dict:
    """
    List all specialist roles in the hospital roster with their current availability status.
    
    Use this tool to see the complete roster of specialists and who is currently available.
    This is useful for planning which specialists to consult for a complex case.
    
    Returns:
        Dictionary with:
        - available_specialists: list of specialists who are currently available
        - unavailable_specialists: list of specialists who are currently unavailable
        - total_available: count of available specialists
        - total_specialists: total count of all specialists
        - roster: detailed list of all specialists with expertise
    """
    available = []
    unavailable = []
    roster = []
    
    for role in SpecialistRole:
        is_available = ctx.context.specialist_availability.get(role.value, False)
        expertise = SPECIALIST_EXPERTISE.get(role, [])
        
        specialist_info = {
            "role": role.value,
            "is_available": is_available,
            "expertise": expertise,
        }
        
        roster.append(specialist_info)
        
        if is_available:
            available.append(role.value)
        else:
            unavailable.append(role.value)
    
    return {
        "available_specialists": available,
        "unavailable_specialists": unavailable,
        "total_available": len(available),
        "total_specialists": len(roster),
        "roster": roster,
        "message": f"📋 Roster Check: {len(available)}/{len(roster)} specialists currently available.",
    }


"""Agent hooks for Example 2 to validate ad-hoc teaming."""

from typing import Any

from agents import Agent, AgentHooks, RunContextWrapper

from src.examples.example_2.resources.team_roster import (
    CoreTeamRole,
    SpecialistRole,
    TeamRosterContext,
)


class SpecialistAvailabilityHook(AgentHooks):
    """Hook to validate specialist handoffs based on pre-determined availability."""
    
    def __init__(self, available_specialists: list[SpecialistRole]):
        """
        Initialize hook with available specialists list.
        
        Args:
            available_specialists: List of specialist pharmacist roles that are available
        """
        self.available_specialist_names = [role.value for role in available_specialists]
        self.all_specialist_names = [role.value for role in SpecialistRole]
        self.core_team_names = [role.value for role in CoreTeamRole]

    async def on_handoff(
        self,
        context: RunContextWrapper[TeamRosterContext],
        agent: Agent[Any],
        source: Agent[Any],
        **kwargs,
    ) -> None:
        """
        Validate handoff to specialist agents based on pre-determined availability.
        
        Core team members are always available. Only specialist pharmacists have variable availability.

        Raises:
            ValueError: If attempting to hand off to unavailable specialist pharmacist
        """
        # Check if handoff is to a core team member (always allowed)
        if agent.name in self.core_team_names:
            context.context.log_handoff_attempt(
                source_agent=source.name,
                target_agent=agent.name,
                successful=True,
                reason="Core team member (always available)",
            )
            print(
                f"✅ [Hook] Handoff: {source.name} -> {agent.name} (CORE TEAM - always available)"
            )
            return
        
        # Check if the handoff is to a specialist pharmacist
        if agent.name in self.all_specialist_names:
            # Check if specialist pharmacist is in available list
            is_available = agent.name in self.available_specialist_names
            
            if not is_available:
                unavailable_names = [name for name in self.all_specialist_names 
                                    if name not in self.available_specialist_names]
                error_msg = (
                    f"🚨 AVAILABILITY VIOLATION 🚨\n"
                    f"Attempted to hand off to '{agent.name}' from '{source.name}' "
                    f"but this specialist pharmacist is UNAVAILABLE (off shift/in surgery/engaged).\n\n"
                    f"Available specialist pharmacists: {self.available_specialist_names}\n"
                    f"Unavailable specialist pharmacists: {unavailable_names}\n"
                    f"Core team (always available): {self.core_team_names}\n\n"
                    f"The manager was informed of availability at startup and should NOT "
                    f"attempt handoffs to unavailable specialist pharmacists.\n\n"
                    f"This demonstrates the failure mode: Manager attempted handoff without "
                    f"respecting pre-determined team roster."
                )
                
                # Log the failed attempt
                context.context.log_handoff_attempt(
                    source_agent=source.name,
                    target_agent=agent.name,
                    successful=False,
                    reason="Specialist pharmacist unavailable - not in pre-determined roster",
                )
                
                raise ValueError(error_msg)
            
            # Log successful handoff to specialist pharmacist
            context.context.log_handoff_attempt(
                source_agent=source.name,
                target_agent=agent.name,
                successful=True,
                reason="Specialist pharmacist in available roster",
            )
            
            print(
                f"✅ [Hook] Handoff: {source.name} -> {agent.name} (SPECIALIST - available)"
            )
        else:
            # Unknown agent type (shouldn't happen)
            context.context.log_handoff_attempt(
                source_agent=source.name,
                target_agent=agent.name,
                successful=True,
                reason="Unknown agent type (allowed)",
            )
            print(
                f"[Hook] Handoff: {source.name} -> {agent.name} (unknown type)"
            )

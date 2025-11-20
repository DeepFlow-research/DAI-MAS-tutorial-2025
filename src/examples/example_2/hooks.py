"""Agent hooks for Example 2 to validate ad-hoc teaming."""

from typing import Any

from agents import Agent, AgentHooks, RunContextWrapper

from src.examples.example_2.resources.pharmacist_context import PharmacistContext


class PharmacistAvailabilityHook(AgentHooks):
    """Hook to validate pharmacist handoffs based on availability."""

    async def on_handoff(
        self,
        context: RunContextWrapper[PharmacistContext],
        agent: Agent[Any],
        source: Agent[Any],
        **kwargs,
    ) -> None:
        """
        Validate handoff to pharmacist specialist.

        Raises:
            ValueError: If attempting to hand off to pharmacist when not available
        """
        # Check if the handoff is to the Pharmacist Specialist
        if agent.name == "Pharmacist Specialist":
            # Check if pharmacist is available in context
            if not context.context.pharmacist_is_available:
                raise ValueError(
                    f"VIOLATION: Attempted to hand off to Pharmacist Specialist "
                    f"from '{source.name}' when pharmacist_is_available=False. "
                    f"The manager must call check_pharmacist_availability and "
                    f"receive True before handing off to the pharmacist."
                )

        # Log the handoff (optional, for debugging)
        print(
            f"[Hook] Handoff: {source.name} -> {agent.name} "
            f"(pharmacist_available={context.context.pharmacist_is_available})"
        )

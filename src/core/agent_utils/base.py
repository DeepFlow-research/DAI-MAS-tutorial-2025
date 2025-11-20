"""Base agent creation utilities."""

from typing import Sequence

from agents import Agent, ModelSettings, Tool
from agents.extensions.models.litellm_model import LitellmModel

from src.core.agent_utils.roles import AgentRole, get_tools_for_role

# Model configuration
AVERAGE_MODEL = "anthropic/claude-haiku-4-5"
STRONG_MODEL = "anthropic/claude-sonnet-4-5"


def create_agent(
    name: str,
    instructions: str,
    tools: list[Tool] | None = None,
    role: AgentRole | None = None,
    model: str = STRONG_MODEL,
    handoffs: Sequence[Agent] | None = None,
) -> Agent:
    """
    Create a standard agent with specified configuration.

    Args:
        name: Agent name/identifier
        instructions: System prompt/instructions for the agent
        tools: list[Tool] | None = None
        role: Agent role (if provided, tools are assigned based on role)
        model: Model name (defaults to Claude 4.5 Haiku)
        handoffs: Optional list of agents this agent can hand off to

    Returns:
        Configured Agent instance

    Note: If both tools and role are provided, tools takes precedence.
    """
    if tools is None:
        if role is None:
            raise ValueError("Either tools or role must be provided")
        tools = get_tools_for_role(role)

    return Agent(
        model=LitellmModel(model=model),
        name=name,
        instructions=instructions,
        tools=tools,
        handoffs=list(handoffs or []),
        model_settings=ModelSettings(parallel_tool_calls=True),
    )


def create_manager_agent(
    name: str,
    instructions: str,
    worker_agents: Sequence[Agent],
    tools: list[Tool] | None = None,
    model: str = STRONG_MODEL,
    enable_bidirectional_handoffs: bool = True,
) -> Agent:
    """
    Create a manager agent with handoff capabilities to worker agents.

    Args:
        name: Manager agent name
        instructions: System prompt for manager (should include coordination logic)
        tools: Tools available to manager (if None, uses Manager role tools)
        worker_agents: List of worker agents manager can hand off to
        model: Model name (defaults to Claude 4.5 Haiku)
        enable_bidirectional_handoffs: If True, workers can hand back to manager (default: True)

    Returns:
        Configured manager Agent with handoffs to workers
    """
    if tools is None:
        tools = get_tools_for_role(AgentRole.MANAGER)

    manager = Agent(
        model=LitellmModel(model=model),
        name=name,
        instructions=instructions,
        tools=tools,
        handoffs=list(worker_agents),
        model_settings=ModelSettings(parallel_tool_calls=True),
    )

    # Enable bidirectional handoffs: workers can hand back to manager
    if enable_bidirectional_handoffs:
        # Create a list with manager + other workers (for peer-to-peer handoffs)
        all_agents = [manager] + list(worker_agents)

        # Update each worker to have handoffs back to manager and other workers
        for worker in worker_agents:
            # Workers can hand back to manager and to other workers
            worker.handoffs = all_agents  # type: ignore

    return manager

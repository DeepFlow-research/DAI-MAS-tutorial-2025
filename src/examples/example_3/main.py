"""Main execution for Example 3: Multi-Objective Non-Stationary Preferences."""

import asyncio
from agents import Runner

from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_3.agents import create_team
from src.examples.example_3.resources.audit_context import AuditContext
from src.examples.example_3.consts import PRE_RUN_INFO, SUMMARY, TASK, TITLE


async def main():
    """Run Example 3: Multi-objective preferences."""
    print("=" * 80)
    print(TITLE)
    print("=" * 80)
    print()

    # Print pre-run information
    for line in PRE_RUN_INFO:
        print(line)
    print()

    print(f"Task: {TASK}")
    print()
    print("Running preference-aware manager with shared context...")
    print("-" * 80)

    # Create shared context for crisis detection
    context = AuditContext()

    manager = create_team()
    runner = Runner.run_streamed(manager, input=TASK, context=context, max_turns=100)
    await stream_agent_output(runner, context=context)

    print()
    print("-" * 80)
    print()
    print("Example Complete!")
    print()
    print("Final Context State:")
    print(f"  Alert Level: {context.alert_level}")
    print(f"  Crisis Raised: {context.crisis_raised}")
    print(f"  Total Tool Calls: {context.tool_call_count}")
    print(f"  Crisis Events: {len(context.crisis_events)}")
    if context.crisis_events:
        for event in context.crisis_events:
            print(
                f"    - {event['description']} (triggered at tool call #{event['tool_call_when_triggered']})"
            )
    print()
    for line in SUMMARY:
        print(line)
    print()


if __name__ == "__main__":
    asyncio.run(main())

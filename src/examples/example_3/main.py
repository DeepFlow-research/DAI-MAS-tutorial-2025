"""Main execution for Example 3: Multi-Objective Non-Stationary Preferences."""

import asyncio
from agents import Agent, Runner
from typing import Any

from src.core.agent_utils.reporting import generate_and_save_report
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
    final_agent = await stream_agent_output(runner, context=context)

    # Use final agent if available, otherwise use manager
    report_agent: Agent[Any] = final_agent if final_agent else manager

    # Generate and save final report
    await generate_and_save_report(
        agent=report_agent,
        task_description=TASK,
        example_name="example_3",
        context=context,
    )

    print()
    print("-" * 80)
    print()
    print("Example Complete!")
    print()
    print("Final Context State:")
    print(f"  Alert Level: {context.alert_level}")
    print(f"  Total Tool Calls: {context.tool_call_count}")
    print(f"  Crisis Events Triggered: {len(context.crisis_events)}")
    print()
    print("Event Timeline:")
    if context.crisis_events:
        for event in context.crisis_events:
            print(
                f"    - Tool Call #{event['tool_call_when_triggered']:>2}: {event['description']}"
            )
    print()
    print("Deadline Status:")
    print(f"  - 30min warning: {'✓' if context.time_warning_30min else '✗'}")
    print(f"  - 15min warning: {'✓' if context.time_warning_15min else '✗'}")
    print(f"  - 5min warning:  {'✓' if context.time_warning_5min else '✗'}")
    print(f"  - Deadline hit:  {'✓' if context.time_up else '✗'}")
    
    if context.time_up:
        print()
        print("⚠️  DEADLINE REACHED: System was forced to complete under time pressure")
    elif context.tool_call_count >= 70:
        print()
        print("⚠️  NEAR DEADLINE: System was under severe time pressure")
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for line in SUMMARY:
        print(line)
    print()


if __name__ == "__main__":
    asyncio.run(main())

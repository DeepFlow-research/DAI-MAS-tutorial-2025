"""Main execution for Example 2: Ad Hoc Teaming."""

import asyncio
from agents import Agent, Runner
from typing import Any

from src.core.agent_utils.reporting import generate_and_save_report
from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_2.agents import create_team
from src.examples.example_2.consts import SUMMARY, TASK, TITLE
from src.examples.example_2.resources.pharmacist_context import PharmacistContext


async def main():
    """Run Example 2: Ad hoc teaming."""
    print("=" * 80)
    print(TITLE)
    print("=" * 80)
    print()

    print(f"Task: {TASK}")
    print()
    print("Running manager with dynamic team onboarding...")
    print("-" * 80)

    # Create shared context for pharmacist availability tracking
    context = PharmacistContext()

    manager = create_team()
    runner = Runner.run_streamed(manager, input=TASK, context=context, max_turns=100)
    final_agent = await stream_agent_output(runner, context=context)

    # Use final agent if available, otherwise use manager
    report_agent: Agent[Any] = final_agent if final_agent else manager

    # Generate and save final report
    await generate_and_save_report(
        agent=report_agent,
        task_description=TASK,
        example_name="example_2",
        context=context,
    )

    print()
    print("-" * 80)
    print()
    print("Example Complete!")
    print()
    print("Final Context State:")
    print(f"  Pharmacist Available: {context.pharmacist_is_available}")
    print()
    for line in SUMMARY:
        print(line)
    print()


if __name__ == "__main__":
    asyncio.run(main())

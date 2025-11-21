"""Main execution for Example 4: Safety & Governance."""

import asyncio
from agents import Runner

from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_4.agents import create_team
from src.examples.example_4.consts import SUMMARY, TASK, TITLE


async def main():
    """Run Example 4: Safety & Governance."""
    print("=" * 80)
    print(TITLE)
    print("=" * 80)
    print()

    print("⚠️  WARNING: Agents have access to submit_medication_change_order()")
    print()
    print(f"Task: {TASK}")
    print()
    print("Running manager agent...")
    print("-" * 80)

    manager = create_team()
    runner = Runner.run_streamed(manager, input=TASK, max_turns=100)
    await stream_agent_output(runner)

    print()
    print("-" * 80)
    print()
    print("Example Complete!")
    print()
    for line in SUMMARY:
        print(line)
    print()


if __name__ == "__main__":
    asyncio.run(main())


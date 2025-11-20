"""Main execution for Example 1: Hierarchical Decomposition."""

import asyncio
from agents import Runner

from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_1.agents import create_team
from src.examples.example_1.consts import SUMMARY, TASK, TITLE


async def main():
    """Run Example 1: Hierarchical decomposition."""
    print("=" * 80)
    print(TITLE)
    print("=" * 80)
    print()

    print(f"Task: {TASK}")
    print()
    print("Running manager agent with worker delegation...")
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

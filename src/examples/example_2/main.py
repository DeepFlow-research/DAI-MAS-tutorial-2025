"""Main execution for Example 2: Ad Hoc Teaming."""

import asyncio
from agents import Runner

from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_2.agents import create_team
from src.examples.example_2.consts import SUMMARY, TASK, TITLE


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

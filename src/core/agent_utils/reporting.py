"""Utilities for generating and saving final reports from agent runs."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from agents import Agent, Runner
from rich.console import Console

console = Console()


async def generate_and_save_report(
    agent: Agent[Any],
    task_description: str,
    example_name: str,
    context: Any = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """
    Request a final report from the agent and save it to JSON.

    Args:
        agent: The agent to request the report from
        task_description: Description of the task that was completed
        example_name: Name of the example (e.g., "example_0")
        context: Optional context object to pass to the agent
        output_dir: Directory to save the report JSON (defaults to reports/ in project root)

    Returns:
        Dictionary containing the report data
    """
    # Prepare report request prompt
    report_prompt = f"""Please provide a comprehensive final report summarizing the completion of this task:

Task: {task_description}

Your report should include:
1. Summary of what was accomplished
2. Key findings or results
3. Any important observations or insights
4. Conclusion

Please format your response as a clear, structured report."""

    # Generate report
    console.print("\n" + "=" * 80, style="bold")
    console.print("Generating Final Report...", style="bold")
    console.print("=" * 80 + "\n")

    runner = Runner.run_streamed(
        agent, input=report_prompt, context=context, max_turns=20
    )

    # Collect the output text by streaming
    report_text = ""
    async for event in runner.stream_events():
        if hasattr(event, "type") and event.type == "raw_response_event":
            if hasattr(event, "data") and event.data:
                # Extract text from the event
                data = event.data
                if hasattr(data, "delta"):
                    delta = data.delta
                    if isinstance(delta, str):
                        report_text += delta
                        console.print(delta, end="")
                    elif hasattr(delta, "text") and delta.text:
                        report_text += delta.text
                        console.print(delta.text, end="")
                    elif hasattr(delta, "content") and delta.content:
                        report_text += delta.content
                        console.print(delta.content, end="")

    # Try to get final output from runner if available
    if not report_text:
        if hasattr(runner, "final_output") and runner.final_output:
            if isinstance(runner.final_output, str):
                report_text = runner.final_output
            elif hasattr(runner.final_output, "text"):
                report_text = runner.final_output.text
            elif hasattr(runner.final_output, "content"):
                report_text = runner.final_output.content

    # Create report data structure
    report_data = {
        "example": example_name,
        "task": task_description,
        "generated_at": datetime.now().isoformat(),
        "report": report_text,
        "agent_name": agent.name if hasattr(agent, "name") else "Unknown",
    }

    # Determine output directory
    if output_dir is None:
        # Default to reports/ directory in project root
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / "reports"
    else:
        output_dir = Path(output_dir)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{example_name}_report_{timestamp}.json"
    filepath = output_dir / filename

    # Save report to JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    console.print(f"\n✓ Report saved to: {filepath}", style="bold green")
    console.print()

    return report_data

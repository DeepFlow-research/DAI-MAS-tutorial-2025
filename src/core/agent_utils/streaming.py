"""Shared utilities for streaming agent output."""

import asyncio
import json
from typing import TYPE_CHECKING, Any

from agents import RunResultStreaming

if TYPE_CHECKING:
    from openai.types.responses import (
        ResponseOutputItemAddedEvent,
        ResponseOutputItemDoneEvent,
        ResponseTextDeltaEvent,
    )


async def stream_agent_output(runner: RunResultStreaming, context: Any = None) -> None:
    """
    Simplified event handler that displays:
    - Streaming text/thinking from the agent
    - Tool calls with inputs and outputs paired together
    - Agent handoffs

    Note: Tool functions themselves are synchronous Python functions.
    The SDK handles calling them asynchronously, but the tool implementations
    don't need to be async unless they perform async I/O operations.

    Args:
        runner: The RunResultStreaming instance from Runner.run_streamed()
        context: Optional context object (e.g., AuditContext) for crisis tracking
    """
    # Track pending tool calls by their ID to match with results
    pending_tool_calls: dict[str, dict[str, Any]] = {}

    try:
        # Consume all events from the async generator
        async for event in runner.stream_events():
            # Handle raw response events (streaming text and tool calls)
            if hasattr(event, "type") and event.type == "raw_response_event":
                if hasattr(event, "data") and event.data:
                    await _handle_raw_response_event(
                        event.data, pending_tool_calls, context
                    )

            # Handle run item events (tool outputs)
            elif hasattr(event, "type") and event.type == "run_item_stream_event":
                if hasattr(event, "item") and event.item:
                    await _handle_run_item_event(event.item, pending_tool_calls)

            # Handle agent updated events (handoffs)
            elif hasattr(event, "type") and event.type == "agent_updated_stream_event":
                if hasattr(event, "new_agent") and event.new_agent:
                    print(f"\n👤 [Agent: {event.new_agent.name}]\n", flush=True)

    finally:
        # Ensure all events are consumed and allow cleanup
        # The Runner's underlying HTTP client sessions (from LiteLLM/OpenAI SDK)
        # will be cleaned up by Python's garbage collector. The "unclosed client session"
        # warning is harmless - it's just Python warning that aiohttp sessions weren't
        # explicitly closed before garbage collection. The SDK handles cleanup internally.
        await asyncio.sleep(0.1)  # Small delay to allow any pending cleanup

        # Try to close underlying client if accessible (best-effort)
        # Note: Runner doesn't expose a close() method, so this may not work
        for attr_name in ["_client", "client", "_http_client", "http_client"]:
            if hasattr(runner, attr_name):
                client = getattr(runner, attr_name)
                if hasattr(client, "close"):
                    try:
                        if asyncio.iscoroutinefunction(client.close):
                            await client.close()
                        else:
                            client.close()
                    except (AttributeError, TypeError, RuntimeError):
                        pass


async def _handle_raw_response_event(
    data: "ResponseTextDeltaEvent | ResponseOutputItemAddedEvent | ResponseOutputItemDoneEvent | Any",
    pending_tool_calls: dict[str, dict[str, Any]],
    context: Any = None,
) -> None:
    """
    Handle raw response events containing streaming text or tool call information.

    Args:
        data: The event data from a raw_response_event
        pending_tool_calls: Dictionary to track pending tool calls by ID
        context: Optional context object (e.g., AuditContext) for crisis tracking
    """
    from openai.types.responses import (
        ResponseFunctionToolCall,
        ResponseOutputItemAddedEvent,
        ResponseOutputItemDoneEvent,
        ResponseTextDeltaEvent,
    )

    # Handle text deltas (streaming text)
    if isinstance(data, ResponseTextDeltaEvent):
        if hasattr(data, "delta") and data.delta:
            # Check if delta is a string (as suggested by type error)
            if isinstance(data.delta, str):
                text = data.delta
                if text.isprintable() or text.isspace():
                    print(text, end="", flush=True)
            # Fallback for object-like delta
            elif hasattr(data.delta, "text") and data.delta.text:
                # Only print printable text to avoid encoding issues
                text = data.delta.text
                if text.isprintable() or text.isspace():
                    print(text, end="", flush=True)

            elif hasattr(data.delta, "content") and data.delta.content:
                content = data.delta.content
                if content.isprintable() or content.isspace():
                    print(content, end="", flush=True)

    # Handle tool call start (function call added) - store for later matching
    elif isinstance(data, ResponseOutputItemAddedEvent):
        if hasattr(data, "item") and isinstance(data.item, ResponseFunctionToolCall):
            tool_call = data.item
            tool_name = getattr(tool_call, "name", None)
            tool_id = getattr(tool_call, "id", None) or getattr(
                tool_call, "call_id", None
            )

            if tool_name:
                # Track ALL tool calls globally - increment counter for every tool call
                # Tools with ctx will check the count in their wrapper (may see 9 or 10 depending on timing)
                if context is not None and hasattr(context, "increment_tool_call"):
                    context.increment_tool_call()

                # Store tool call info for matching with result
                if tool_id:
                    pending_tool_calls[tool_id] = {
                        "name": tool_name,
                        "arguments": getattr(tool_call, "arguments", None),
                    }

                # Format tool name nicely (convert snake_case to Title Case)
                display_name = " ".join(
                    word.capitalize() for word in tool_name.split("_")
                )
                print(f"\n🔧 Calling: {display_name}", flush=True)

                # Show arguments if available
                if hasattr(tool_call, "arguments") and tool_call.arguments:
                    try:
                        args_dict = (
                            json.loads(tool_call.arguments)
                            if isinstance(tool_call.arguments, str)
                            else tool_call.arguments
                        )
                        if args_dict:
                            print("   Parameters:", flush=True)
                            for key, value in args_dict.items():
                                print(f"     • {key}: {value}", flush=True)
                    except (json.JSONDecodeError, TypeError):
                        print(f"   Parameters: {tool_call.arguments}", flush=True)

    # Handle tool call completion (function call done) - we'll show result when it arrives
    elif isinstance(data, ResponseOutputItemDoneEvent):
        # Tool call is done, but we wait for the result to show them together
        pass


async def _handle_run_item_event(
    item: Any, pending_tool_calls: dict[str, dict[str, Any]]
) -> None:
    """
    Handle run item events containing tool outputs.
    Matches tool outputs with their corresponding tool calls and displays them together.

    Args:
        item: The item from a run_item_stream_event
        pending_tool_calls: Dictionary of pending tool calls to match with results
    """
    # Check if this is a tool output
    if hasattr(item, "output") and item.output is not None:
        # Try to get tool name and ID from various places
        tool_name: str | None = None
        tool_id: str | None = None

        # Try to get tool call ID to match with pending calls
        if hasattr(item, "tool_call_id"):
            tool_id = item.tool_call_id
        elif hasattr(item, "call_id"):
            tool_id = item.call_id
        elif hasattr(item, "id"):
            tool_id = item.id

        # Try to get tool name
        if hasattr(item, "name"):
            tool_name = item.name
        elif hasattr(item, "tool_name"):
            tool_name = item.tool_name
        elif hasattr(item, "function_name"):
            tool_name = item.function_name

        # Try to match with pending call by ID first, then by name
        matched_call = None

        if tool_id and tool_id in pending_tool_calls:
            matched_call = pending_tool_calls.pop(tool_id)
            tool_name = tool_name or matched_call.get("name")
        elif tool_name:
            # Try to match by name (for cases where ID matching fails)
            # Find first pending call with matching name
            for call_id, call_info in list(pending_tool_calls.items()):
                if call_info.get("name") == tool_name:
                    matched_call = pending_tool_calls.pop(call_id)
                    break

        output = item.output

        # Show result immediately after the tool call (or standalone if no match)
        if matched_call:
            # We already showed the tool call, now show the result right after
            print("\n✓ Result:", flush=True)
        else:
            # No matching call found, show tool name if available
            if tool_name:
                display_name = " ".join(
                    word.capitalize() for word in tool_name.split("_")
                )
                print(f"\n✓ {display_name} Result:", flush=True)
            else:
                print("\n✓ Result:", flush=True)

        # Format output based on type
        if isinstance(output, dict):
            # Pretty print dictionary output
            _print_dict_nicely(output, indent=2)
        elif hasattr(output, "model_dump"):
            # Pydantic model
            _print_dict_nicely(output.model_dump(), indent=2)
        elif isinstance(output, list):
            # List output
            if len(output) == 0:
                print("   (empty list)", flush=True)
            else:
                for i, output_item in enumerate(output[:10], 1):  # Show first 10 items
                    print(f"   {i}. {output_item}", flush=True)
                if len(output) > 10:
                    print(f"   ... and {len(output) - 10} more items", flush=True)
        elif isinstance(output, str):
            # String output - check if it's an error
            if "error" in output.lower() or "Error:" in output:
                print(f"   ⚠ Error: {output}", flush=True)
            else:
                output_str = output[:500] + ("..." if len(output) > 500 else "")
                print(f"   {output_str}", flush=True)
        else:
            output_str = str(output)
            truncated = output_str[:500] + ("..." if len(output_str) > 500 else "")
            print(f"   {truncated}", flush=True)


def _print_dict_nicely(data: dict, indent: int = 0, max_depth: int = 3) -> None:
    """
    Print a dictionary in a more readable format for demos.

    Args:
        data: Dictionary to print
        indent: Current indentation level
        max_depth: Maximum nesting depth to print
    """
    if indent // 2 > max_depth:
        print(" " * indent + "...", flush=True)
        return

    prefix = " " * indent
    for key, value in data.items():
        # Format key nicely
        display_key = " ".join(
            word.capitalize() for word in str(key).replace("_", " ").split()
        )

        if isinstance(value, dict):
            print(f"{prefix}• {display_key}:", flush=True)
            _print_dict_nicely(value, indent + 2, max_depth)
        elif isinstance(value, list):
            print(f"{prefix}• {display_key}:", flush=True)
            if len(value) == 0:
                print(f"{prefix}  (empty)", flush=True)
            elif len(value) <= 3:
                for item in value:
                    if isinstance(item, dict):
                        _print_dict_nicely(item, indent + 2, max_depth)
                    else:
                        print(f"{prefix}  - {item}", flush=True)
            else:
                for item in value[:3]:
                    if isinstance(item, dict):
                        _print_dict_nicely(item, indent + 2, max_depth)
                    else:
                        print(f"{prefix}  - {item}", flush=True)
                print(f"{prefix}  ... and {len(value) - 3} more items", flush=True)
        else:
            # Format value nicely
            if value is None:
                display_value = "(none)"
            elif isinstance(value, bool):
                display_value = "Yes" if value else "No"
            elif isinstance(value, (int, float)):
                display_value = str(value)
            else:
                display_value = str(value)
                # Truncate long strings
                if len(display_value) > 100:
                    display_value = display_value[:100] + "..."

            print(f"{prefix}• {display_key}: {display_value}", flush=True)

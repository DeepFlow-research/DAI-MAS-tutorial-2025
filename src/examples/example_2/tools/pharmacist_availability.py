"""Tool for checking pharmacist availability."""

import random

from agents import RunContextWrapper, function_tool

from src.examples.example_2.resources.pharmacist_context import PharmacistContext


@function_tool
def check_pharmacist_availability(
    ctx: RunContextWrapper[PharmacistContext],
) -> bool:
    """
    Check if the pharmacist specialist is currently available.

    This tool checks the pharmacist's availability status. The pharmacist
    may become available at different times during the audit process.

    Returns:
        True if pharmacist is available, False otherwise
    """
    # 25% chance of returning True
    is_available = random.random() < 0.25

    # Update the context
    ctx.context.pharmacist_is_available = is_available

    return is_available

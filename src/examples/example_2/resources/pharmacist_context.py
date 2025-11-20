"""Shared context for ad-hoc teaming in Example 2."""

from pydantic import BaseModel, Field


class PharmacistContext(BaseModel):
    """Shared context for tracking pharmacist availability."""

    pharmacist_is_available: bool = Field(
        default=False,
        description="Whether the pharmacist specialist is currently available for handoffs",
    )

    model_config = {"extra": "forbid"}

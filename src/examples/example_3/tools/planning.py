"""Example 3 specific planning tools with crisis detection."""

from datetime import datetime
from typing import Literal
from uuid import uuid4

from agents import RunContextWrapper

from src.core.tools.planning import (
    AuditPlan,
    ItemPriorityUpdate,
    PlanItemInput,
    PlanItemUpdateResponse,
    PlanItem,
)
from src.examples.example_3.resources.audit_context import AuditContext
from src.examples.example_3.tools.crisis_wrapper import crisis_aware_tool
import src.core.tools.planning as core_planning_module

# Re-export types for convenience
__all__ = [
    "AuditPlan",
    "PlanItemInput",
    "PlanItemUpdateResponse",
    "ItemPriorityUpdate",
    "create_audit_plan",
    "update_plan_item",
    "get_plan_status",
    "list_plans",
    "update_audit_plan",
]


@crisis_aware_tool
def create_audit_plan(
    ctx: RunContextWrapper[AuditContext],
    title: str,
    items: list[PlanItemInput],
) -> AuditPlan:
    """
    Create a new audit plan with multiple tasks.

    Use this to break down complex audit tasks into manageable sub-tasks.
    Each item should have: description, priority (optional), assigned_agent (optional).

    Args:
        ctx: Shared context for crisis detection
        title: Plan title/description
        items: List of task items

    Returns:
        Created AuditPlan with all items set to "pending" status
    """
    # Access the shared plan storage from core module
    _PLANS = core_planning_module._PLANS

    plan_id = f"PLAN-{uuid4().hex[:8].upper()}"
    created_at = datetime.now().isoformat()

    plan_items = []
    for i, item_input in enumerate(items):
        item_id = f"{plan_id}-ITEM-{i + 1}"
        plan_items.append(
            PlanItem(
                item_id=item_id,
                description=item_input.description,
                assigned_agent=item_input.assigned_agent,
                priority=item_input.priority,
                status="pending",
                notes=item_input.notes,
            )
        )

    plan = AuditPlan(
        plan_id=plan_id,
        created_at=created_at,
        title=title,
        items=plan_items,
        status="active",
    )

    _PLANS[plan_id] = plan
    return plan


@crisis_aware_tool
def update_plan_item(
    ctx: RunContextWrapper[AuditContext],
    plan_id: str,
    item_id: str,
    status: Literal["pending", "in_progress", "completed", "blocked"] | None = None,
    assigned_agent: str | None = None,
    notes: str | None = None,
) -> PlanItemUpdateResponse:
    """
    Update a specific item in an audit plan.

    Use this to track progress: mark items as "in_progress" when delegating,
    "completed" when done, or "blocked" if there's an issue.

    Args:
        ctx: Shared context for crisis detection
        plan_id: Plan identifier
        item_id: Item identifier to update
        status: New status (optional)
        assigned_agent: Agent assigned to this task (optional)
        notes: Additional notes or results (optional)

    Returns:
        PlanItemUpdateResponse with updated item and progress summary
    """
    _PLANS = core_planning_module._PLANS

    if plan_id not in _PLANS:
        raise ValueError(f"Plan {plan_id} not found")

    plan = _PLANS[plan_id]
    item = None
    for plan_item in plan.items:
        if plan_item.item_id == item_id:
            item = plan_item
            break

    if item is None:
        raise ValueError(f"Item {item_id} not found in plan {plan_id}")

    # Update fields
    if status is not None:
        item.status = status
    if assigned_agent is not None:
        item.assigned_agent = assigned_agent
    if notes is not None:
        item.notes = notes

    # Auto-update plan status if all items completed
    if all(i.status == "completed" for i in plan.items):
        plan.status = "completed"

    # Generate progress summary
    total_items = len(plan.items)
    completed_count = sum(1 for i in plan.items if i.status == "completed")
    in_progress_count = sum(1 for i in plan.items if i.status == "in_progress")
    pending_items = [i for i in plan.items if i.status == "pending"]

    # Build progress summary
    progress_parts = [f"{completed_count}/{total_items} completed"]
    if in_progress_count > 0:
        progress_parts.append(f"{in_progress_count} in progress")

    # Add next pending items (up to 3)
    if pending_items:
        next_items = pending_items[:3]
        next_descriptions = [
            item.description[:50] + ("..." if len(item.description) > 50 else "")
            for item in next_items
        ]
        if len(pending_items) > 3:
            progress_parts.append(
                f"next 3 pending: {', '.join(next_descriptions)} ({len(pending_items) - 3} more)"
            )
        else:
            progress_parts.append(
                f"next {len(next_items)} pending: {', '.join(next_descriptions)}"
            )
    elif completed_count == total_items:
        progress_parts.append("all tasks completed!")

    progress_summary = "; ".join(progress_parts)

    return PlanItemUpdateResponse(
        updated_item=item,
        progress_summary=progress_summary,
    )


@crisis_aware_tool
def get_plan_status(
    ctx: RunContextWrapper[AuditContext],
    plan_id: str,
) -> AuditPlan:
    """
    Get the current status of an audit plan.

    Use this to check progress and see which tasks are pending, in progress, or completed.

    Args:
        ctx: Shared context for crisis detection
        plan_id: Plan identifier

    Returns:
        AuditPlan with current status of all items
    """
    _PLANS = core_planning_module._PLANS

    if plan_id not in _PLANS:
        raise ValueError(f"Plan {plan_id} not found")

    return _PLANS[plan_id]


@crisis_aware_tool
def list_plans(
    ctx: RunContextWrapper[AuditContext],
) -> list[AuditPlan]:
    """
    List all active audit plans.

    Args:
        ctx: Shared context for crisis detection

    Returns:
        List of all active plans
    """
    _PLANS = core_planning_module._PLANS

    return [plan for plan in _PLANS.values() if plan.status == "active"]


@crisis_aware_tool
def update_audit_plan(
    ctx: RunContextWrapper[AuditContext],
    plan_id: str,
    title: str | None = None,
    add_items: list[PlanItemInput] | None = None,
    remove_item_ids: list[str] | None = None,
    reprioritize_items: list[ItemPriorityUpdate] | None = None,
    status: Literal["draft", "active", "completed", "cancelled"] | None = None,
) -> AuditPlan:
    """
    Adaptively update an audit plan in response to changing conditions (e.g., crisis mode).

    Use this when priorities change or you need to replan:
    - Add new high-priority items
    - Remove or deprioritize low-priority items
    - Reprioritize existing items
    - Update plan status

    This is especially important when crisis mode is activated - you should
    replan to focus on high-risk medications and expedite critical checks.

    Args:
        ctx: Shared context for crisis detection
        plan_id: Plan identifier to update
        title: New title (optional)
        add_items: New items to add (optional)
        remove_item_ids: Item IDs to remove (optional)
        reprioritize_items: List of priority updates (optional)
        status: New plan status (optional)

    Returns:
        Updated AuditPlan
    """
    _PLANS = core_planning_module._PLANS

    if plan_id not in _PLANS:
        raise ValueError(f"Plan {plan_id} not found")

    plan = _PLANS[plan_id]

    # Update title if provided
    if title is not None:
        plan.title = title

    # Add new items
    if add_items:
        for item_input in add_items:
            item_id = f"{plan_id}-ITEM-{len(plan.items) + 1}"
            plan.items.append(
                PlanItem(
                    item_id=item_id,
                    description=item_input.description,
                    assigned_agent=item_input.assigned_agent,
                    priority=item_input.priority,
                    status="pending",
                    notes=item_input.notes,
                )
            )

    # Remove items
    if remove_item_ids:
        plan.items = [
            item for item in plan.items if item.item_id not in remove_item_ids
        ]

    # Reprioritize items
    if reprioritize_items:
        # Create a lookup dict from the list of updates
        priority_updates: dict[str, Literal["low", "medium", "high", "critical"]] = {
            update.item_id: update.priority for update in reprioritize_items
        }
        for item in plan.items:
            if item.item_id in priority_updates:
                item.priority = priority_updates[item.item_id]

    # Update status
    if status is not None:
        plan.status = status

    # Auto-update status if all items completed
    if all(i.status == "completed" for i in plan.items):
        plan.status = "completed"

    return plan

# Example 3: Multi-Objective Non-Stationary Preferences

## Scenario

The audit team is conducting a routine, thorough audit of ICU medication records when a **crisis event occurs mid-execution**: multiple trauma patients are admitted to the ICU Emergency Department. The system must:
- **Adapt priorities immediately**: Switch from thoroughness to speed
- **Reprioritize tasks**: Focus on high-risk medications first
- **Continue operations**: Don't halt, but adapt strategy
- **Replan dynamically**: Update the audit plan to reflect new priorities
- **Coordinate emergency response**: Leverage the Head of Emergency Room for crisis planning

The crisis is **automatically triggered on the 10th tool call** to simulate a real-world event occurring during normal operations. The system should naturally adapt to the crisis without explicit instructions about what to do when it occurs.

## Builds On Example 2

**Problem**: Example 2's system treats all tasks equally and can't adapt to changing priorities or crisis events. The manager has no way to balance competing objectives (speed vs thoroughness) or respond to urgent situations.

**Solution**: Implement **shared context pattern** with:
1. Global state tracking (tool calls, crisis events, preferences)
2. Tool-level short-circuiting (tools block until crisis acknowledged)
3. Adaptive replanning (manager updates plan when crisis detected)
4. Emergency response specialist (Head of Emergency Room agent for crisis planning)
5. General preference-balancing instructions (manager adapts based on information received, not explicit protocols)

## Technical Implementation

### Shared Context Pattern

**AuditContext** (Pydantic BaseModel):
```python
class AuditContext(BaseModel):
    tool_call_count: int = 0  # Global counter
    crisis_events: list[dict] = field(default_factory=list)
    alert_level: str = "normal"  # "normal", "elevated", "crisis"
    current_preferences: PreferenceWeights = ...
    crisis_raised: bool = False  # Key flag for short-circuiting
    
    model_config = {"extra": "forbid"}  # Strict schema validation
```

**Context Passed to Runner**:
```python
context = AuditContext()
runner = Runner.run_streamed(manager, input=TASK, context=context)
```

### Crisis Detection Mechanism

#### 1. Tool Call Counter
Every tool call with `ctx: RunContextWrapper[AuditContext]` increments the global counter:

```python
@crisis_aware_tool
def create_audit_plan(ctx: RunContextWrapper[AuditContext], ...):
    # Wrapper automatically increments counter
    # On 10th call, triggers crisis
    ...
```

#### 2. Crisis Wrapper (`crisis_wrapper.py`)

**Simplified Implementation** (reuses SDK's conversion logic):
```python
def with_crisis_check(func):
    """Wraps function to check crisis status."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ctx = _extract_ctx(func, ctx_param_name, args, kwargs)
        
        if ctx and hasattr(ctx, "context"):
            current_count = ctx.context.tool_call_count
            
            # Trigger crisis on 10th call
            if current_count == 10 and not ctx.context.crisis_raised:
                ctx.context.add_crisis_event(...)
                return CRISIS_MESSAGE
            elif current_count > 10 and not ctx.context.crisis_raised:
                ctx.context.add_crisis_event(...)
                return CRISIS_MESSAGE
            
            # Short-circuit until crisis raised (calls 1-9)
            if not ctx.context.crisis_raised:
                return CRISIS_MESSAGE
        
        return func(*args, **kwargs)
    return wrapper

def crisis_aware_tool(func):
    """Combines @function_tool and @with_crisis_check."""
    # Create tool from original function (for schema generation)
    tool = function_tool(func)
    
    # Wrap function with crisis check
    wrapped_func = with_crisis_check(func)
    
    # Create new tool from wrapped function - SDK handles JSON->Pydantic conversion
    wrapped_tool = function_tool(wrapped_func)
    
    # Replace on_invoke_tool to reuse SDK's conversion logic
    tool.on_invoke_tool = wrapped_tool.on_invoke_tool
    return tool
```

**Crisis Message**:
```
🚨 CRITICAL EMERGENCY ALERT 🚨

Multiple trauma patients have been admitted to the ICU Emergency Department.
The hospital is now in crisis mode and priorities must shift immediately.

Our goal is now to see if we get small free time to finish our audit, we can

But our key objective is now to handle these patients using the best team members for the job.
```

**Key Behavior**:
- Tools return crisis message until `crisis_raised=True` (calls 1-9)
- On 10th call, crisis is triggered and message returned
- After crisis raised, tools work normally
- **Simplified**: Reuses SDK's built-in JSON→Pydantic conversion instead of reimplementing it

**Critical Insight**: By creating a tool from the wrapped function, we automatically get the SDK's conversion logic for free - no need to manually handle Union types, Optional types, nested lists, etc.

### Adaptive Replanning

**New Tool**: `update_audit_plan`
```python
@crisis_aware_tool
def update_audit_plan(
    ctx: RunContextWrapper[AuditContext],
    plan_id: str,
    reprioritize_items: list[ItemPriorityUpdate] | None = None,
    remove_item_ids: list[str] | None = None,
    add_items: list[PlanItemInput] | None = None,
    ...
) -> AuditPlan:
    """Adaptively update plan in response to changing conditions."""
    # Reprioritize: Focus on high-risk/critical items
    # Remove: Low-priority items that can wait
    # Add: Urgent crisis-response tasks
```

**Manager Instructions** (General, Not Explicit):
```
- Balance multiple competing objectives based on current priorities
- When priorities shift mid-execution: Use update_audit_plan to adaptively replan
- If urgent priorities emerge: Reprioritize items, focus on high-risk/critical
- Consider delegating to Head of Emergency Room for emergency response planning
```

**Key Design**: The manager is NOT explicitly told what to do when crisis occurs. It must interpret the crisis message and adapt based on general instructions about balancing objectives. This tests whether the system can naturally handle crises without explicit protocols.

### Emergency Response Specialist

**New Agent**: Head of Emergency Room
- **Role**: Crisis response planning specialist
- **Tools**: Same planning tools as manager (with crisis detection)
- **Purpose**: Create/update crisis response plans during emergencies
- **Integration**: Manager can delegate to this agent when urgent priorities emerge

The manager is instructed to "consider delegating to the Head of Emergency Room for emergency response planning" but is not explicitly told to do so when crisis messages appear. This tests adaptive delegation.

### Code Structure
```python
# Create shared context
context = AuditContext()

# Create team
manager = create_manager_agent(
    worker_agents=[...workers...],
    tools=[...planning tools...],
)

# Run with context
runner = Runner.run_streamed(manager, input=TASK, context=context)
```

## What We Learn

### ✅ What Works
- **Event-Driven Adaptation**: System responds to crisis automatically
- **Non-Interrupting**: Crisis doesn't halt execution, tools short-circuit gracefully
- **Shared State**: Context persists across handoffs (SDK feature)
- **Adaptive Replanning**: Manager can update plan for crisis conditions
- **Tool-Level Enforcement**: Short-circuiting ensures crisis is acknowledged
- **Simplified Implementation**: Reusing SDK's conversion logic reduces complexity
- **Natural Adaptation**: Manager adapts based on general instructions, not explicit protocols

### ❌ Limitations Revealed
1. **Preference Conflicts**: Speed vs thoroughness can conflict with safety
   - System might skip critical safety checks in crisis mode
   - Need governance to ensure preferences don't override safety protocols

2. **Manual Replanning**: Manager must manually call `update_audit_plan`
   - Could be automated with better planning tools
   - Relies on LLM to recognize crisis and replan
   - **Testing**: Does the manager naturally delegate to Head of Emergency Room?

3. **Hardcoded Trigger**: Crisis triggers on 10th tool call (for demo)
   - Real system would use event detection
   - Could be more sophisticated (time-based, external events)

4. **LLM-Dependent Adaptation**: Manager's response depends on LLM interpretation
   - May not always recognize crisis or delegate appropriately
   - No guarantee of optimal crisis response

### Key Technical Insights

1. **Shared Context Pattern**: Using `RunContextWrapper[T]` enables global state that persists across agents
2. **Tool-Level Short-Circuiting**: Wrapping tools with crisis checks enforces acknowledgment
3. **Reusing SDK Logic**: Creating a tool from wrapped function automatically gives us JSON→Pydantic conversion - no need to reimplement complex type handling
4. **Bidirectional Handoffs**: Enable dynamic team coordination and crisis response
5. **General Instructions**: Manager adapts based on general preference-balancing instructions, not explicit crisis protocols - tests natural adaptation
6. **Emergency Specialist**: Head of Emergency Room agent provides dedicated crisis planning capability

### Next Steps
**Example 4** will introduce **safety and governance** - regulatory constraints, approval workflows, and audit trails to ensure preferences don't compromise patient safety.


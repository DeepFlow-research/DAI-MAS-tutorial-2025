# Example 2: Ad Hoc Teaming

## Scenario

The audit team is **midway through** auditing ICU medication records when a **senior clinical pharmacist specialist** becomes available. This specialist has deep expertise in:
- Complex drug-drug interactions
- Pharmacokinetics and pharmacodynamics
- Medication dosing in special populations

The team needs to:
- Integrate the new specialist into the ongoing workflow
- Redistribute tasks to leverage their expertise
- Provide context (findings, pending records, concerns)
- Have them focus on high-risk medication cases

## Builds On Example 1

**Problem**: Example 1's team is **static** - fixed at startup, can't adapt to new specialists or changing requirements.

**Solution**: Enable **dynamic team composition** through:
1. Bidirectional handoffs (workers can hand off to each other)
2. Context sharing (new agent receives current audit status)
3. Flexible task redistribution

## Technical Implementation

### Dynamic Agent Integration

**New Agent Added Mid-Execution**:
```python
pharmacist_specialist = create_agent(
    name="Pharmacist Specialist",
    instructions="...",  # Expert in drug interactions
    role=AgentRole.PHARMACIST_SPECIALIST,
    tools=get_tools_for_role(AgentRole.PHARMACIST_SPECIALIST),
)
```

**Bidirectional Handoffs**:
```python
manager = create_manager_agent(
    worker_agents=[...existing workers..., pharmacist_specialist],
    enable_bidirectional_handoffs=True,  # Workers can hand to each other
)

# All agents can hand off to each other
all_agents = [manager] + worker_agents
for worker in worker_agents:
    worker.handoffs = all_agents  # Ring topology
```

### Key Mechanisms

#### 1. Handoff Instructions
Manager instructions explicitly guide integration:
```
"A Pharmacist Specialist has joined the team. When you encounter complex
drug interaction cases, hand off to the Pharmacist Specialist for expert
analysis. They have access to all relevant tools and context."
```

#### 2. Context Through Planning Tools
The new specialist can:
- Call `get_plan_status` to see current audit progress
- Check `list_plans` to understand what's been done
- Use `update_plan_item` to mark their work

#### 3. Peer-to-Peer Handoffs
Workers can hand off to each other:
- Medication Records Specialist → Pharmacist Specialist (for drug interaction analysis)
- Pharmacist Specialist → Manager (to report findings)

### Code Structure
```python
# Existing team from Example 1
all_workers = [medication_specialists, patient_specialists, ...]

# Add new specialist
pharmacist_specialist = create_agent(...)
all_workers.append(pharmacist_specialist)

# Manager with bidirectional handoffs
manager = create_manager_agent(
    worker_agents=all_workers,
    enable_bidirectional_handoffs=True,  # Key difference from Example 1
)
```

## What We Learn

### ✅ What Works
- **Dynamic Integration**: New specialist successfully joins mid-audit
- **Context Sharing**: Planning tools provide shared state
- **Flexible Coordination**: Peer-to-peer handoffs enable direct collaboration
- **Expertise Leveraging**: Manager redirects complex cases to specialist

### ❌ Limitations Revealed
1. **No Governance**: New agent reports findings directly
   - May violate HIPAA compliance (no approval workflow)
   - Missing audit trail requirements
   - No validation of findings before reporting

2. **No Preference Management**: Can't balance competing objectives
   - Speed vs thoroughness
   - Cost vs quality
   - Can't adapt priorities mid-execution

3. **No Crisis Handling**: System can't respond to urgent events
   - All tasks treated equally
   - No way to reprioritize when crisis occurs

### Next Steps
**Example 3** introduces **preference management** with **event-driven priority changes** - the system adapts when a crisis occurs mid-execution.


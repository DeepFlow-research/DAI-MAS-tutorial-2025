# Example 1: Hierarchical Decomposition

## Scenario

The hospital needs to audit **all ICU medication records from the past 7 days** (5 records). This is too large for a single agent to handle sequentially. The audit must:
- Cover 5 medication records
- Verify dosage accuracy, drug interactions, allergies, timing
- Organize results by patient, medication type, and risk level
- Complete within 48 hours for regulatory deadlines

## Builds On Example 0

**Problem**: Example 0's single-agent approach fails at scale (timeouts, token limits, sequential processing).

**Solution**: Introduce a **manager agent** that:
1. Decomposes the large task into smaller sub-tasks
2. Coordinates multiple specialized worker agents
3. Enables parallel execution through handoffs

## Technical Implementation

### Multi-Agent Architecture

**Manager Agent**:
- **Role**: Task decomposition and coordination
- **Tools**: Planning tools (`create_audit_plan`, `update_plan_item`, `get_plan_status`)
- **Capability**: Hand off to worker agents sequentially

**Worker Agents** (Specialized):
- **Medication Records Specialists** (4 instances): Fetch and organize records
- **Patient Data Specialists** (2 instances): Retrieve patient information and lab results
- **Compliance Auditors** (2 instances): Verify dosages, interactions, timing, HIPAA
- **Prescription Verifier** (1 instance): Verify prescriptions and prescriber credentials
- **Audit Reporter** (1 instance): Generate final reports

### Key Mechanisms

#### 1. Handoffs
```python
manager = create_manager_agent(
    name="Audit Manager",
    instructions="...",  # Decomposition and coordination logic
    worker_agents=[...],  # List of worker agents
    enable_bidirectional_handoffs=True,  # Workers can hand back
)
```

- Manager can hand off to any worker agent
- Workers hand back to manager after completing tasks
- Sequential handoffs (SDK limitation: one at a time)

#### 2. Planning Tools
- `create_audit_plan`: Break down audit into plan items
- `update_plan_item`: Track progress (pending → in_progress → completed)
- `get_plan_status`: Check overall progress

#### 3. Role-Based Tool Assignment
Each worker agent gets a **subset** of tools based on their role:
- Medication Records Specialists: `fetch_ward_records`, `get_record_by_priority`, etc.
- Patient Data Specialists: `get_patient_info`, `get_recent_lab_results`, etc.
- Compliance Auditors: `verify_dosage`, `check_drug_interactions`, etc.

This forces **collaboration** - no single agent can complete the audit alone.

### Code Structure
```python
# Create specialized workers
medication_specialists = [create_agent(..., role=AgentRole.MEDICATION_RECORDS_SPECIALIST) ...]
patient_specialists = [create_agent(..., role=AgentRole.PATIENT_DATA_SPECIALIST) ...]
# ... more workers

# Create manager with handoffs
manager = create_manager_agent(
    name="Audit Manager",
    worker_agents=[...all workers...],
    tools=get_tools_for_role(AgentRole.MANAGER),  # Planning tools
)
```

## What We Learn

### ✅ What Works
- **Decomposition**: Manager successfully breaks down 5 records into manageable chunks
- **Coordination**: Sequential handoffs enable parallel-like execution
- **Specialization**: Role-based tool assignment forces collaboration
- **Scalability**: System can handle larger tasks by distributing work

### ❌ Limitations Revealed
1. **No Prioritization**: Manager treats all records equally
   - Critical high-risk medications may be audited after routine ones
   - No way to prioritize urgent cases

2. **Static Team**: Team composition is fixed at startup
   - Can't add specialists mid-execution
   - Can't adapt to changing requirements

3. **No Preference Management**: Can't balance competing objectives (speed vs thoroughness)

### Next Steps
**Example 2** introduces **ad hoc teaming** - dynamically integrating a new specialist agent mid-audit.


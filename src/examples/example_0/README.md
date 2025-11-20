# Example 0: Base Case - Simple Single-Agent Audit

## Scenario

A hospital needs to audit a single medication administration record (`REC-12345`) that was flagged during routine quality assurance. The audit must verify:
- Dosage accuracy (administered vs prescribed)
- Drug interactions with current medications
- Patient allergies
- Administration timing appropriateness

This is a **trivial task** - a single record that can be processed linearly by one agent.

## Technical Implementation

### Agent Setup
- **Single Agent**: One "Medication Audit Agent" with all tools available
- **Tools**: All audit tools (medication records, patient data, compliance checks, reporting)
- **Model**: Claude Haiku 4.5 (via LiteLLM)
- **Execution**: Direct `Runner.run_streamed()` with no handoffs

### Code Structure
```python
agent = create_agent(
    name="Medication Audit Agent",
    instructions="...",  # Simple instructions for single-record audit
    tools=get_all_tools(),  # All tools available
)
runner = Runner.run_streamed(agent, input=TASK, max_turns=100)
```

### Key Files
- `agents.py`: Single agent creation
- `consts.py`: Task definition (single record audit)
- `main.py`: Simple execution loop

## What We Learn

### ✅ What Works
- **Simple tasks**: Single-agent systems work perfectly for linear, well-defined tasks
- **Tool calling**: Agents can effectively use multiple tools in sequence
- **Structured outputs**: Pydantic models ensure type safety and validation

### ❌ Limitations Revealed
1. **Scalability**: This approach fails when asked to audit 5 records sequentially
   - Timeout issues (API rate limits, execution time)
   - Token limits (conversation history grows linearly)
   - No parallelism (one record at a time)

2. **No Coordination**: Single agent can't delegate or parallelize work

3. **No Specialization**: One agent tries to do everything (records, patient data, compliance, reporting)

### Next Steps
**Example 1** introduces **hierarchical decomposition** - a manager agent breaks down the large task (5 records) into sub-tasks and coordinates multiple worker agents to execute in parallel.


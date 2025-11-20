# Multi-Agent System Examples

This directory contains progressive examples demonstrating how manager agents become essential as system complexity increases. Each example builds on the previous one, introducing new challenges and solutions.

## Example Progression

### [Example 0: Base Case](./example_0/README.md)
**Simple Single-Agent Audit**
- Single agent with all tools
- Works for trivial tasks (one record)
- Reveals scalability limitations

### [Example 1: Hierarchical Decomposition](./example_1/README.md)
**Manager Coordinates Multiple Workers**
- Manager agent breaks down large tasks
- Multiple specialized worker agents
- Sequential handoffs enable parallel-like execution
- Reveals need for prioritization

### [Example 2: Ad Hoc Teaming](./example_2/README.md)
**Dynamic Team Integration**
- New specialist joins mid-execution
- Bidirectional handoffs enable peer-to-peer coordination
- Context sharing through planning tools
- Reveals need for preference management

### [Example 3: Multi-Objective Non-Stationary Preferences](./example_3/README.md)
**Event-Driven Priority Adaptation**
- Shared context pattern for global state (`AuditContext`)
- Crisis detection on 10th tool call (automatic trigger)
- Tool-level short-circuiting enforces acknowledgment
- Adaptive replanning when crisis occurs (`update_audit_plan`)
- Emergency response specialist (Head of Emergency Room agent)
- General preference-balancing instructions (tests natural adaptation)
- Reveals need for safety and governance

## Structure

Each example is organized in its own folder:

```
src/examples/
└── example_N/
    ├── README.md        # Detailed explanation (scenario, build-on, implementation, learnings)
    ├── __init__.py      # Package marker
    ├── consts.py        # Constants: TITLE, TASK, SUMMARY, PRE_RUN_INFO
    ├── agents.py        # Agent definitions (create_agent/create_manager_agent calls)
    └── main.py          # Main execution logic
```

## Running Examples

Run examples using Python's module syntax:

```bash
# Example 0: Base Case
python -m src.examples.example_0.main

# Example 1: Hierarchical Decomposition
python -m src.examples.example_1.main

# Example 2: Ad Hoc Teaming
python -m src.examples.example_2.main

# Example 3: Multi-Objective Preferences
python -m src.examples.example_3.main
```

## Shared Utilities

All shared utilities are in `src/core/`:
- `agent_utils/`: Agent creation, role definitions, streaming utilities
- `tools/`: Tool definitions, wrappers, and crisis detection
- `resources/`: Context objects, event simulations, test inputs
- `data/`: Mock data files

## Key Concepts Demonstrated

1. **Handoffs**: Agents delegate work to other agents
2. **Planning Tools**: Manager creates and tracks multi-step plans
3. **Role-Based Access**: Agents have different tool subsets (forces collaboration)
4. **Bidirectional Handoffs**: Workers can hand back to manager or peers
5. **Shared Context**: Global state persists across agents (`RunContextWrapper`)
6. **Crisis Detection**: Tool-level short-circuiting enforces acknowledgment
7. **Adaptive Replanning**: Manager updates plan when priorities change

## File Responsibilities

- **README.md**: Detailed explanation of scenario, technical implementation, and learnings
- **consts.py**: Constants like `TITLE`, `TASK`, `SUMMARY`, `PRE_RUN_INFO`
- **agents.py**: Contains all `create_agent()` and `create_manager_agent()` calls
- **main.py**: Direct execution logic - creates agents, runs with context, displays output


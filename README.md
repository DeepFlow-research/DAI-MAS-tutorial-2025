# DAI 2025 Tutorial - Multi-Agent Systems Coding Demo

This repository contains progressive coding examples demonstrating how manager agents become essential as system complexity increases in multi-agent systems.

## Overview

Five progressive examples showing the evolution from a simple single-agent system to a sophisticated multi-agent system with manager coordination:

- **Example 0**: Base case - single agent audits one record
- **Example 1**: Hierarchical decomposition - manager coordinates multiple worker agents (3-5 workers)
- **Example 2**: Ad hoc teaming - pharmacist specialist joins mid-audit
- **Example 3**: Multi-objective preferences - event-driven priority adaptation with crisis response
- **Example 4**: Safety & governance - HIPAA compliance, approval workflows, audit trails

## Domain: Healthcare Medication Safety Audit

The examples use a hospital medication administration audit system that evolves as real-world constraints reveal failures requiring increasingly complex management.

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Installation

1. Install dependencies:
```bash
uv sync
# or
pip install -e .
```

2. Set up environment variables:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
# or set LITELLM_API_KEY if using LiteLLM proxy
```

## Running Examples

Each example can be run independently:

```bash
# Example 0: Base case
python -m src.examples.example_0.main

# Example 1: Hierarchical decomposition
python -m src.examples.example_1.main

# Example 2: Ad hoc teaming
python -m src.examples.example_2.main

# Example 3: Multi-objective preferences
python -m src.examples.example_3.main

# Example 4: Safety & governance (when implemented)
python -m src.examples.example_4.main
```

## Project Structure

```
coding_demo_examples/
├── src/
│   ├── examples/                        # Example implementations
│   │   ├── example_0/                   # Base case
│   │   │   ├── README.md                # Detailed explanation
│   │   │   ├── agents.py                # Agent definitions
│   │   │   ├── consts.py                # Constants (TITLE, TASK, etc.)
│   │   │   └── main.py                  # Execution logic
│   │   ├── example_1/                   # Hierarchical decomposition
│   │   ├── example_2/                   # Ad hoc teaming
│   │   ├── example_3/                   # Multi-objective preferences
│   │   │   ├── tools/                   # Example-3 specific tools
│   │   │   │   ├── crisis_wrapper.py    # Crisis detection wrapper
│   │   │   │   └── planning.py          # Crisis-aware planning tools
│   │   │   └── resources/               # Example-3 specific resources
│   │   │       └── audit_context.py     # Shared AuditContext
│   │   └── example_4/                   # Safety & governance (when implemented)
│   ├── core/                            # Shared utilities
│   │   ├── agent_utils/                 # Agent creation utilities
│   │   │   ├── base.py                  # create_agent, create_manager_agent
│   │   │   ├── roles.py                 # Role-based tool assignment
│   │   │   └── streaming.py             # Streaming output utilities
│   │   ├── tools/                       # Shared tool implementations
│   │   │   ├── planning.py              # Core planning tools
│   │   │   ├── medication_records.py    # Medication record access
│   │   │   ├── patient_data.py          # Patient information
│   │   │   ├── prescriptions.py         # Prescription verification
│   │   │   ├── administration.py        # Administration timing
│   │   │   ├── inventory.py             # Medication inventory
│   │   │   ├── lab_results.py           # Lab results access
│   │   │   ├── compliance.py            # Compliance checking
│   │   │   ├── reporting.py             # Audit reporting
│   │   │   └── red_herring/             # Irrelevant tools (for testing)
│   │   │       ├── scheduling.py        # Staff scheduling
│   │   │       ├── billing.py           # Billing information
│   │   │       └── ward_management.py    # Ward capacity
│   │   └── resources/                    # Shared resources
│   │       └── events.py                # Event simulations
│   ├── pyproject.toml                   # Project dependencies
│   └── README.md                        # This file
```

See [src/examples/README.md](src/examples/README.md) for detailed documentation of each example.

## Key Technologies

- **Framework**: OpenAI Agents SDK (`openai-agents>=0.5.1`)
- **Model**: Claude 4.5 Haiku via LiteLLM (`LitellmModel`)
- **Language**: Python 3.13+
- **Type Safety**: Pydantic models for all inputs/outputs

## Narrative Flow

Each example builds on the previous, revealing limitations that drive the progression:

1. **Example 0 → 1**: Scale failure - single agent can't handle volume (5 records)
2. **Example 1 → 2**: Static team failure - can't integrate new specialists mid-execution
3. **Example 2 → 3**: Preference failure - can't balance competing objectives or adapt to crises
4. **Example 3 → 4**: Governance failure - preferences may override safety protocols

See [src/examples/README.md](src/examples/README.md) for detailed progression and learnings.

## Notes

- All functions use Pydantic models for type safety (no dict returns)
- Mock data is used for demonstration purposes
- Examples are designed for tutorial presentation with clear progression
- Each example includes comments explaining the scenario and limitations

## Runtime Issues and Fixes

See [RUNTIME_ISSUES_AND_FIXES.md](RUNTIME_ISSUES_AND_FIXES.md) for documentation of runtime issues encountered during development, their fixes, and recommendations for production use.

## License

This code is for educational purposes as part of the DAI 2025 Tutorial.


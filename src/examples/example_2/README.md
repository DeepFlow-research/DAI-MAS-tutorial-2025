# Example 2: Ad Hoc Teaming - Dynamic Team Formation

## Scenario

A **critical pediatric case** requires immediate expert consultation: a 6-year-old child with acute kidney injury receiving multiple nephrotoxic medications. The case clearly requires specific specialists:

- **Pediatric Specialist** (pediatric dosing)
- **Nephrology Specialist** (renal dosing adjustments)
- **Clinical Pharmacist** (drug interactions)
- **Infectious Disease Specialist** (antibiotic dosing)
- **Toxicology Specialist** (nephrotoxicity assessment)

**The Problem**: Only ~40% of specialists are available at any given time (random). The manager must:
1. Check which specialists are currently available
2. Form an ad-hoc team from available specialists
3. Proceed with the best possible team
4. Document limitations when critical expertise is missing

## Builds On Example 1

**Problem**: Example 1's team is **static** - fixed at startup, can't adapt to who's actually available.

**New Challenge**: Real healthcare environments have:
- Specialists on different shifts
- Experts in surgery/procedures
- Variable availability throughout the day
- Need to form teams dynamically based on current availability

**Solution**: Implement **dynamic roster management** with:
1. Large pool of specialist agents (10 different specialties)
2. Random availability (drawn at runtime, ~40% available)
3. Tools for checking availability (`check_specialist_availability`, `list_all_specialists`)
4. Manager must form ad-hoc team based on availability

## Technical Implementation

### Specialist Roster

**10 Specialist Roles**:
- Pediatric Specialist
- Nephrology Specialist  
- Cardiology Specialist
- Infectious Disease Specialist
- Toxicology Specialist
- Psychiatry Specialist
- Oncology Specialist
- Clinical Pharmacist
- Geriatric Specialist
- Pain Management Specialist

Each specialist has:
- Specific expertise areas
- Random availability status (40% probability)
- Role-appropriate tool access

### Availability Management

**TeamRosterContext** (Pydantic BaseModel):
```python
class TeamRosterContext(BaseModel):
    specialist_availability: dict[str, bool]  # Role -> availability
    availability_checks_made: int  # How many times manager checked
    handoff_attempts: list[dict]  # Log of all handoff attempts
    
    def initialize_random_availability(self, rate: float = 0.4):
        """Randomly set each specialist's availability."""
        
    def get_available_specialists(self) -> list[str]:
        """Get list of currently available specialists."""
        
    def log_handoff_attempt(self, source, target, successful, reason):
        """Track handoff attempts for debugging."""
```

### Availability Tools

**check_specialist_availability(specialist_role: str)**:
```python
@function_tool
def check_specialist_availability(
    ctx: RunContextWrapper[TeamRosterContext],
    specialist_role: str,
) -> dict:
    """
    Check if a specific specialist is currently available.
    
    Returns:
        {
            "is_available": bool,
            "role": str,
            "expertise": list[str],
            "message": str (human-readable status)
        }
    """
```

**list_all_specialists()**:
```python
@function_tool
def list_all_specialists(
    ctx: RunContextWrapper[TeamRosterContext],
) -> dict:
    """
    List all specialists in roster with availability status.
    
    Returns:
        {
            "available_specialists": list[str],
            "unavailable_specialists": list[str],
            "total_available": int,
            "roster": list[dict] (detailed info)
        }
    """
```

### Validation Hooks

**SpecialistAvailabilityHook**:
```python
class SpecialistAvailabilityHook(AgentHooks):
    async def on_handoff(self, context, agent, source, **kwargs):
        """Validate handoff to specialist agents."""
        if agent.name in specialist_names:
            if not context.specialist_availability[agent.name]:
                raise ValueError(
                    f"🚨 AVAILABILITY VIOLATION 🚨\n"
                    f"Cannot hand off to {agent.name} - UNAVAILABLE!"
                )
```

This **enforces** availability checks - attempting to hand off to an unavailable specialist causes a runtime error.

## What We're Demonstrating (The Failures)

### Expected Failure Modes

1. **Manager Doesn't Check Availability**
   - Assumes required specialists are available
   - Attempts handoff without calling `check_specialist_availability()`
   - **Result**: Runtime error from validation hook

2. **Manager Picks Wrong Team**
   - Required specialist (e.g., Pediatric) is unavailable
   - Manager picks less relevant specialist or proceeds without
   - **Result**: Incomplete analysis, missing critical expertise

3. **No Systematic Team Matching**
   - Query explicitly lists 5 required specialists
   - Manager must manually check each one
   - No framework support for "this query requires these roles"
   - **Result**: Brittle, LLM-dependent team formation

4. **Poor Adaptation Strategy**
   - Critical specialist unavailable
   - Manager has no fallback strategy
   - May proceed with inadequate expertise or fail entirely
   - **Result**: Suboptimal response to urgent query

5. **Context/Memory Limitations**
   - Query lists required specialists at the start
   - Manager may forget or ignore this by the time it forms team
   - **Result**: Picks wrong team despite clear requirements

## The "Greatest Query" Design

The query is designed to **maximize failure potential**:

- **High Stakes**: Pediatric patient, acute kidney injury, nephrotoxic drugs
- **Clear Requirements**: Explicitly lists 5 required specialists
- **Combinatorial Challenge**: Requires 5 specific specialists, only ~40% availability
  - Probability all 5 available: 0.4^5 = 1% (extremely unlikely!)
- **Medical Complexity**: Requires genuine domain expertise
- **Time Pressure**: Urgent case requiring immediate consultation

## What You'll See in Live Demo

### Successful Run (Rare)
- Manager calls `list_all_specialists()` to see roster
- Checks each required specialist with `check_specialist_availability()`
- Forms optimal team from available specialists
- Documents limitations when critical expertise missing

### Failed Run (Common)
- Manager doesn't check availability
- Attempts handoff to unavailable specialist → **CRASH**
- Or picks wrong specialists (e.g., Pain Management instead of Pediatrics)
- Or proceeds without checking, gets incomplete analysis
- Or "forgets" the required specialists listed in query

## Why This Is Hard

### No Framework Support for Team Formation

**What We Need**:
```python
# Hypothetical API
query = "Pediatric patient with renal failure..."
required_roles = infer_required_roles(query)  # ["Pediatric", "Nephrology", ...]
team = TeamFormation(
    required_roles=required_roles,
    available_agents=get_available_agents(),
    fallback_strategy="best_available_with_documentation"
)
manager.execute(query, team=team)
```

**What We Actually Have**:
```python
# Manual everything
manager_instructions = """
You have 10 specialists. You MUST:
1. Call list_all_specialists() to see who's available
2. Call check_specialist_availability() for each specialist you want
3. If unavailable, find alternative
4. Hand off to available specialists only
5. Document limitations
"""
# Hope the LLM follows instructions correctly!
```

### Brittle LLM-Dependent Logic

- Query explicitly states "This case REQUIRES: Pediatric Specialist, Nephrology Specialist, ..."
- Manager must:
  1. Parse query to extract required roles
  2. Remember these roles during execution
  3. Check each role's availability
  4. Adapt when roles unavailable
  5. Form optimal team from available agents
- **All logic is in natural language instructions** - no programmatic guarantees

### Combinatorial Explosion

- 10 specialists × 40% availability = ~4 available (varies each run)
- Query requires 5 specific specialists
- Probability all required specialists available: **1%**
- Manager must adapt ~99% of the time
- No systematic adaptation strategy

## Key Insights

### ✅ What Agent SDKs Provide
- Basic handoff mechanism
- Tool calling
- Shared context (with manual plumbing)

### ❌ What's Missing
1. **Team Formation Primitives**: No native support for "form team based on requirements"
2. **Requirement Matching**: No way to say "this query requires these roles"
3. **Availability Management**: No built-in roster/availability tracking
4. **Fallback Strategies**: No framework for handling unavailable specialists
5. **Verification**: Manual validation hooks required to enforce availability
6. **Observability**: Hard to debug "why did manager pick wrong team?"

### Production Implications

**Time to Build**:
- Specialist roster system: 1-2 days
- Availability tools: 1 day
- Validation hooks: 1 day
- Testing all failure modes: 2-3 days
- **Total**: ~1 week for basic ad-hoc teaming

**Maintenance Burden**:
- Every new specialist requires updates across multiple files
- Availability logic scattered (context, tools, hooks, instructions)
- Team formation logic encoded in LLM instructions (drift over time)
- Hard to systematically test all availability combinations

**Debugging Challenges**:
- Why did manager pick Geriatric Specialist instead of Pediatric?
- Did manager ever call `list_all_specialists()`?
- Which specialists were available during this run?
- How to replay with same availability configuration?

## Code Structure

```
example_2/
├── resources/
│   └── team_roster.py           # Specialist roles, availability context
├── tools/
│   └── specialist_availability.py  # check_specialist_availability, list_all_specialists
├── agents.py                    # Create all 10+ specialist agents + manager
├── hooks.py                     # SpecialistAvailabilityHook (validation)
├── consts.py                    # The "greatest query" (designed to fail)
├── main.py                      # Initialize random availability, run demo
└── README.md                    # This file
```

## Running the Example

```bash
python -m src.examples.example_2.main
```

**What You'll See**:
1. Roster display showing random availability (e.g., "4/10 specialists available")
2. Manager attempts to form team
3. Likely failures:
   - Handoff violation (attempted unavailable specialist)
   - Wrong team composition (suboptimal specialists)
   - Incomplete analysis (missing critical expertise)
   - Manager confusion (forgets requirements, doesn't check availability)

## Discussion Points for Tutorial

1. **Is this realistic?** Yes - healthcare, legal, consulting all have variable expert availability

2. **Why so hard?** No native team formation primitives in agent SDKs

3. **What's the fix?** Need framework support for:
   - Declarative team requirements ("this query needs these roles")
   - Automatic availability checking
   - Intelligent fallback strategies
   - Systematic team formation algorithms

4. **Production impact?** Every team wastes 1-2 weeks building custom roster management

## Learning Outcomes

After this demo, participants understand:

1. ✅ **Ad-hoc teaming is critical** - real environments have variable availability
2. ✅ **Current SDKs don't support it** - all team formation is manual + brittle
3. ✅ **LLM-dependent logic is fragile** - manager may ignore requirements, forget to check availability
4. ✅ **Production systems need frameworks** - not DIY solutions for each project

## Next Steps

**Example 3** introduces **multi-objective preferences** with **event-driven priority changes** - the system must adapt when a crisis occurs mid-execution, switching from thorough audit to rapid response.

---

**The Big Question**: "If ad-hoc teaming is this hard with one manager and 10 specialists, how do we build systems with hundreds of agents and dynamic team formation at scale?"

*[Transition to your tool pitch]*

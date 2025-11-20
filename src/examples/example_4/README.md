# Example 4: Safety & Governance - Human-in-the-Loop

## Overview

This example demonstrates **why AI agents need human oversight** in high-stakes domains, using a healthcare medication audit scenario where agents have access to dangerous tools that can propose medication changes.

## The Scenario

The audit team is investigating urgent medication safety alerts in ICU patients:

1. **Patient P-67890**: Receiving 10mg warfarin daily (prescribed 5mg) - appears to be double dosing for 3 days
2. **Patient P-67891**: On warfarin + ibuprofen (NSAID) - dangerous drug interaction with bleeding risk  
3. **Patient P-67892**: Receiving amoxicillin despite documented penicillin allergy - anaphylaxis risk

These are **critical safety issues** that appear to require immediate intervention. The question is: should AI agents be allowed to fix these problems directly?

### Example 4 Mock Data

Example 4 uses **specialized mock data** (in `data/` subdirectory) showing realistic safety scenarios:
- `example_4_medication_records.json` - 10 ICU records with apparent safety issues
- `example_4_prescriptions.py` - Prescriptions showing discrepancies (e.g., P-67890 prescribed 5mg, receiving 10mg)
- `example_4_patients.py` - Patient medical histories with clinical context

**Note**: To run Example 4 with this data, you would need to update the core tools to use these records, or integrate this data into the main `src/core/data/` directory. The data structure demonstrates realistic scenarios where AI might propose dangerous "fixes."

**The twist**: Issues #1 and #2 would be false positives (physician had good reasons), but #3 is a true positive (legitimate danger). This shows agents can't distinguish without human oversight.

## The Dangerous Tool

### `submit_medication_change_order`

The Safety Compliance Specialist has access to this tool, which allows proposing medication changes:

- **Discontinue medications** when contraindications found
- **Adjust dosages** when errors detected
- **Change medications** when dangerous interactions identified
- **Adjust timing** when administration schedules are suboptimal
- **Add monitoring** when risk factors present

### Why It's Dangerous

1. **Direct Patient Impact**: Wrong medication changes can cause serious harm or death
2. **AI Lacks Context**: Doesn't know physician's treatment goals, recent decisions, full patient history
3. **Tempting to Use**: When agents find real problems, they naturally want to fix them
4. **Realistic Scope Creep**: Systems designed for observation often expand into action

## The Safety Architecture

### Human-in-the-Loop Pattern

```
Agent Finds Issue → Evaluates Severity → Proposes Change
                                              ↓
                                    🚨 APPROVAL GATE 🚨
                                              ↓
                    Human Reviews with Full Context
                                              ↓
                                  Approves or Rejects
```

### Key Safety Features

1. **Default Block**: ALL medication changes require human approval (cannot be bypassed)
2. **Risk Assessment**: System automatically generates risk analysis for reviewers
3. **Audit Trail**: All attempts to use dangerous tools are logged
4. **Clear Warnings**: Agents receive explicit warnings about approval requirements
5. **Tracking**: Order IDs allow tracking from submission through approval/rejection

## What You'll See

1. **Agent Workflow**:
   - Manager creates audit plan
   - Compliance Auditor finds medication issues
   - Patient Data Specialist gathers context
   - Safety Specialist evaluates and proposes changes
   - Audit Reporter generates final report

2. **Dangerous Tool Usage**:
   - Safety Specialist identifies critical issues
   - Submits medication change orders with justification
   - Orders are **BLOCKED** pending human approval
   - System displays clear warnings

3. **Approval Queue**:
   - All submitted orders shown at end
   - Risk assessment presented for each
   - Status: "pending" (blocked)
   - Waiting for human authorization

## Why This Matters

### The Temptation is Natural

When the agent finds a patient receiving **double the prescribed dosage** of a blood thinner, the logical response is: "This is dangerous! I should reduce the dose immediately!"

### The Danger is Hidden

What the agent doesn't know:
- Physician intentionally increased the dose yesterday
- Patient had a blood clot requiring aggressive treatment
- INR levels are being monitored and are therapeutic
- Prescription system update is pending (admin delay)
- **Reducing the dose could cause another life-threatening clot**

### The Solution is Architectural

- Agent submits order → **BLOCKED**
- Physician reviews with full context → **REJECTS**
- Patient safety maintained → **HARM PREVENTED**

## Key Teaching Points

### 1. AI Strengths & Limitations

**AI Excels At**:
- Pattern detection across large datasets
- Finding anomalies and potential issues
- Consistent application of rules
- Never getting tired or distracted

**AI Struggles With**:
- Understanding full clinical context
- Knowing recent physician decisions not in records
- Assessing complex risk/benefit tradeoffs
- Clinical judgment requiring years of training

### 2. Human-in-the-Loop Benefits

**Not a Limitation, but a Feature**:
- Combines AI pattern detection with human judgment
- Prevents harm from incomplete information
- Maintains accountability (humans make final decisions)
- Builds trust through transparency

**Trade-offs**:
- Speed: Human review adds latency (minutes to hours)
- Scalability: Requires human availability
- Consistency: Humans may disagree with each other
- Cost: Human time is expensive

### 3. Broader Applications

This pattern applies to many high-stakes domains:

| Domain | Dangerous Actions | Human Approval |
|--------|-------------------|----------------|
| 🏥 Healthcare | Medication changes, diagnoses | Licensed providers |
| 💰 Finance | Large transactions, investments | Compliance officers |
| ⚖️ Legal | Contract terms, legal advice | Licensed attorneys |
| 🏭 Manufacturing | Equipment shutdown, process changes | Safety engineers |
| ⚔️ Military | Weapons authorization | Command authority |

## Running the Example

```bash
# Run Example 4
python -m src.examples.example_4.main

# You'll see:
# 1. Manager creates audit plan
# 2. Agents execute tasks sequentially
# 3. Safety Specialist finds issues and proposes changes
# 4. Orders are BLOCKED with warnings
# 5. Approval queue displayed at end
```

## Discussion Questions

1. **Boundary**: Where should we draw the line between AI observation and action?

2. **Accuracy**: What if the AI is 99% accurate? Should it act then?
   - Consider: In healthcare, 1% errors on thousands of cases = many harmed patients

3. **Speed**: How do we balance urgency vs. safety?
   - Emergency cases need fast response
   - But fast wrong decisions cause harm
   - Could we have rapid approval workflows?

4. **Trust**: How do we prevent "approval fatigue"?
   - Humans might start rubber-stamping
   - Need to maintain vigilance
   - UI/UX design is critical

5. **Evolution**: Should approval requirements change as AI improves?
   - What metrics prove AI is "good enough"?
   - Who decides the threshold?
   - What about edge cases AI still misses?

6. **Liability**: Who's responsible if an approved AI suggestion causes harm?
   - The AI developer?
   - The human who approved it?
   - The institution deploying it?

## Code Structure

```
example_4/
├── __init__.py
├── consts.py           # TITLE, TASK, SUMMARY
├── agents.py           # Team with Safety Specialist (dangerous tool access)
├── main.py             # Execution with approval queue display
└── README.md           # This file
```

## Related Files

- `src/core/tools/medication_orders.py` - Dangerous tool implementation
- `src/core/tools/DANGEROUS_TOOLS_EXPLANATION.md` - Deep dive explanation
- `DANGEROUS_TOOL_INTEGRATION.md` - Integration guide
- `README_DANGEROUS_TOOLS.md` - Quick reference

## Learning Outcomes

After running this example, participants should understand:

1. ✅ **Why dangerous tools need approval gates** - Concrete examples of AI limitations
2. ✅ **How to architect human-in-the-loop systems** - Approval workflows, audit trails
3. ✅ **Trade-offs in AI safety** - Speed vs. safety, automation vs. oversight
4. ✅ **Broader implications** - Pattern applies beyond healthcare
5. ✅ **Responsible AI development** - Safety by design, not as afterthought

## Progression Through Examples

- **Example 0**: Single agent, single record (baseline)
- **Example 1**: Manager coordinates multiple workers (scale)
- **Example 2**: Specialist joins mid-audit (ad hoc teaming)
- **Example 3**: Event-driven priority changes (multi-objective preferences)
- **Example 4**: Dangerous actions require approval (**safety & governance**) ⭐

Each example reveals limitations that drive the need for more sophisticated management and governance.

## Next Steps

1. Run the example and observe agent behavior
2. Review the approval queue and risk assessments
3. Discuss with your team: Where else do you need human-in-the-loop?
4. Consider: How would you implement the human approval side?
5. Think about: What other "dangerous tools" exist in your domain?

---

**Remember**: The goal isn't to limit AI capabilities, but to deploy them safely and responsibly in high-stakes environments. Human-in-the-loop is a feature that enables trust and prevents harm.


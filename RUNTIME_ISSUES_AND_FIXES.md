# Runtime Issues and Fixes

This document catalogs runtime issues encountered during development and testing of the multi-agent system examples, along with their fixes and workarounds.

## Issue Categories

### 1. Agent Behavior Issues

#### Issue: Workers Not Executing Tools After Handoff
**Symptoms:**
- Worker agent receives handoff from manager
- Agent acknowledges handoff but doesn't call any tools
- Agent ends without completing assigned task

**Root Cause:**
- Instructions were too implicit - agents didn't understand they needed to immediately execute tools
- No explicit protocol for handling handoffs

**Fix Applied:**
- Added "CRITICAL HANDOFF PROTOCOL" section to all worker agent instructions
- Explicit 5-step protocol:
  1. IMMEDIATELY identify assigned task
  2. EXECUTE THE APPROPRIATE TOOLS IMMEDIATELY
  3. Use specific tools listed
  4. Summarize findings
  5. Hand back to manager

**Files Changed:**
- `src/examples/example_1/agents.py`
- `src/examples/example_2/agents.py`
- `src/examples/example_3/agents.py`

**Status:** ✅ Fixed (but requires explicit prompting - see "Better Solutions" below)

---

#### Issue: Workers Not Handing Back to Manager
**Symptoms:**
- Worker completes task but doesn't hand control back to manager
- Manager waits indefinitely for results
- Workflow stalls

**Root Cause:**
- Workers had no handoff capability configured
- Instructions didn't explicitly require handback

**Fix Applied:**
1. **Code Fix:** Enabled bidirectional handoffs in `create_manager_agent()`:
   - Workers can now hand back to manager and other workers
   - Manager is included in each worker's handoff list

2. **Instruction Fix:** Added explicit requirement:
   - "You MUST explicitly hand back to the Audit Manager Agent - do NOT end without handing back"
   - "Do NOT end your response without handing back"

**Files Changed:**
- `src/core/agent_utils/base.py` (bidirectional handoffs)
- All example agent instruction files

**Status:** ✅ Fixed (but requires explicit prompting - see "Better Solutions" below)

---

#### Issue: Workers Attempting to Use Planning Tools
**Symptoms:**
- Worker agent tries to call `update_plan_item` or `create_audit_plan`
- SDK returns "Tool not found" error
- Agent gets confused

**Root Cause:**
- Planning tools are manager-only (correctly restricted)
- Worker instructions didn't explicitly prohibit planning tool usage
- Agent inferred it should update plans based on context

**Fix Applied:**
- Added explicit prohibition: "Do NOT use planning tools (create_audit_plan, update_plan_item, etc.) - only the [Manager] Agent manages plans."
- Added to all worker agent instructions

**Files Changed:**
- All example agent instruction files

**Status:** ✅ Fixed (SDK correctly blocks + instructions prevent attempts)

---

#### Issue: Multiple Handoffs Error
**Symptoms:**
- Manager tries to hand off to multiple agents simultaneously
- SDK error: "Multiple handoffs requested"
- Workflow fails

**Root Cause:**
- OpenAI Agents SDK only supports sequential handoffs (one at a time)
- Manager instructions didn't clarify this limitation
- Manager tried to parallelize work

**Fix Applied:**
- Updated manager instructions to explicitly state:
  - "Hand off to ONE agent at a time (handoffs are sequential, not parallel)"
  - Added workflow pattern: hand off → wait for results → mark complete → next agent
  - Clarified that parallelism must be achieved through sequential coordination

**Files Changed:**
- `src/examples/example_1/agents.py` (manager instructions)
- `src/examples/example_2/agents.py` (manager instructions)
- `src/examples/example_3/agents.py` (manager instructions)

**Status:** ✅ Fixed (SDK limitation, workaround documented)

---

### 2. Configuration Issues

#### Issue: Running Out of Turns
**Symptoms:**
- Agent execution stops prematurely
- Complex multi-step workflows incomplete
- No error, just stops

**Root Cause:**
- Default `max_turns` too low for complex workflows
- Multi-agent coordination requires many turns

**Fix Applied:**
- Set `max_turns=50` for all examples
- Applied to all `Runner.run_streamed()` calls

**Files Changed:**
- `src/examples/example_0/main.py`
- `src/examples/example_1/main.py`
- `src/examples/example_2/main.py`
- `src/examples/example_3/main.py`

**Status:** ✅ Fixed

**Note:** May need to increase further for very complex workflows. Consider making configurable.

---

#### Issue: Parallel Tool Calling Not Enabled
**Symptoms:**
- Agents call tools sequentially even when independent
- Slower execution than necessary
- Missed opportunity for efficiency

**Root Cause:**
- `ModelSettings` didn't enable `parallel_tool_calls`
- Default is sequential tool execution

**Fix Applied:**
- Set `parallel_tool_calls=True` in all agent creation
- Applied globally in `create_agent()` and `create_manager_agent()`

**Files Changed:**
- `src/core/agent_utils/base.py`

**Status:** ✅ Fixed

---

### 3. Observability Issues

#### Issue: Poor Visibility into Agent Activity
**Symptoms:**
- Hard to see what agents are doing
- Tool calls not visible
- Tool inputs/outputs not displayed
- No way to debug agent behavior

**Root Cause:**
- Basic streaming output didn't format tool calls well
- No structured display of tool execution

**Fix Applied:**
- Enhanced `stream_agent_output()` in `src/core/agent_utils/streaming.py`:
  - Formatted tool calls with Title Case names
  - Displayed tool parameters as bullet points
  - Pretty-printed JSON outputs
  - Highlighted errors
  - Tracked pending tool calls and matched with results
  - Improved text filtering and display

**Files Changed:**
- `src/core/agent_utils/streaming.py`

**Status:** ✅ Fixed

---

## Better Solutions (Not Yet Implemented)

### 1. Use Stronger Models for Workers
**Current State:**
- All agents use `claude-haiku-4-5` (fast but less capable)
- Requires very explicit instructions to follow protocols

**Better Solution:**
- Use stronger model (e.g., `claude-sonnet-4-5`) for workers
- More capable of following implicit instructions
- Better at understanding handoff protocols
- Trade-off: Higher cost and latency

**Implementation:**
```python
# In base.py, make model configurable per role
def create_agent(..., worker_model: str = "claude-sonnet-4-5"):
    # Use stronger model for workers
```

**Status:** ⚠️ Not implemented (cost/latency trade-off)

---

### 2. Agents as Tools Pattern
**Current State:**
- Agents hand off to each other directly
- True multi-agent system with handoffs

**Alternative Pattern:**
- Manager calls worker agents as tools
- Workers become function-callable tools
- More deterministic, easier to control

**Trade-offs:**
- ✅ More predictable behavior
- ✅ Easier to debug
- ✅ Better error handling
- ❌ Less "true" multi-agent system
- ❌ Workers can't initiate handoffs
- ❌ Less dynamic collaboration

**Status:** ⚠️ Not implemented (design choice - want true MAS)

---

### 3. Structured Handoff Protocol
**Current State:**
- Handoffs rely on natural language instructions
- No structured protocol enforcement

**Better Solution:**
- Define structured handoff format (JSON schema)
- Require specific fields: task_id, context, expected_output
- Validate handoff format before accepting
- Could use Pydantic models for handoff requests/responses

**Status:** ⚠️ Not implemented (SDK limitation - handoffs are free-form)

---

### 4. Tool Availability Checking
**Current State:**
- Agents try to call tools they don't have
- SDK blocks with "Tool not found" error
- Agent gets confused

**Better Solution:**
- Pre-check tool availability before attempting call
- Provide clearer error messages
- Suggest alternative tools agent does have
- Could be done in custom tool wrapper

**Status:** ⚠️ Not implemented (would require SDK changes or custom wrappers)

---

### 5. Retry Logic for Failed Handoffs
**Current State:**
- If handoff fails, workflow stops
- No automatic retry or fallback

**Better Solution:**
- Implement retry logic for failed handoffs
- Fallback to alternative agent if primary unavailable
- Exponential backoff for transient failures
- Would require custom Runner wrapper

**Status:** ⚠️ Not implemented (complexity vs. benefit)

---

## Current Limitations

### SDK Limitations
1. **Sequential Handoffs Only:** Cannot hand off to multiple agents simultaneously
2. **Free-form Handoffs:** No structured protocol enforcement
3. **No Handoff Rejection:** Cannot programmatically reject handoffs (would need hooks)
4. **Limited Observability:** Some events not easily accessible

### Model Limitations
1. **Instruction Following:** Requires very explicit instructions
2. **Context Window:** Long conversation histories may hit limits
3. **Cost:** Stronger models increase API costs significantly
4. **Latency:** Sequential handoffs + API calls = slow execution

### Design Trade-offs
1. **Explicit vs. Implicit:** More explicit = more verbose but more reliable
2. **Cost vs. Capability:** Stronger models = better behavior but higher cost
3. **MAS vs. Tool Pattern:** True MAS = more dynamic but harder to control

---

## Recommendations

### For Production Use:
1. **Use stronger models** for critical agents (manager + key workers)
2. **Implement structured handoff protocol** using custom wrappers
3. **Add retry logic** for failed operations
4. **Monitor turn counts** and adjust `max_turns` dynamically
5. **Implement tool availability checking** before calls

### For Demo/Tutorial:
1. **Current approach is acceptable** - explicit instructions work
2. **Document limitations** clearly for audience
3. **Show trade-offs** between approaches
4. **Demonstrate debugging** techniques (streaming output, tool visibility)

---

## Summary

**Issues Fixed:**
- ✅ Workers not executing tools (explicit protocol)
- ✅ Workers not handing back (bidirectional handoffs + instructions)
- ✅ Workers using wrong tools (explicit prohibitions)
- ✅ Multiple handoffs error (sequential pattern)
- ✅ Running out of turns (max_turns=50)
- ✅ Poor observability (enhanced streaming)
- ✅ Parallel tool calling (enabled globally)

**Remaining Challenges:**
- ⚠️ Heavy reliance on explicit prompting (not ideal)
- ⚠️ SDK limitations (sequential handoffs, free-form protocol)
- ⚠️ Model limitations (instruction following, cost)
- ⚠️ No structured error recovery

**Key Insight:**
Multi-agent systems with LLMs require **much more explicit instructions** than single-agent systems. The coordination overhead is significant, and agents need clear protocols to follow. This is a fundamental challenge of LLM-based MAS, not just a bug to fix.


"""Main execution for Example 4: Safety & Governance."""

import asyncio
from agents import Runner

from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_4.agents import create_team
from src.examples.example_4.consts import SUMMARY, TASK, TITLE


async def main():
    """Run Example 4: Safety & Governance with human-in-the-loop."""
    print("=" * 80)
    print(TITLE)
    print("=" * 80)
    print()

    print("⚠️  WARNING: This example includes DANGEROUS TOOL DEMONSTRATIONS")
    print("Agents will have access to submit_medication_change_order(), which")
    print("proposes medication changes. All changes require human approval.")
    print()
    print(f"Task: {TASK}")
    print()
    print("Running manager agent with safety governance...")
    print("-" * 80)

    manager = create_team()
    runner = Runner.run_streamed(manager, input=TASK, max_turns=100)
    await stream_agent_output(runner)

    print()
    print("-" * 80)
    print()
    
    # Explain what happened with dangerous tools
    print("=" * 80)
    print("⚠️  DANGEROUS TOOL DEMONSTRATION")
    print("=" * 80)
    print()
    print("During this audit, the Safety Compliance Specialist had access to:")
    print("  • submit_medication_change_order() - Proposes medication changes")
    print("  • list_pending_approval_requests() - Views approval queue")
    print("  • get_order_status() - Checks order status")
    print()
    print("If the agent identified critical safety issues (such as double dosing,")
    print("drug interactions, or allergy violations), it would have attempted to")
    print("submit medication change orders.")
    print()
    print("🚨 ALL ORDERS BLOCKED BY APPROVAL GATE:")
    print("   • Orders automatically set to approval_status='pending'")
    print("   • Risk assessments generated for human reviewers")
    print("   • Complete audit trail created")
    print("   • NO changes implemented without human authorization")
    print()
    print("📋 TO BUILD THE APPROVAL SYSTEM, YOU WOULD NEED:")
    print("   1. Web interface for human reviewers (physicians)")
    print("   2. Authentication & authorization (MFA, role-based access)")
    print("   3. Order management (approve/reject with reasoning)")
    print("   4. Real-time notifications (urgent cases)")
    print("   5. Audit trail & compliance reporting")
    print("   6. Integration with EHR/hospital systems")
    print()
    print("See src/core/tools/medication_orders.py for the dangerous tool implementation")
    print("and the _MEDICATION_ORDERS and _APPROVAL_REQUESTS storage for order tracking.")
    print()
    print("-" * 80)
    print()
    print("Example Complete!")
    print()
    for line in SUMMARY:
        print(line)
    print()
    
    print("=" * 80)
    print("KEY LESSON: Human-in-the-Loop for High-Stakes AI")
    print("=" * 80)
    print()
    print("This example demonstrates that:")
    print("  🤖 AI excels at: Pattern detection, finding anomalies, proposing solutions")
    print("  👨‍⚕️ Humans essential for: Contextual judgment, authorization, accountability")
    print("  🛡️  Safety architecture: Approval gates prevent AI from acting on incomplete information")
    print("  📋 Audit trails: All dangerous action attempts are logged for governance")
    print()
    print("Together, AI + Human oversight creates safer and more effective systems")
    print("than either could achieve alone.")
    print()


if __name__ == "__main__":
    asyncio.run(main())


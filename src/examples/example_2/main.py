"""Main execution for Example 2: Ad Hoc Teaming with Dynamic Roster."""

import asyncio
import os
from agents import Agent, Runner
from typing import Any

from src.core.agent_utils.reporting import generate_and_save_report
from src.core.agent_utils.streaming import stream_agent_output
from src.examples.example_2.agents import create_team
from src.examples.example_2.consts import PRE_RUN_INFO, SUMMARY, TASK, TITLE
from src.examples.example_2.resources.team_roster import CoreTeamRole, SpecialistRole, TeamRosterContext


async def main(manual_availability: list[SpecialistRole] | None = None):
    """
    Run Example 2: Ad hoc teaming with dynamic roster.
    
    Args:
        manual_availability: Optional list of specialists to make available.
                            If None, will be randomly determined (40% probability each).
                            
    Example manual configurations:
        # Make only Clinical Pharmacist available (force suboptimal choices)
        manual_availability = [SpecialistRole.CLINICAL_PHARMACIST]
        
        # Make Cardiology but not Anticoagulation available (for warfarin case)
        manual_availability = [
            SpecialistRole.CARDIOLOGY_PHARMACIST,
            SpecialistRole.CLINICAL_PHARMACIST
        ]
        
        # Make all specialists available (ideal scenario)
        manual_availability = list(SpecialistRole)
    """
    print("=" * 80)
    print(TITLE)
    print("=" * 80)
    print()

    # Print pre-run information
    for line in PRE_RUN_INFO:
        print(line)
    print()

    # Create shared context
    context = TeamRosterContext()
    
    # Create team with specified or random availability
    manager, available_specialists, unavailable_specialists = create_team(
        available_specialists=manual_availability
    )
    
    # Update context with final availability
    context.specialist_availability = {
        role.value: (role in available_specialists)
        for role in SpecialistRole
    }
    
    print("📋 TEAM ROSTER - AVAILABILITY STATUS")
    print("=" * 80)
    
    # Core team - always available
    print(f"✅ CORE TEAM (ALWAYS AVAILABLE - {len(list(CoreTeamRole))} agents):")
    for role in CoreTeamRole:
        print(f"   - {role.value}")
    print()
    
    # Specialist pharmacists - variable availability
    print(f"🔬 SPECIALIST PHARMACISTS (Variable Availability):")
    print("-" * 80)
    if available_specialists:
        print(f"✅ AVAILABLE ({len(available_specialists)}):")
        for role in available_specialists:
            print(f"   - {role.value}")
    else:
        print("✅ AVAILABLE (0):")
        print("   - None available")
    print()
    if unavailable_specialists:
        print(f"❌ UNAVAILABLE ({len(unavailable_specialists)}):")
        for role in unavailable_specialists:
            print(f"   - {role.value}")
    else:
        print("❌ UNAVAILABLE (0):")
        print("   - All specialist pharmacists available!")
    print()
    
    total_available = len(list(CoreTeamRole)) + len(available_specialists)
    total_roster = len(list(CoreTeamRole)) + len(list(SpecialistRole))
    print(f"📊 TOTAL AVAILABLE: {total_available}/{total_roster} agents ({int(100*total_available/total_roster)}%)")
    print("   Manager should form team of 9-15+ agent assignments from available roster.")
    print("=" * 80)
    print()

    print(f"Task: {TASK}")
    print()
    print("Running manager with pre-determined team roster...")
    print("-" * 80)

    runner = Runner.run_streamed(manager, input=TASK, context=context, max_turns=100)
    final_agent = await stream_agent_output(runner, context=context)

    # Use final agent if available, otherwise use manager
    report_agent: Agent[Any] = final_agent if final_agent else manager

    # Generate and save final report
    await generate_and_save_report(
        agent=report_agent,
        task_description=TASK,
        example_name="example_2",
        context=context,
    )

    print()
    print("-" * 80)
    print()
    print("Example Complete!")
    print()
    
    # Display team formation if declared
    if context.team_formation:
        print()
        print("=" * 80)
        print("📋 FINAL TEAM FORMATION DECLARED BY MANAGER")
        print("=" * 80)
        team_members = context.team_formation.get("team_members", [])
        limitations = context.team_formation.get("limitations", [])
        
        print(f"\nTotal Team Size: {len(team_members)} agents")
        print()
        
        if team_members:
            print("TEAM ASSIGNMENTS:")
            print("-" * 80)
            for i, member in enumerate(team_members, 1):
                print(f"\n{i}. {member['agent_name']}")
                print(f"   └─ Assigned to: {member['assigned_to']}")
                print(f"   └─ Rationale: {member['rationale']}")
            print()
            print("-" * 80)
        
        if limitations:
            print("\n⚠️  EXPERTISE LIMITATIONS DOCUMENTED:")
            for limitation in limitations:
                print(f"   - {limitation}")
            print()
        else:
            print("\n✅ Optimal team formed with no expertise limitations")
            print()
        
        # Analyze team composition
        print("\nTEAM COMPOSITION ANALYSIS:")
        print(f"   Target: 9-15 agent assignments for comprehensive 3-patient audit")
        if len(team_members) < 6:
            print(f"   ⚠️  INSUFFICIENT team ({len(team_members)} assignments) - Lacks comprehensive coverage")
            print(f"      Manager should assign multiple specialists per patient for different sub-tasks")
        elif len(team_members) >= 6 and len(team_members) < 9:
            print(f"   ⚠️  Small team ({len(team_members)} assignments) - Minimal coverage")
            print(f"      Could improve by assigning more specialists to sub-tasks")
        elif len(team_members) >= 9 and len(team_members) <= 15:
            print(f"   ✅ Good team size ({len(team_members)} assignments) - Appropriate specialist coverage")
        else:
            print(f"   ✅ Large team ({len(team_members)} assignments) - Comprehensive specialist coverage")
        
        print("=" * 80)
        print()
    else:
        print()
        print("=" * 80)
        print("⚠️  FAILURE: Manager did NOT declare team formation!")
        print("=" * 80)
        print("   This is a critical failure mode - manager should explicitly state team composition")
        print("   using the declare_team_formation() tool before beginning audits.")
        print("=" * 80)
        print()
    
    print("FINAL ANALYSIS:")
    print(f"  Total Handoff Attempts: {len(context.handoff_attempts)}")
    successful_handoffs = [a for a in context.handoff_attempts if a['successful']]
    failed_handoffs = [a for a in context.handoff_attempts if not a['successful']]
    print(f"  Successful Handoffs: {len(successful_handoffs)}")
    if successful_handoffs:
        print(f"    Agents Used: {set([a['target'] for a in successful_handoffs])}")
    print(f"  Failed Handoffs: {len(failed_handoffs)}")
    if failed_handoffs:
        for fail in failed_handoffs:
            print(f"    ❌ {fail['source']} tried to hand to {fail['target']} (UNAVAILABLE)")
    print()
    for line in SUMMARY:
        print(line)
    print()


if __name__ == "__main__":
    # Check for manual availability configuration via environment variable
    # Example: SPECIALIST_CONFIG="clinical,id,icu" python -m src.examples.example_2.main
    # Note: Only Specialist Pharmacists have variable availability
    # Core Team is always available and doesn't need to be specified
    manual_config = os.environ.get("SPECIALIST_CONFIG")
    if manual_config:
        role_mapping = {
            # Specialized Pharmacists (variable availability)
            "anticoag": SpecialistRole.ANTICOAGULATION_SPECIALIST,
            "oncology": SpecialistRole.ONCOLOGY_PHARMACIST,
            "id": SpecialistRole.INFECTIOUS_DISEASE_PHARMACIST,
            "icu": SpecialistRole.ICU_CRITICAL_CARE_PHARMACIST,
            "cardiology": SpecialistRole.CARDIOLOGY_PHARMACIST,
            "clinical": SpecialistRole.CLINICAL_PHARMACIST,
        }
        config_roles = [role_mapping[key.strip()] 
                       for key in manual_config.split(",") 
                       if key.strip() in role_mapping]
        print(f"🔧 Manual Configuration (Specialist Pharmacists): {[r.value for r in config_roles]}")
        print(f"   Note: Core Team (6 agents) always available automatically")
        print()
        asyncio.run(main(manual_availability=config_roles))
    else:
        # Random availability for specialist pharmacists
        asyncio.run(main())

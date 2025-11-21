"""Constants for Example 2 - Ad Hoc Teaming with Dynamic Roster."""

# Example metadata
TITLE = "Example 2: Ad Hoc Teaming - Dynamic Team Formation"

# THE "GREATEST QUERY" - Realistic stakeholder communication
# Designed to show ad-hoc teaming failures without prescriptive instructions
TASK = (
    "Subject: URGENT - Three High-Risk ICU Patients Need Immediate Review\n\n"
    "I need your team to review three critical ICU cases that were flagged overnight. "
    "The night shift is concerned about medication safety issues that need expert eyes on them ASAP.\n\n"
    "PATIENT P001 (ICU Bed 3):\n"
    "65yo male with atrial fibrillation. Started on amiodarone yesterday for arrhythmia control. "
    "He's also on warfarin for stroke prevention. Night nurse is worried - his INR jumped from "
    "2.1 to 3.8 overnight. Records: REC-12345, REC-12346, REC-12350.\n\n"
    "PATIENT P002 (ICU Bed 7):\n"
    "45yo female with breast cancer on chemotherapy (doxorubicin). She spiked a fever overnight "
    "and was started on meropenem for suspected neutropenic fever. Morning labs show WBC 0.8, "
    "platelets 45k. She's still getting her daily aspirin. Records: REC-12347, REC-12351, REC-12352.\n\n"
    "PATIENT P003 (ICU Bed 12):\n"
    "78yo male with COPD and heart failure. Respiratory therapist is concerned - respiratory rate "
    "dropped to 8, O2 sat 88%. He's on morphine PRN for pain and just started midazolam for agitation. "
    "Nurse notes he's been getting 12mg morphine doses, but I thought the order was for 10mg? "
    "Records: REC-12348, REC-12349, REC-12353.\n\n"
    "Can you coordinate a review of these three cases? I know it's a lot, but they all need "
    "attention today. Use whoever's available on your team - I'm not sure who's on shift right now. "
    "We just need to make sure we're not missing anything critical that could harm these patients.\n\n"
    "Please get back to me with findings and any urgent recommendations.\n\n"
    "Thanks,\n"
    "Dr. Sarah Chen\n"
    "ICU Medical Director"
)

PRE_RUN_INFO = [
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "Example 2: Ad-Hoc Team Formation",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "",
    "Scenario: ICU Medical Director sends urgent request to review 3 critical patients",
    "",
    "Clinical Issues:",
    "  • P001: Warfarin-Amiodarone interaction (INR 2.1 → 3.8)",
    "  • P002: Chemo patient with febrile neutropenia + aspirin (platelets 45k)",  
    "  • P003: Morphine overdose + respiratory depression (RR=8, SpO2=88%)",
    "",
    "Roster: 12 agents total",
    "  • 6 Core Team (always available): Records, Data, Lab, Drug Interactions, Compliance, Prescriptions",
    "  • 6 Specialist Pharmacists (variable): Anticoagulation, Oncology, ID, ICU, Cardiology, Clinical",
    "",
    "What to watch for:",
    "  → Does manager form a comprehensive team using diverse specialists?",
    "  → Does manager leverage Core Team + Specialist Pharmacists together?",
    "  → How does manager handle missing optimal specialists?",
    "  → Does manager assign multiple agents per patient or just one?",
]

SUMMARY = [
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "What Just Happened?",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    "",
    "The manager received an urgent request from the ICU Medical Director to review 3 critical",
    "patients. Each patient has different medication safety concerns requiring specialized expertise.",
    "",
    "Common Failure Modes You May Have Seen:",
    "  ❌ Only assigned 3 agents (one per patient) despite having 9+ available",
    "  ❌ Didn't use Core Team specialists (Lab Results, Drug Interaction Analyst)",
    "  ❌ Attempted handoff to unavailable specialist → Runtime crash",
    "  ❌ Used Clinical Pharmacist for chemo case (should prioritize Oncology if available)",
    "  ❌ Didn't declare team formation upfront",
    "  ❌ Didn't document expertise limitations",
    "",
    "The Core Problem:",
    "  → Agent SDKs provide NO team formation primitives",
    "  → No way to declaratively specify: 'Warfarin case needs Anticoag > Cardio > Clinical'",
    "  → No automatic matching of case requirements to specialist capabilities",
    "  → All team formation logic relies on LLM following vague instructions",
    "  → Probability of optimal team (all 5 key specialists available): ~1%",
    "",
    "What Makes This Hard:",
    "  → 12 agent roster with variable availability = combinatorial explosion",
    "  → Must manually match 'patient needs' → 'specialist expertise' → 'check availability'",
    "  → No fallback strategy when optimal specialists unavailable",
    "  → Debugging: 'Why did manager pick wrong specialist?' requires inspecting full trace",
    "",
    "Production Impact:",
    "  → 1 week to build custom roster management for each project",
    "  → Runtime crashes when manager violates availability constraints",
    "  → Suboptimal teams → degraded quality",
    "  → No systematic approach → every team reinvents the wheel",
    "",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
]

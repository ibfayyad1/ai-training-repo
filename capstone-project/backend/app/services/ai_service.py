"""
AI Service - Core AI Functions
================================
All AI-powered features in one place.
Each function is annotated with which MODULE and TECHNIQUE it uses.

MODULES USED:
- Module 01: LLM Fundamentals (temperature, tokens, context window)
- Module 02: Prompt Engineering (system prompts, few-shot, CoT, JSON format, constraints)
- Module 03: RAG (embeddings, vector search - see rag_service.py)
- Module 04: Agents (tool use, ReAct loop - see agent_service.py)
"""

import json
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


# ============================================================
# 1. CLASSIFY INCIDENT
#    Techniques: Few-Shot + CoT + JSON Format + Constraints
#    Module: 02 (Prompt Engineering)
# ============================================================

def classify_incident(description: str) -> dict:
    """
    Classify an incident report into category and severity.

    TECHNIQUES USED:
    ┌──────────────────────────────────────────────────────────┐
    │ • System Prompt (Module 02): Defines the AI's role       │
    │ • Few-Shot (Module 02): 3 examples teach the pattern     │
    │ • Chain of Thought (Module 02): "Think step by step"     │
    │ • JSON Format (Module 02): Structured output for code    │
    │ • Constraints (Module 02): "Do NOT invent info"          │
    │ • Temperature 0 (Module 01): Deterministic, consistent   │
    └──────────────────────────────────────────────────────────┘
    """

    # ---- SYSTEM PROMPT (Module 02: Role + Rules + Format) ----
    system_prompt = """You are an incident classification specialist for a government reporting system.
You process incoming incident reports and extract structured information.

CLASSIFICATION RULES:
- Categories: Traffic, Fire, Theft, Public Safety, Environmental
- Severity levels: low, medium, high, critical
- If injuries are mentioned → minimum severity = high
- If weapons, explosives, or life-threatening situations → severity = critical
- If ambiguous between categories → pick the most severe possibility

OUTPUT FORMAT:
Respond ONLY in valid JSON. No extra text.

CONSTRAINTS:
- Do NOT invent information not present in the report
- Do NOT classify as 'Other' - always pick the closest category
- If location is not mentioned, use "not specified"
- If time is not mentioned, use "not specified"
- Include your reasoning (Chain of Thought)"""

    # ---- FEW-SHOT EXAMPLES (Module 02: In-Context Learning) ----
    few_shot_examples = """
EXAMPLES:

Report: "Car hit a pedestrian near the shopping mall at 3pm. Ambulance was called."
Output: {"category": "Traffic", "severity": "high", "location": "shopping mall area", "timestamp_extracted": "15:00", "summary": "Vehicle-pedestrian collision, ambulance dispatched", "confidence": 92, "reasoning": "Step 1: Vehicle + pedestrian = Traffic. Step 2: Ambulance called = injuries present. Step 3: Injuries → minimum high severity."}

Report: "Heavy smoke visible from warehouse roof in Industrial Zone B. Fire trucks on the way."
Output: {"category": "Fire", "severity": "high", "location": "Industrial Zone B", "timestamp_extracted": "not specified", "summary": "Warehouse fire with heavy smoke, fire response dispatched", "confidence": 95, "reasoning": "Step 1: Smoke + fire trucks = Fire category. Step 2: Active fire in industrial area = high severity. Step 3: No injuries mentioned but fire is active danger."}

Report: "Broken street lamp creating dark area on Road 45 near the school."
Output: {"category": "Public Safety", "severity": "low", "location": "Road 45, near school", "timestamp_extracted": "not specified", "summary": "Street lamp malfunction causing dark spot near school", "confidence": 88, "reasoning": "Step 1: Infrastructure damage, no fire/traffic/theft = Public Safety. Step 2: No injuries, no immediate danger = low severity. Step 3: Near school adds some concern but still low."}
"""

    # ---- CHAIN OF THOUGHT instruction (Module 02) ----
    cot_instruction = """
Now classify this report. Think step by step:
1. What type of incident is this? (determine category)
2. Are there injuries or danger? (determine severity)
3. Extract location and time if mentioned
4. Write a one-sentence summary
5. Rate your confidence 0-100

Respond ONLY in JSON format matching the examples above."""

    # ---- API CALL (Module 01: Temperature 0 for consistency) ----
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,           # Module 01: Temperature 0 = deterministic (same input → same output)
        max_tokens=300,          # Module 01: Limit tokens to control cost
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": few_shot_examples + "\nReport: \"" + description + "\"\n" + cot_instruction}
        ]
    )

    # Parse JSON response
    try:
        result = json.loads(response.choices[0].message.content)
        return result
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "category": "Public Safety",
            "severity": "medium",
            "location": "not specified",
            "timestamp_extracted": "not specified",
            "summary": description[:100],
            "confidence": 50,
            "reasoning": "Could not parse AI response properly"
        }


# ============================================================
# 2. ANALYZE IMAGE
#    Techniques: Vision model + structured prompt
# ============================================================

def analyze_image(image_path: str) -> str:
    """
    Analyze an incident scene image using GPT-4o Vision.

    TECHNIQUES USED:
    ┌──────────────────────────────────────────────────────────┐
    │ • (Module 01): GPT-4o can "see" images   │
    │ • Structured Prompt (Module 02): Tell it exactly what    │
    │   to look for in the scene                               │
    │ • Temperature 0.2 (Module 01): Mostly factual but        │
    │   allows slight variation in description                 │
    └──────────────────────────────────────────────────────────┘
    """

    # Read and encode the image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Determine image type
    if image_path.endswith('.png'):
        media_type = "image/png"
    else:
        media_type = "image/jpeg"

    # ---- STRUCTURED PROMPT (Module 02: Clear task + format) ----
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,       # Module 01: Slightly above 0 for natural description
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Analyze this incident scene image. Provide a detailed but concise description covering:

1. WHAT HAPPENED: What type of incident is visible?
2. VEHICLES/OBJECTS: What vehicles or objects are involved? Describe them.
3. DAMAGE: What damage is visible?
4. INJURIES: Are any injuries or people in distress visible?
5. CONDITIONS: What are the road/weather/lighting conditions?
6. SAFETY CONCERNS: Any ongoing dangers visible?

Be factual. Describe only what you can actually see in the image. Do not speculate beyond what is visible."""
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{image_data}"}
                }
            ]
        }]
    )

    return response.choices[0].message.content


# ============================================================
# 3. GENERATE FULL REPORT
#    Techniques: System Prompt + Context Injection + Temperature
#    Module: 01 + 02
# ============================================================

def generate_report(description: str, classification: dict, image_analysis: str = None) -> str:
    """
    Generate a professional incident report combining all available data.

    TECHNIQUES USED:
    ┌──────────────────────────────────────────────────────────┐
    │ • System Prompt (Module 02): Professional report writer  │
    │ • Context Injection (Module 01): Feed all known data     │
    │   into the context window                                │
    │ • Temperature 0.3 (Module 01): Natural writing style     │
    │   while staying factual                                  │
    │ • Constraints (Module 02): Structure, length, tone       │
    └──────────────────────────────────────────────────────────┘
    """

    # Build context from all available information
    context = f"""INCIDENT DATA:
Description: {description}
Category: {classification.get('category', 'Unknown')}
Severity: {classification.get('severity', 'Unknown')}
Location: {classification.get('location', 'Not specified')}
Time: {classification.get('timestamp_extracted', 'Not specified')}
AI Classification Confidence: {classification.get('confidence', 'N/A')}%
AI Reasoning: {classification.get('reasoning', 'N/A')}"""

    if image_analysis:
        context += f"\n\nIMAGE ANALYSIS:\n{image_analysis}"

    # ---- API CALL ----
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,        # Module 01: Natural writing, still factual
        max_tokens=800,
        messages=[
            {"role": "system", "content": """You are a professional incident report writer for a government system.
Generate formal, clear, and actionable incident reports.

REPORT STRUCTURE:
1. INCIDENT SUMMARY (2-3 sentences overview)
2. SCENE DESCRIPTION (what happened, based on evidence)
3. CLASSIFICATION JUSTIFICATION (why this category and severity)
4. CONTRIBUTING FACTORS (if identifiable from the data)
5. RECOMMENDED ACTIONS (what response is needed)
6. RESOURCES REQUIRED (teams, equipment needed)

CONSTRAINTS:
- Use professional, formal tone suitable for official documentation
- Do NOT invent details not supported by the provided data
- Base everything on the incident data and image analysis provided
- Keep total report under 400 words
- Use bullet points for actions and resources"""},
            {"role": "user", "content": f"Generate a professional incident report based on this data:\n\n{context}"}
        ]
    )

    return response.choices[0].message.content


# ============================================================
# 4. AI ANALYTICS - Pattern Detection
#    Techniques: Context Window + Summarization + CoT
#    Module: 01 + 02 + 03 (uses RAG-retrieved data)
# ============================================================

def analyze_patterns(incidents: list) -> str:
    """
    Analyze patterns across multiple incidents.

    TECHNIQUES USED:
    ┌──────────────────────────────────────────────────────────┐
    │ • Context Window (Module 01): Feed multiple incidents     │
    │   into context for cross-analysis                        │
    │ • Chain of Thought (Module 02): Step-by-step analysis    │
    │ • Temperature 0.4 (Module 01): Analytical but insightful │
    │ • Grounding (Module 02): "Only from provided data"       │
    └──────────────────────────────────────────────────────────┘
    """

    # Format incidents for context
    incident_text = "\n".join([
        f"- [{inc.get('report_number')}] {inc.get('category')} | {inc.get('severity')} | "
        f"{inc.get('location')} | {inc.get('created_at', '')[:10]} | {inc.get('description', '')[:100]}"
        for inc in incidents[:30]  # Limit to 30 to fit context window (Module 01)
    ])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        max_tokens=600,
        messages=[
            {"role": "system", "content": """You are a data analyst for an incident reporting system.
Analyze the provided incidents and identify patterns.

Think step by step (Chain of Thought):
1. What categories appear most frequently?
2. Are there location clusters (same area, multiple incidents)?
3. Are there time-based patterns (certain days/times)?
4. What severity distribution do you see?
5. What actionable recommendations can you make?

CONSTRAINTS:
- ONLY analyze data that is provided - do NOT invent statistics
- If data is insufficient to identify a pattern, say so
- Be specific with numbers and percentages from the actual data
- End with 2-3 concrete recommendations"""},
            {"role": "user", "content": f"Analyze these {len(incidents)} incident reports for patterns:\n\n{incident_text}"}
        ]
    )

    return response.choices[0].message.content


# ============================================================
# 5. GENERATE MONTHLY REPORT
#    Techniques: Large context + structured generation
#    Module: 01 + 02
# ============================================================

def generate_monthly_report(incidents: list, stats: dict) -> str:
    """
    Generate a comprehensive monthly report for leadership.

    TECHNIQUES USED:
    ┌──────────────────────────────────────────────────────────┐
    │ • Large Context (Module 01): All month's data in context │
    │ • Structured Output (Module 02): Executive report format │
    │ • Temperature 0.3 (Module 01): Professional writing      │
    │ • Grounding (Module 02): Only from real data             │
    └──────────────────────────────────────────────────────────┘
    """

    # Build summary of all incidents
    incident_summaries = "\n".join([
        f"- {inc.get('report_number')}: {inc.get('category')} ({inc.get('severity')}) - "
        f"{inc.get('description', '')[:80]} [{inc.get('created_at', '')[:10]}]"
        for inc in incidents[:50]
    ])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": """You are a senior analyst writing a monthly incident report for executive leadership.

REPORT STRUCTURE:
1. EXECUTIVE SUMMARY (3-4 sentences, key numbers)
2. STATISTICS OVERVIEW (use the provided stats)
3. CATEGORY BREAKDOWN (main findings per category)
4. TRENDS & PATTERNS (what changed, what's concerning)
5. HIGH-SEVERITY INCIDENTS (brief detail on critical/high)
6. RECOMMENDATIONS (3-5 actionable items)
7. RESOURCE ALLOCATION SUGGESTIONS

TONE: Professional, concise, data-driven.
CONSTRAINT: Only reference data from the provided incidents. Never invent numbers."""},
            {"role": "user", "content": f"""Generate the monthly incident report.

STATISTICS:
{json.dumps(stats, indent=2)}

INCIDENTS THIS MONTH ({len(incidents)} total):
{incident_summaries}"""}
        ]
    )

    return response.choices[0].message.content

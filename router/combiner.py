import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config.api_config import KEYS

# ── Initialize Groq for combining ───────────────
groq_client = Groq(api_key=KEYS['groq'])

# ── Intent Specific Combine Instructions ─────────
COMBINE_INSTRUCTIONS = {

    "CODING": """
    You are a Senior Software Engineer.
    Your job is to create the BEST code answer.

    Rules:
    1. Take the BEST code from lead answer
    2. Add any improvements from support answers
    3. Make sure code is clean and working
    4. Add brief explanation after code
    5. Format with proper markdown code blocks
    """,

    "COMPLEX_LOGIC": """
    You are a Expert Logician and Mathematician.
    Your job is to create the BEST logical answer.

    Rules:
    1. Use lead answer as primary reasoning
    2. Add any better explanations from support
    3. Show step by step solution clearly
    4. Make sure answer is 100% accurate
    5. End with clear final answer
    """,

    "CREATIVE_WRITING": """
    You are a Master Creative Writer.
    Your job is to create the BEST creative piece.

    Rules:
    1. Use lead answer as primary creative work
    2. Borrow best phrases from support answers
    3. Make it flow naturally and beautifully
    4. Keep consistent tone and style
    5. Output only the final creative piece
    """,

    "DATA_ANALYSIS": """
    You are a Senior Data Analyst.
    Your job is to create the BEST analysis.

    Rules:
    1. Use lead answer as primary analysis
    2. Add any insights from support answers
    3. Structure findings clearly
    4. Use bullet points for key insights
    5. End with clear conclusion
    """,

    "QUICK_ANSWER": """
    You are a helpful assistant.
    Give the direct answer only.
    No extra explanation needed.
    """,

    "GENERAL": """
    You are a world class expert.
    Your job is to create the BEST possible answer.

    Rules:
    1. Extract best parts from ALL answers
    2. Remove any wrong information
    3. Structure answer clearly
    4. Be comprehensive but concise
    5. Make it better than any single answer
    """,
}


# ── Main Combiner Function ───────────────────────

def combine_answers(
    user_question: str,
    intent: str,
    lead_model: str,
    lead_answer: str,
    support_answers: dict
) -> str:
    """
    Takes all AI answers
    Combines into ONE perfect expert answer
    """

    # ── For QUICK_ANSWER just return lead directly
    if intent == "QUICK_ANSWER" or not support_answers:
        return lead_answer

    # ── Build support answers text
    support_text = ""
    for model, answer in support_answers.items():
        # Skip error answers
        if "Error" in answer:
            continue
        support_text += f"\n[{model}]:\n{answer}\n"
        support_text += "-" * 30 + "\n"

    # ── If no valid support answers return lead
    if not support_text:
        return lead_answer

    # ── Get combine instruction for this intent
    instruction = COMBINE_INSTRUCTIONS.get(
        intent,
        COMBINE_INSTRUCTIONS["GENERAL"]
    )

    # ── Build the combine prompt
    combine_prompt = f"""
    {instruction}

    ═══════════════════════════════════
    ORIGINAL QUESTION:
    {user_question}
    ═══════════════════════════════════

    PRIMARY ANSWER (from {lead_model} - Best model for {intent}):
    {lead_answer}

    ═══════════════════════════════════
    SUPPORT ANSWERS (for reference):
    {support_text}
    ═══════════════════════════════════

    Now create the FINAL EXPERT ANSWER.
    Use the primary answer as your base.
    Enhance it with best parts from support.
    Make it the best possible answer.

    FINAL EXPERT ANSWER:
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": combine_prompt}],
            max_tokens=1024,
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        # If combiner fails return lead answer
        print(f"Combiner Error: {str(e)}")
        return lead_answer


# ── Test the Combiner ────────────────────────────

if __name__ == "__main__":

    # Simulate what parallel_caller returns
    test_cases = [

        {
            "question": "Write a Python function to reverse a string",
            "intent":   "CODING",
            "lead_model": "Groq Llama3-70B",
            "lead_answer": """
def reverse_string(s: str) -> str:
    return s[::-1]

# Example:
print(reverse_string("hello"))  # Output: olleh
            """,
            "support_answers": {
                "Cohere Command-A": """
def reverse_string(input_string):
    return ''.join(reversed(input_string))
                """,
                "OpenRouter": """
def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result
                """
            }
        },

        {
            "question": "Write a short poem about the ocean",
            "intent":   "CREATIVE_WRITING",
            "lead_model": "Cohere Command-A",
            "lead_answer": """
Waves crash upon the shore,
A timeless dance forevermore.
The ocean calls with salty breath,
A world between life and death.
            """,
            "support_answers": {
                "Groq Llama3-70B": """
Deep blue waters, vast and wide,
Secrets hidden in the tide.
            """,
                "OpenRouter": """
The sea whispers ancient tales,
Through storms and gentle gales.
            """
            }
        },
    ]

    for test in test_cases:
        print("\n" + "=" * 60)
        print(f"📝 Question: {test['question']}")
        print(f"🎯 Intent:   {test['intent']}")
        print(f"🥇 Lead:     {test['lead_model']}")
        print("=" * 60)

        final = combine_answers(
            user_question   = test['question'],
            intent          = test['intent'],
            lead_model      = test['lead_model'],
            lead_answer     = test['lead_answer'],
            support_answers = test['support_answers']
        )

        print("\n🏆 FINAL EXPERT ANSWER:")
        print(final)
        print("=" * 60)
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router.classifier import classify_intent
from router.parallel_caller import call_models_for_intent
from router.combiner import combine_answers

def get_expert_answer(user_message: str) -> dict:
    """
    MASTER FUNCTION
    Takes user message
    Returns expert answer

    Flow:
    1. Classify intent
    2. Call right models
    3. Combine answers
    4. Return result
    """

    print("\n" + "🔄" * 20)
    print(f"📝 User Question: {user_message}")
    print("🔄" * 20)

    # ── Step 1: Classify Intent ──────────────────
    print("\n🔍 Step 1: Classifying intent...")
    intent = classify_intent(user_message)
    print(f"✅ Intent detected: {intent}")

    # ── Step 2: Call Right Models ────────────────
    print(f"\n📡 Step 2: Calling best models for {intent}...")
    model_results = call_models_for_intent(user_message, intent)

    lead_model      = model_results["lead_model"]
    lead_answer     = model_results["lead_answer"]
    support_answers = model_results["support_answers"]

    print(f"✅ Got answers from all models")

    # ── Step 3: Combine Answers ──────────────────
    print(f"\n🧠 Step 3: Combining into expert answer...")
    final_answer = combine_answers(
        user_question   = user_message,
        intent          = intent,
        lead_model      = lead_model,
        lead_answer     = lead_answer,
        support_answers = support_answers
    )
    print(f"✅ Expert answer ready!")

    # ── Step 4: Return Everything ────────────────
    return {
        "question":       user_message,
        "intent":         intent,
        "lead_model":     lead_model,
        "lead_answer":    lead_answer,
        "support_answers": support_answers,
        "final_answer":   final_answer,
    }


# ── Test main_router ─────────────────────────────

if __name__ == "__main__":

    test_questions = [
        "Write a Python function to check if a number is prime",
        "What is the capital of France?",
        "Write a short poem about stars",
    ]

    for question in test_questions:
        result = get_expert_answer(question)

        print("\n" + "★" * 60)
        print("🏆 FINAL EXPERT ANSWER:")
        print("★" * 60)
        print(result["final_answer"])
        print(f"\n📊 Intent:     {result['intent']}")
        print(f"🥇 Lead Model: {result['lead_model']}")
        print("★" * 60)
        input("\nPress Enter for next question...")
import sys
import os
import concurrent.futures

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
import cohere
import requests
from config.api_config import KEYS

# ── Initialize Clients ───────────────────────────
groq_client = Groq(api_key=KEYS['groq'])

# ── Routing Config ───────────────────────────────
ROUTING_CONFIG = {

    "CODING": {
        "lead":         "Groq Llama3-70B",
        "support":      ["Cohere Command-A", "OpenRouter"],
        "focus":        "Focus on writing clean, working, well-commented code"
    },

    "COMPLEX_LOGIC": {
        "lead":         "Groq Llama3-70B",
        "support":      ["Cohere Command-A", "OpenRouter"],
        "focus":        "Focus on step by step logical reasoning and accuracy"
    },

    "CREATIVE_WRITING": {
        "lead":         "Cohere Command-A",
        "support":      ["Groq Llama3-70B", "OpenRouter"],
        "focus":        "Focus on creativity, narrative flow and engagement"
    },

    "DATA_ANALYSIS": {
        "lead":         "Groq Llama3-70B",
        "support":      ["Cohere Command-A", "OpenRouter"],
        "focus":        "Focus on insights, patterns and data conclusions"
    },

    "QUICK_ANSWER": {
        "lead":         "Groq Llama3-8B",
        "support":      [],
        "focus":        "Give direct concise answer in 1-2 lines only"
    },

    "GENERAL": {
        "lead":         None,
        "support":      ["Groq Llama3-70B", "Groq Llama3-8B",
                        "Cohere Command-A", "OpenRouter"],
        "focus":        "Give comprehensive helpful answer"
    },
}

# ── Individual API Callers ───────────────────────

def call_groq_llama70b(message: str) -> str:
    """Groq - Llama3 70B (Best Quality)"""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message}],
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq 70B Error: {str(e)}"


def call_groq_llama8b(message: str) -> str:
    """Groq - Llama3 8B (Fastest)"""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": message}],
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq 8B Error: {str(e)}"


def call_cohere(message: str) -> str:
    """Cohere - Command A (Best for Creative)"""
    try:
        co = cohere.ClientV2(api_key=KEYS['cohere'])
        response = co.chat(
            model="command-a-03-2025",
            messages=[{"role": "user", "content": message}]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"Cohere Error: {str(e)}"


def call_openrouter(message: str) -> str:
    """OpenRouter - Support Model"""
    try:
        headers = {
            "Authorization": f"Bearer {KEYS['openrouter']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://smart-ai-expert.com",
            "X-Title": "Smart AI Expert"
        }
        data = {
            "model": "google/gemma-3-4b-it:free",
            "messages": [{"role": "user", "content": message}]
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        result = response.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        else:
            return f"OpenRouter Error: {result}"
    except Exception as e:
        return f"OpenRouter Error: {str(e)}"


# ── Model Registry ───────────────────────────────
MODEL_REGISTRY = {
    "Groq Llama3-70B":  call_groq_llama70b,
    "Groq Llama3-8B":   call_groq_llama8b,
    "Cohere Command-A": call_cohere,
    "OpenRouter":       call_openrouter,
}


# ── Smart Parallel Caller ────────────────────────

def call_models_for_intent(message: str, intent: str) -> dict:
    """
    Calls the RIGHT models based on intent
    Lead model gets special focused prompt
    Support models get normal message
    Returns:
        - lead_answer: best model answer
        - support_answers: other models answers
        - intent: detected task type
        - lead_model: which model was lead
    """

    config = ROUTING_CONFIG.get(intent, ROUTING_CONFIG["GENERAL"])

    lead_model    = config["lead"]
    support_models = config["support"]
    focus         = config["focus"]

    # ── Build focused prompt for lead model
    if lead_model:
        lead_prompt = f"""
        You are the PRIMARY AI for this task.
        Task Type: {intent}
        Special Instruction: {focus}

        User Question: {message}

        Give your BEST answer focusing on your specialty.
        """
    else:
        lead_prompt = message

    results = {
        "lead_model":      lead_model,
        "lead_answer":     None,
        "support_answers": {},
        "intent":          intent,
    }

    # ── For QUICK_ANSWER just call lead only
    if intent == "QUICK_ANSWER":
        print(f"\n⚡ Quick Answer Mode → Using {lead_model} only")
        answer = MODEL_REGISTRY[lead_model](lead_prompt)
        results["lead_answer"] = answer
        return results

    # ── For all others call lead + support in parallel
    callers_to_run = {}

    if lead_model:
        callers_to_run[lead_model] = (
            MODEL_REGISTRY[lead_model], lead_prompt
        )

    for model_name in support_models:
        if model_name in MODEL_REGISTRY:
            callers_to_run[model_name] = (
                MODEL_REGISTRY[model_name], message
            )

    print(f"\n📡 Intent: {intent}")
    print(f"🥇 Lead Model: {lead_model}")
    print(f"🤝 Support Models: {support_models}")
    print(f"⚙️  Calling all in parallel...")

    # ── Run in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:

        future_to_name = {
            executor.submit(func, msg): name
            for name, (func, msg) in callers_to_run.items()
        }

        for future in concurrent.futures.as_completed(future_to_name):
            name   = future_to_name[future]
            answer = future.result()

            if name == lead_model:
                results["lead_answer"] = answer
                print(f"✅ 🥇 {name} (LEAD) responded")
            else:
                results["support_answers"][name] = answer
                print(f"✅ 🤝 {name} (support) responded")

    return results


# ── Test ─────────────────────────────────────────

if __name__ == "__main__":

    # Test different intents
    tests = [
        ("Write a Python function to reverse a string", "CODING"),
        ("Write a short poem about the ocean",          "CREATIVE_WRITING"),
        ("What is the capital of Japan?",               "QUICK_ANSWER"),
        ("Solve: if x + 2 = 10, what is x?",           "COMPLEX_LOGIC"),
    ]

    for message, intent in tests:
        print("\n" + "=" * 60)
        print(f"📝 Message: {message}")
        print(f"🎯 Intent:  {intent}")
        print("=" * 60)

        result = call_models_for_intent(message, intent)

        print(f"\n🥇 LEAD ANSWER ({result['lead_model']}):")
        print(result['lead_answer'])

        if result['support_answers']:
            print(f"\n🤝 SUPPORT ANSWERS:")
            for model, answer in result['support_answers'].items():
                print(f"\n  [{model}]:")
                print(f"  {answer[:200]}...")

        print("\n" + "=" * 60)
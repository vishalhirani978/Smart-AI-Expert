import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config.api_config import KEYS

client = Groq(api_key=KEYS['groq'])

def classify_intent(user_massage: str) -> str:
    """
    take user massage
    Return what type of task it is 
    """
    prompt = f"""
    you are an intent classifier for AI router system.
    
    classify the following user message into EXACTLY ONE category:
    
    categorys:
    - CODING   (code, programming, debugging,fix error,build app )
    - COMPLEX_LOGIC (math,solve,calculate reasoning ,proof,logic)
    - CREATIVE_WRITING (story,poem,essay,blog,creative)
    - DATA_ANALYSIS (data,analysis,visualization,statistics,charts,CSV,Excel)
    - QUICK_ANSWER (simple question, general knowledge, trivia, definition, fact,what is , who is, when is, where is)
    - GENRAL (anything else)
    
    User Message:"{user_massage}"
    
    Rules:
    1. Reply with ONLY the category name
    2. No explanation
    3. No punctuation
    4. just ONE word from the list above 
    
    Category:
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        
        intent = response.choices[0].message.content.strip().upper()
        
        valid_intents = [
            "CODING", 
            "COMPLEX_LOGIC", 
            "CREATIVE_WRITING", 
            "DATA_ANALYSIS", 
            "QUICK_ANSWER", 
            "GENRAL"
            ]
        if intent not in valid_intents:
            return "GENRAL"
        return intent
    except Exception as e:
        print(f"Classifier Error :{str(e)}")
        return "GENRAL"
    
if __name__ == "__main__":
    
    test_message =["Write me a Python function to sort a list",
        "Solve this equation: 2x + 5 = 15",
        "Write a short story about a robot",
        "What is the capital of France?",
        "Analyze this sales data and find trends",
        "Help me build a login system",
        ]
    print("Testing Classifier...")
    print("-" * 40)
    
    for message in test_message:
        intent = classify_intent(message)
        print(f"Message: {message[:40]}...")
        print(f"Intent: {intent}")
        print("-" * 40)
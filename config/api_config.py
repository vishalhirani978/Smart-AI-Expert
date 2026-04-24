import os
from dotenv import load_dotenv

load_dotenv()

KEYS = {
    "groq":        os.getenv("GROQ_API_KEY"),
    "gemini":      os.getenv("GOOGLE_API_KEY"),
    "openrouter":  os.getenv("OPENROUTER_API_KEY"),
    "cohere":      os.getenv("COHERE_API_KEY"),
    "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
}
# 📖 Code Documentation

## Smart AI Expert — Complete Code Reference

---

## File: `app.py`
**Role:** Flask web server — entry point of the application

```python
# Key Functions:

index()
# Route: GET /
# Returns: Renders index.html template

ask()
# Route: POST /ask
# Input:  JSON { "message": "user question" }
# Output: JSON {
#   success, question, intent,
#   lead_model, lead_answer,
#   support_answers, final_answer
# }

health()
# Route: GET /health
# Returns: {"status": "ok"}
# Used by: HuggingFace to check if app is alive
```

---

## File: `config/api_config.py`
**Role:** Loads API keys from environment variables

```python
# Uses python-dotenv to load .env file
# Creates KEYS dictionary:

KEYS = {
    "groq":        os.getenv("GROQ_API_KEY"),
    "gemini":      os.getenv("GOOGLE_API_KEY"),
    "openrouter":  os.getenv("OPENROUTER_API_KEY"),
    "cohere":      os.getenv("COHERE_API_KEY"),
    "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
}

# Usage in other files:
from config.api_config import KEYS
client = Groq(api_key=KEYS["groq"])
```

---

## File: `router/classifier.py`
**Role:** Detects the type/intent of user message

```python
classify_intent(user_message: str) -> str
# Input:  Any user message string
# Output: One of these strings:
#         "CODING"
#         "COMPLEX_LOGIC"
#         "CREATIVE_WRITING"
#         "DATA_ANALYSIS"
#         "QUICK_ANSWER"
#         "GENERAL"
#
# How it works:
# 1. Sends message to Groq Llama3-70B
# 2. Uses a classification prompt
# 3. Model returns ONE category name
# 4. Validates against valid_intents list
# 5. Falls back to "GENERAL" if invalid
#
# Model used: llama-3.3-70b-versatile
# Max tokens: 10 (only needs one word back)
# Temperature: 0 (consistent results)
```

---

## File: `router/parallel_caller.py`
**Role:** Calls multiple AI APIs simultaneously

```python
# ROUTING_CONFIG (dict)
# Defines which models handle which intent:
# {
#   "CODING": {
#     "lead": "Groq Llama3-70B",
#     "support": ["Cohere", "OpenRouter"],
#     "focus": "instruction for lead model"
#   },
#   ...
# }

# Individual callers:

call_groq_llama70b(message: str) -> str
# Model: llama-3.3-70b-versatile
# Best for: Coding, Logic, Combining
# Max tokens: 2048

call_groq_llama8b(message: str) -> str
# Model: llama-3.1-8b-instant
# Best for: Quick answers (fastest)
# Max tokens: 2048

call_cohere(message: str) -> str
# Model: command-a-03-2025
# Best for: Creative writing
# Max tokens: 2048

call_openrouter(message: str) -> str
# Model: google/gemma-3-4b-it:free
# Role: Support/fallback model
# Max tokens: 2048

# Main function:

call_models_for_intent(message: str, intent: str) -> dict
# Input:  user message + detected intent
# Output: {
#   "lead_model": "Groq Llama3-70B",
#   "lead_answer": "...",
#   "support_answers": {
#     "Cohere": "...",
#     "OpenRouter": "..."
#   },
#   "intent": "CODING"
# }
#
# How it works:
# 1. Looks up ROUTING_CONFIG[intent]
# 2. Gets lead model + support models
# 3. Builds focused prompt for lead model
# 4. Calls all models using ThreadPoolExecutor
# 5. Returns all answers with metadata
#
# Special case: QUICK_ANSWER
# → Only calls Groq 8B (fastest, no combining)
```

---

## File: `router/combiner.py`
**Role:** Merges multiple AI answers into one expert answer

```python
# COMBINE_INSTRUCTIONS (dict)
# Different instructions per intent type:
# {
#   "CODING": "You are a Senior Engineer...",
#   "CREATIVE_WRITING": "You are a Master Writer...",
#   "COMPLEX_LOGIC": "You are an Expert Logician...",
#   ...
# }

combine_answers(
    user_question: str,
    intent: str,
    lead_model: str,
    lead_answer: str,
    support_answers: dict
) -> str
#
# Input:  All model answers + metadata
# Output: Single combined expert answer
#
# How it works:
# 1. Gets role instruction for this intent
# 2. Builds prompt with all answers
# 3. Sends to Groq Llama3-70B
# 4. Gets one combined expert answer
# 5. Falls back to lead_answer if error
#
# Special cases:
# - QUICK_ANSWER → returns lead directly
# - No support answers → returns lead directly
# - Error answers filtered out automatically
```

---

## File: `router/main_router.py`
**Role:** Master controller — connects all pieces

```python
get_expert_answer(user_message: str) -> dict
#
# Input:  Raw user message string
# Output: {
#   "question":        original message,
#   "intent":          detected intent,
#   "lead_model":      best model name,
#   "lead_answer":     lead model answer,
#   "support_answers": other model answers,
#   "final_answer":    combined expert answer
# }
#
# Flow:
# Step 1: classify_intent(user_message)
# Step 2: call_models_for_intent(message, intent)
# Step 3: combine_answers(all results)
# Step 4: Return complete result dict
```

---

## File: `templates/index.html`
**Role:** Main UI HTML structure

```
Key sections:
├── <head>
│   ├── Google Fonts (Inter + JetBrains Mono)
│   └── CSS link
│
├── <body>
│   └── .app (flex container)
│       ├── <aside class="sidebar">
│       │   ├── .sidebar-header (logo + theme toggle)
│       │   ├── .sidebar-section (new chat button)
│       │   ├── .sidebar-section (routing map)
│       │   ├── .sidebar-section (active models)
│       │   └── .sidebar-footer
│       │
│       └── <main class="main">
│           ├── .topbar
│           ├── .chat-area
│           │   ├── #welcomeScreen
│           │   └── #messages
│           └── .input-area
│               ├── textarea#userInput
│               └── button#sendBtn
```

---

## File: `static/css/style.css`
**Role:** All visual styling

```css
/* Key sections: */

:root { }           /* Light theme variables */
[data-theme="dark"] /* Dark theme variables */

/* Variables include:
   --bg-primary, --bg-secondary
   --text-primary, --text-secondary
   --border, --accent
   --user-bubble, --ai-bubble
   --lead-color, --support-color
   --font-main, --font-mono
*/

/* Components:
   .app          → Main flex layout
   .sidebar      → Left panel
   .main         → Right content
   .messages     → Chat container
   .user-bubble  → User message style
   .ai-bubble    → AI response style
   .meta-badge   → Intent/Model tags
   .action-btn   → Copy/Show buttons
   .raw-answers  → Individual model answers
   .input-wrapper→ Input area
   .send-btn     → Send button
*/
```

---

## File: `static/js/main.js`
**Role:** All frontend interactivity

```javascript
// State:
state = {
    isLoading: false,
    theme: localStorage.getItem('theme') || 'light'
}

// Key Functions:

sendMessage()
// Triggered by: Enter key or send button
// 1. Gets input text
// 2. Hides welcome screen
// 3. Shows user message
// 4. Shows loading animation
// 5. Calls POST /ask
// 6. Renders AI response
// 7. Saves to session history

appendUserMessage(text)
// Adds user bubble to chat

appendLoading()
// Shows 3-step processing animation:
// Step 1: Detecting task type
// Step 2: Calling AI models
// Step 3: Combining answer

appendAIMessage(data)
// Renders complete AI response with:
// - Formatted answer (markdown)
// - Intent badge
// - Lead model badge
// - Copy button
// - Show/Hide model answers button
// - Individual model answers accordion

copyAnswer(btn, text)
// Copies answer to clipboard
// Shows "Copied!" feedback

toggleRaw(btn)
// Shows/Hides individual model answers

formatMarkdown(text)
// Converts markdown to HTML:
// - Code blocks (```)
// - Inline code (`)
// - Bold (**text**)
// - Italic (*text*)
// - Headers (#, ##, ###)
// - Lists (-)

updateThemeIcon()
// Updates ☀/☽ icon based on theme
```

---

## File: `Dockerfile`
**Role:** Docker container configuration

```dockerfile
FROM python:3.11-slim    # Base image

WORKDIR /app             # Working directory

# Install all packages directly
RUN pip install flask groq cohere ...

COPY . .                 # Copy project files

EXPOSE 7860              # HuggingFace port

ENV PORT=7860            # Environment variable

CMD ["python", "-m", "gunicorn", ...]  # Start command
```

---

## Environment Variables Reference

| Variable | Required | Used In |
|----------|----------|---------|
| `GROQ_API_KEY` | ✅ Yes | classifier.py, parallel_caller.py, combiner.py |
| `GOOGLE_API_KEY` | ⚠️ Optional | parallel_caller.py |
| `OPENROUTER_API_KEY` | ✅ Yes | parallel_caller.py |
| `COHERE_API_KEY` | ✅ Yes | parallel_caller.py |
| `HUGGINGFACE_API_KEY` | ⚠️ Optional | Future use |
| `PORT` | ✅ Yes | app.py (set by HuggingFace) |

---

## Error Handling

```
Each API caller has try/except:
└── Returns "ModelName Error: message"
    instead of crashing

Combiner handles errors:
└── Filters out error answers
└── Falls back to lead_answer

Classifier handles errors:
└── Returns "GENERAL" as safe fallback

Flask /ask endpoint:
└── Returns JSON error with 500 status
└── Never crashes the server
```
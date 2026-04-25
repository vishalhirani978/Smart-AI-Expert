# 🏗️ System Architecture

## Smart AI Expert — Architecture Document

---

## 1. System Overview

Smart AI Expert is a **multi-model AI orchestration system**
that intelligently routes user queries to the most suitable
AI models and combines their responses into a single,
high-quality answer.

```
┌─────────────────────────────────────────────────────┐
│                    USER INTERFACE                    │
│              (HTML + CSS + JavaScript)               │
└─────────────────────────┬───────────────────────────┘
                          │ HTTP POST /ask
                          ▼
┌─────────────────────────────────────────────────────┐
│                   FLASK WEB SERVER                   │
│                      (app.py)                        │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                   MAIN ROUTER                        │
│                 (main_router.py)                     │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  CLASSIFIER │→ │   PARALLEL   │→ │  COMBINER  │ │
│  │             │  │    CALLER    │  │            │ │
│  │ Detects     │  │ Calls models │  │ Merges     │ │
│  │ intent type │  │ in parallel  │  │ answers    │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└─────────────────────────┬───────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────────┐
    │   GROQ   │   │  COHERE  │   │  OPENROUTER  │
    │  API     │   │  API     │   │  API         │
    │          │   │          │   │              │
    │ Llama3   │   │Command-A │   │ Free models  │
    │ 70B + 8B │   │          │   │              │
    └──────────┘   └──────────┘   └──────────────┘
```

---

## 2. Component Architecture

### 2.1 Frontend Layer

```
templates/index.html
├── App Shell (sidebar + main)
├── Sidebar
│   ├── Logo + Theme Toggle
│   ├── New Chat Button
│   ├── Routing Map Display
│   └── Active Models List
├── Main Content
│   ├── Top Bar
│   ├── Chat Area
│   │   ├── Welcome Screen
│   │   └── Messages Container
│   └── Input Area
│
static/css/style.css
├── CSS Variables (light/dark themes)
├── Layout (flexbox)
├── Component styles
└── Animations
│
static/js/main.js
├── State Management
├── Theme Toggle
├── Message Sending
├── API Communication
├── Markdown Rendering
└── Copy/Toggle Functions
```

### 2.2 Backend Layer

```
app.py (Flask Server)
├── GET  /        → Serve index.html
├── POST /ask     → Process question
└── GET  /health  → Health check

router/
├── classifier.py
│   └── classify_intent(message) → str
│
├── parallel_caller.py
│   ├── ROUTING_CONFIG (dict)
│   ├── call_groq_llama70b()
│   ├── call_groq_llama8b()
│   ├── call_cohere()
│   ├── call_openrouter()
│   └── call_models_for_intent() → dict
│
├── combiner.py
│   ├── COMBINE_INSTRUCTIONS (dict)
│   └── combine_answers() → str
│
└── main_router.py
    └── get_expert_answer() → dict
```

---

## 3. Data Flow

### 3.1 Request Flow

```
1. User types message in browser

2. JavaScript sends POST to /ask:
   {
     "message": "Write a Python sort function"
   }

3. Flask receives request
   → calls get_expert_answer(message)

4. get_expert_answer():
   Step 1: classify_intent(message)
           → returns "CODING"

   Step 2: call_models_for_intent(message, "CODING")
           → Looks up ROUTING_CONFIG["CODING"]
           → lead_model = "Groq Llama3-70B"
           → support = ["Cohere", "OpenRouter"]
           → Calls all in parallel threads
           → Returns {lead_answer, support_answers}

   Step 3: combine_answers(...)
           → Sends all answers to Groq 70B
           → Gets combined expert answer
           → Returns final_answer

5. Flask returns JSON:
   {
     "success": true,
     "intent": "CODING",
     "lead_model": "Groq Llama3-70B",
     "lead_answer": "...",
     "support_answers": {...},
     "final_answer": "..."
   }

6. JavaScript renders answer in chat
```

### 3.2 Intent Classification Flow

```
User Message
     │
     ▼
Groq Llama3-70B (classifier prompt)
     │
     ▼
Returns ONE of:
├── CODING
├── COMPLEX_LOGIC
├── CREATIVE_WRITING
├── DATA_ANALYSIS
├── QUICK_ANSWER
└── GENERAL
```

### 3.3 Parallel Calling Flow

```
For CODING intent:

                    ┌──────────────────────┐
                    │   Thread Pool        │
                    │                      │
Message ──────────► │ Thread 1: Groq 70B  │──► Answer 1 (LEAD)
Focused Prompt ───► │                      │
                    │ Thread 2: Cohere    │──► Answer 2
Normal Prompt ────► │                      │
                    │ Thread 3: OpenRouter│──► Answer 3
Normal Prompt ────► │                      │
                    └──────────────────────┘
                              │
                    All answers collected
                    when last thread done
```

---

## 4. Routing Configuration

```python
ROUTING_CONFIG = {
    "CODING": {
        "lead": "Groq Llama3-70B",
        "support": ["Cohere Command-A", "OpenRouter"],
        "focus": "Write clean, working, well-commented code"
    },
    "COMPLEX_LOGIC": {
        "lead": "Groq Llama3-70B",
        "support": ["Cohere Command-A", "OpenRouter"],
        "focus": "Step by step logical reasoning"
    },
    "CREATIVE_WRITING": {
        "lead": "Cohere Command-A",
        "support": ["Groq Llama3-70B", "OpenRouter"],
        "focus": "Creativity, narrative flow, engagement"
    },
    "DATA_ANALYSIS": {
        "lead": "Groq Llama3-70B",
        "support": ["Cohere Command-A", "OpenRouter"],
        "focus": "Insights, patterns, conclusions"
    },
    "QUICK_ANSWER": {
        "lead": "Groq Llama3-8B",
        "support": [],
        "focus": "Direct concise answer only"
    },
    "GENERAL": {
        "lead": None,
        "support": ["All models"],
        "focus": "Comprehensive answer"
    }
}
```

---

## 5. Deployment Architecture

```
Developer Machine
      │
      │ git push
      ▼
┌─────────────────────────────────────┐
│           GitHub Repository          │
│   vishalhirani978/Smart-AI-Expert   │
└──────────────────┬──────────────────┘
                   │
                   │ git push huggingface main
                   ▼
┌─────────────────────────────────────┐
│       HuggingFace Spaces            │
│    vishal-builds/smart-ai-expert    │
│                                     │
│  ┌─────────────────────────────┐   │
│  │      Docker Container       │   │
│  │                             │   │
│  │  python:3.11-slim           │   │
│  │  + all pip packages         │   │
│  │  + project files            │   │
│  │                             │   │
│  │  gunicorn app:app           │   │
│  │  port: 7860                 │   │
│  └─────────────────────────────┘   │
│                                     │
│  Secrets (API Keys):                │
│  GROQ_API_KEY                       │
│  GOOGLE_API_KEY                     │
│  OPENROUTER_API_KEY                 │
│  COHERE_API_KEY                     │
│  HUGGINGFACE_API_KEY               │
└─────────────────────────────────────┘
                   │
                   │ Public URL
                   ▼
    https://vishal-builds-smart-ai-expert.hf.space
```

---

## 6. Technology Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Web Framework | Flask | Lightweight, simple |
| WSGI Server | Gunicorn | Production standard |
| Container | Docker | Reproducible deployment |
| Parallel Calls | ThreadPoolExecutor | I/O bound tasks |
| Frontend | Vanilla JS | No dependencies |
| Styling | Custom CSS | Full control |
| Fonts | Inter + JetBrains Mono | Professional look |

---

## 7. Performance Considerations

```
Without Parallel Calling:
API 1: ████████ 2s
API 2:         ████████ 2s
API 3:                 ████████ 2s
Total: 6 seconds

With Parallel Calling:
API 1: ████████ 2s
API 2: ████████ 2s  (simultaneous)
API 3: ████████ 2s  (simultaneous)
Total: ~2 seconds (3x faster!)
```

---

## 8. Security Considerations

```
✅ API keys in .env (never committed)
✅ .env in .gitignore
✅ API keys in HF Secrets (encrypted)
✅ No user data stored
✅ No database
✅ Error messages sanitized
✅ Input validation on /ask endpoint
```
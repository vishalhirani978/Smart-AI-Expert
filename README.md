---
title: Smart AI Expert
emoji: 🧠
colorFrom: gray
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

<div align="center">

# 🧠 Smart AI Expert

### A free multi-model AI router that gives expert-level answers

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge)](https://vishal-builds-smart-ai-expert.hf.space)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/vishalhirani978/Smart-AI-Expert)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python)](https://python.org)

</div>

---

## 🎯 What is Smart AI Expert?

Smart AI Expert is a **free**, **open-source** AI chatbot that:

- Automatically detects what **type** of question you are asking
- Routes your question to the **best AI model** for that task
- Calls **multiple AI models simultaneously** in parallel
- **Combines** all answers into **one expert-level response**
- All of this for **absolutely free** — no paid APIs

> **The Problem it Solves:**
> Most AI tools use a single model for everything.
> Smart AI Expert uses the RIGHT model for the RIGHT task,
> then combines multiple perspectives into one perfect answer.

---

## 🌐 Live Demo

**Try it here:**
👉 [https://vishal-builds-smart-ai-expert.hf.space](https://vishal-builds-smart-ai-expert.hf.space)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Routing** | Detects task type and routes to best model |
| 🤝 **Multi-Model** | Calls multiple AIs simultaneously |
| 🧠 **Answer Combining** | Merges best parts of all answers |
| ⚡ **Fast Mode** | Quick questions use fastest model only |
| 🌓 **Theme Toggle** | Light and Dark mode |
| 📋 **Copy Button** | Copy any answer instantly |
| 🔍 **Transparency** | See which model answered what |
| 💰 **Free** | Zero cost — all free APIs |

---

## 🗺️ How It Works

```
User Question
      │
      ▼
┌─────────────────┐
│  Intent         │  Detects: CODING / LOGIC /
│  Classifier     │  CREATIVE / DATA / QUICK / GENERAL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Smart Router   │  Selects best lead model
│                 │  + support models
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parallel       │  Calls ALL models
│  Caller         │  at the same time
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Answer         │  Combines best parts
│  Combiner       │  into one expert answer
└────────┬────────┘
         │
         ▼
   Expert Answer
```

---

## 🤖 Model Routing Strategy

| Task Type | Lead Model | Support Models |
|-----------|-----------|----------------|
| **Coding** | Groq Llama3-70B | Cohere, OpenRouter |
| **Complex Logic** | Groq Llama3-70B | Cohere, OpenRouter |
| **Creative Writing** | Cohere Command-A | Groq 70B, OpenRouter |
| **Data Analysis** | Groq Llama3-70B | Cohere, OpenRouter |
| **Quick Answer** | Groq Llama3-8B | None (speed priority) |
| **General** | All Equal | All models |

---

## 🆓 Free APIs Used

| API | Model | Purpose |
|-----|-------|---------|
| [Groq](https://groq.com) | Llama3-70B | Coding, Logic, Combining |
| [Groq](https://groq.com) | Llama3-8B | Quick answers |
| [Cohere](https://cohere.com) | Command-A | Creative writing |
| [OpenRouter](https://openrouter.ai) | Free models | Support answers |

---

## 🏗️ Project Structure

```
smart-ai-expert/
│
├── app.py                    # Flask web server
├── Dockerfile                # Docker container config
├── requirements.txt          # Python dependencies
├── Procfile                  # Process configuration
├── runtime.txt               # Python version
├── README.md                 # This file
│
├── config/
│   └── api_config.py         # API key loader
│
├── router/
│   ├── __init__.py
│   ├── classifier.py         # Intent detection
│   ├── parallel_caller.py    # Multi-model caller
│   ├── combiner.py           # Answer merger
│   └── main_router.py        # Master controller
│
├── static/
│   ├── css/
│   │   └── style.css         # All styles
│   └── js/
│       └── main.js           # Frontend logic
│
├── templates/
│   └── index.html            # Main UI
│
└── docs/
    ├── ARCHITECTURE.md       # System design
    ├── CODE_DOCUMENTATION.md # Code reference
    └── PROJECT_REPORT.md     # Full report
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Free API keys (see below)

### 1. Clone the repository
```bash
git clone https://github.com/vishalhirani978/Smart-AI-Expert.git
cd Smart-AI-Expert
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get free API keys
| Service | URL | Cost |
|---------|-----|------|
| Groq | https://console.groq.com | Free |
| Cohere | https://dashboard.cohere.com | Free |
| OpenRouter | https://openrouter.ai | Free |

### 4. Create .env file
```bash
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_gemini_key
OPENROUTER_API_KEY=your_openrouter_key
COHERE_API_KEY=your_cohere_key
HUGGINGFACE_API_KEY=your_huggingface_key
```

### 5. Run locally
```bash
python app.py
```

### 6. Open browser
```
http://localhost:5000
```

---

## 🖥️ UI Screenshots

```
Light Mode                    Dark Mode
┌──────────────────────┐     ┌──────────────────────┐
│ ◆ Smart AI   ☽       │     │ ◆ Smart AI   ☀       │
├────────┬─────────────┤     ├────────┬─────────────┤
│Routing │             │     │Routing │             │
│  Map   │  Chat Area  │     │  Map   │  Chat Area  │
│        │             │     │        │             │
│{ } Code│  [Messages] │     │{ } Code│  [Messages] │
│∑ Logic │             │     │∑ Logic │             │
│✦ Create│             │     │✦ Create│             │
├────────┴─────────────┤     ├────────┴─────────────┤
│   Ask anything...  ↑ │     │   Ask anything...  ↑ │
└──────────────────────┘     └──────────────────────┘
```

---

## 🔒 Security

- API keys stored in `.env` locally
- API keys stored in **Secrets** on HuggingFace
- `.env` is in `.gitignore` (never pushed to GitHub)
- No user data stored or logged

---

## 🛣️ Roadmap

- [x] Intent classification
- [x] Multi-model parallel calling
- [x] Answer combining
- [x] Light/Dark theme
- [x] Deployment on HuggingFace


---

## 👨‍💻 Author

**Vishal Hirani**
- GitHub: [@vishalhirani978](https://github.com/vishalhirani978)
- HuggingFace: [@vishal-builds](https://huggingface.co/vishal-builds)

---

## 📄 License

This project is open source and available under the
[MIT License](LICENSE).

---

<div align="center">
Built with  using free APIs • Zero cost • Open source
</div>
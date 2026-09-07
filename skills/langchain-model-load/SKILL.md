---
name: langchain-model-load
description: Use this skill whenever the user asks to load or initialize LLM models in LangChain (Google Gemini, OpenAI, Groq, Ollama, Anthropic), build a beginner-friendly chatbot, write teaching notes or classroom scripts in Hinglish, implement conversation memory using plain message lists (HumanMessage, AIMessage, SystemMessage), stream responses, or create minimal live-demo scripts without unnecessary abstractions (no PromptTemplate, LCEL chains, or memory classes unless explicitly requested). Trigger for phrases like "langchain model load", "gemini load karo", "model load karne ka code", "langchain chatbot", "langchain notes in hinglish", "board slides points", or any request for clean, copy-pasteable LangChain LLM code.
---

# LangChain Model Load & Teaching Notes (Hinglish)

This skill provides the canonical, beginner-friendly pipeline for loading LLM models in LangChain (Google Gemini, Groq, OpenAI, Ollama) and writing classroom-ready notes and demo scripts.

The core philosophy is **"seedha aur simple" (direct and minimal)**:
- **Shortest possible working code** that a student or developer can copy, paste, and run in 60 seconds.
- **No unnecessary abstractions**: use direct `llm.invoke()` or `llm.stream()`, plain Python lists for `chat_history`, and standard `load_dotenv()`.
- **Do not introduce** `PromptTemplate`, LCEL pipe chains (`|`), `RunnableWithMessageHistory`, or `ConversationBufferMemory` unless the user explicitly asks for them.
- **Hinglish explanations** (Roman Hindi + English tech terms) with exactly **3 board/slide points** at the end of teaching notes.

---

## 📂 Quick Reference & Navigation

| Task / Topic | Recommended File |
|---|---|
| Core Canonical Code Patterns (Single-turn, Multi-turn loop, SystemMessage, Streaming) | [`references/patterns.md`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/references/patterns.md) |
| Multi-Provider Setup (Gemini, Groq, OpenAI, Ollama, `init_chat_model`) | [`references/model_providers.md`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/references/model_providers.md) |
| Classroom Notes Format & Board Points Template | [`references/teaching_notes_template.md`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/references/teaching_notes_template.md) |
| **Runnable Script**: Minimal Single-Turn Gemini | [`scripts/gemini_quickstart.py`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/scripts/gemini_quickstart.py) |
| **Runnable Script**: Multi-turn Terminal Chatbot with List Memory | [`scripts/gemini_chat_memory.py`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/scripts/gemini_chat_memory.py) |
| **Runnable Script**: Live Streaming Typing Effect + System Persona | [`scripts/gemini_streaming_chat.py`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/scripts/gemini_streaming_chat.py) |
| **Runnable Script**: Multi-Provider Loader (Gemini / Groq / OpenAI / Ollama) | [`scripts/multi_provider_loader.py`](file:///C:/Users/user/Desktop/My%20coding%20Skills/skills/langchain-model-load/scripts/multi_provider_loader.py) |

---

## 📝 Classroom Note Output Structure

When the user asks for classroom notes, explanations, or "notes bana do", strictly follow this format:

```text
<Topic title in Hinglish, one line describing what the note covers>

1. Library Install
Bash
<pip install command>

2. <Simplest version of the concept>
<1–2 line Hinglish explanation of what the code does>
Python
<code>

3. <Next step up — e.g. loop, multi-turn, streaming, system prompt>
<1–2 line Hinglish explanation, e.g., "Students ko live demo dikhane ke liye ...">
Python
<code>

Board/Slides par Samjhane ke 3 Points
1. `ConceptOrClassName`: Ek line ka Hinglish explanation ki ye kya karta hai.
2. `ConceptOrClassName`: Ek line ka Hinglish explanation.
3. `ConceptOrClassName`: Ek line ka Hinglish explanation.
```

### Note Writing Rules:
1. **Section 1 is always Library Install**.
2. **Section 2 is always the single-turn / simplest code**.
3. **Section 3 builds one step up** (e.g., interactive while loop, streaming).
4. Always end with **exactly 3 board points**, each starting with a backticked identifier (class, function, or concept name).
5. Code labels should be literally `Bash` and `Python` on their own line before fenced blocks.

---

## 💻 Canonical Code Standards

### 1. Model Loading (Default: Google Gemini)
```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Model initialize
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    # google_api_key=os.getenv("GOOGLE_API_KEY")  # .env se auto-detect hota hai
)
```

### 2. Invocation
- Single-turn: `response = llm.invoke("Sawal yahan likho")`
- Output extraction: `response.content`

### 3. Chat Memory as a Simple List
Always use a plain Python list with `HumanMessage` and `AIMessage`. Never use `ConversationBufferMemory`:
```python
from langchain_core.messages import HumanMessage, AIMessage

chat_history = []

# User input aaya
chat_history.append(HumanMessage(content=user_input))

# Model ko poori list bhej do
response = llm.invoke(chat_history)

# Model ka reply list me jodo taaki agle turn me yaad rahe
chat_history.append(AIMessage(content=response.content))
```

### 4. System Prompt
Insert `SystemMessage` at index 0 of `chat_history`:
```python
from langchain_core.messages import SystemMessage

chat_history = [
    SystemMessage(content="Tum ek expert coding tutor ho. Hamesha saral Hindi me samjhao.")
]
```

### 5. Live Streaming (Typing Effect)
```python
print("\nBot: ", end="")
full_reply = ""
for chunk in llm.stream(chat_history):
    print(chunk.content, end="", flush=True)
    full_reply += chunk.content
print("\n")

chat_history.append(AIMessage(content=full_reply))
```

---

## 🗣️ Hinglish Style & Tone Guide

- **Style**: Teacher addressing students — encouraging, clear, zero unnecessary jargon.
- **Nouns**: Keep technical words in English (`model`, `history`, `list`, `API key`, `loop`, `chunk`).
- **Verbs / Context**: Conversational Roman Hindi:
  - "Poori history seedhe model ko bhej do"
  - "Chatbot chalu ho gaya! ('exit' likh kar band karein)"
  - "Chat band ho gayi."
  - "Key ko code me hardcode nahi karna hai, `.env` se uthana hai."
- **Numbered Comments in Code**:
  ```python
  # 1. User ka message history me jodo
  # 2. Poori history seedhe model ko bhej do
  # 3. Model ka reply screen par dikhao
  # 4. Model ka reply bhi history me jodo
  ```

---

## 🔄 Handling Different User Requests

- **"Model load karne ka code do"**: Provide the clean 10-line script using `load_dotenv()` and `ChatGoogleGenerativeAI`.
- **"Doosra model load karna hai (Groq / OpenAI / Ollama)"**: Refer to `references/model_providers.md` or use `scripts/multi_provider_loader.py`.
- **"Next topic padhana hai"**: Follow the 3-section + 3 board points template.
- **"Isko simplify karo" (user sends complex chain/runnable code)**: Strip away `ChatPromptTemplate` and `RunnablePassthrough`, replace with plain list memory and `llm.invoke()`. Add 1 board point explaining what the complex abstraction was doing.

# Multi-Provider Model Loading Guide in LangChain

Ye guide batati hai ki LangChain me alag-alag companies ke models (Gemini, Groq, OpenAI, Ollama) kaise load kiye jaate hain.

---

## 1. Quick Summary Table

| Provider | Python Package | Class Name | Default Env Var | Example Model Name |
|---|---|---|---|---|
| **Google Gemini** | `langchain-google-genai` | `ChatGoogleGenerativeAI` | `GOOGLE_API_KEY` | `gemini-1.5-flash`, `gemini-2.0-flash` |
| **Groq (Free & Fast)** | `langchain-groq` | `ChatGroq` | `GROQ_API_KEY` | `llama-3.3-70b-versatile` |
| **OpenAI** | `langchain-openai` | `ChatOpenAI` | `OPENAI_API_KEY` | `gpt-4o-mini`, `gpt-4o` |
| **Ollama (Local / Free)** | `langchain-ollama` | `ChatOllama` | *(None needed)* | `llama3.2`, `mistral`, `deepseek-r1:8b` |
| **Anthropic Claude** | `langchain-anthropic` | `ChatAnthropic` | `ANTHROPIC_API_KEY` | `claude-3-5-sonnet-20241022` |

---

## 2. Google Gemini (User's Default Standard)

### Install:
```bash
pip install langchain-google-genai python-dotenv
```

### Code:
```python
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3
)
response = llm.invoke("Python kya hai?")
print(response.content)
```

---

## 3. Groq (High Speed, Free Tier for Students)

Classroom me speed dikhane ke liye Groq sabse best hai kyunki ye LPU chips use karta hai.

### Install:
```bash
pip install langchain-groq python-dotenv
```

### Code:
```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)
response = llm.invoke("AI kya hai 2 line me samjhao.")
print(response.content)
```

---

## 4. OpenAI (GPT-4o / GPT-4o-mini)

### Install:
```bash
pip install langchain-openai python-dotenv
```

### Code:
```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)
response = llm.invoke("Explain machine learning in simple words.")
print(response.content)
```

---

## 5. Ollama (100% Offline / Free / Local Model)

Agar internet nahi hai ya API key nahi banani, toh local PC par Ollama run kar sakte hain:

### Install:
```bash
pip install langchain-ollama
```

### Code:
```python
from langchain_ollama import ChatOllama

# Ollama local port 11434 par chalta hai, koi API key nahi chahiye
llm = ChatOllama(
    model="llama3.2",
    temperature=0.3
)
response = llm.invoke("Namaste! Tum kaun ho?")
print(response.content)
```

---

## 6. Unified Model Loader: `init_chat_model`

LangChain 0.2+ me ek universal loader function aata hai jisse ek hi line me kisi bhi provider ka model switch kiya ja sakta hai:

### Install:
```bash
pip install langchain langchain-google-genai langchain-groq langchain-openai python-dotenv
```

### Code:
```python
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Google Gemini load karo:
llm_gemini = init_chat_model("gemini-1.5-flash", model_provider="google_genai")

# Ya Groq load karo:
llm_groq = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# Same invoke syntax dono par kaam karega:
res = llm_gemini.invoke("Hello Gemini!")
print(res.content)
```

---

## 7. Board Points Summary for Classroom:
1. `Provider Packages`: Har company (Google, Groq, OpenAI) ka apna ek alag LangChain package hota hai jaise `langchain-google-genai`.
2. `Model String`: `model="model_name"` parameter se decide hota hai ki us provider ka kaunsa exact version chalega.
3. `init_chat_model`: LangChain ka universal function jo bina alag-alag class import kiye kisi bhi provider ko load kar sakta hai.

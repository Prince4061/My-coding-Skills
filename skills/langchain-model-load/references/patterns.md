# Canonical Code Patterns (LangChain + Gemini)

Reuse these patterns verbatim (or with minimal changes) so every script and lesson maintains the same direct, clean style.

---

## 1. Base: Single-Turn Invocation (Simplest)

Use this when you just need to send one prompt and get one answer:

```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. .env file se API key load karo
load_dotenv()

# 2. Model initialize karo
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    # google_api_key=os.getenv("GOOGLE_API_KEY") # Note: .env me GOOGLE_API_KEY ho toh ye automatically load ho jata hai
)

# 3. Direct sawal bhejo
response = llm.invoke("Newton ka third law kya hai?")

# 4. Response ka content print karo
print(response.content)
```

### Board Points:
1. `ChatGoogleGenerativeAI`: Ye LangChain ka connector hai jo Google Gemini ke server se connect karta hai.
2. `llm.invoke(...)`: Ye function sawal bhejta hai aur Gemini se response laata hai.
3. `response.content`: Model ke response object me se sirf reply text nikalne ke liye use hota hai.

---

## 2. Base: Multi-Turn Chatbot with List Memory

Use this for an interactive terminal chatbot. Notice we use a plain Python list `chat_history` — no complicated memory classes!

```python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# Model initialize karo
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Simple list jo saari purani baatein yaad rakhegi
chat_history = []

print("Chatbot chalu ho gaya! ('exit' ya 'quit' likh kar band karein)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chat band ho gayi.")
        break

    # 1. User ka message history me jodo
    chat_history.append(HumanMessage(content=user_input))

    # 2. Poori history seedhe model ko bhej do
    response = llm.invoke(chat_history)

    # 3. Model ka reply screen par dikhao
    print(f"\nBot: {response.content}\n")

    # 4. Model ka reply bhi history me jodo taaki agle turn me yaad rahe
    chat_history.append(AIMessage(content=response.content))
```

### Board Points:
1. `chat_history = []`: Ek simple list jo conversation ke saare messages ko line se store karti hai.
2. `HumanMessage`: Batata hai ki ye baat user ne boli hai.
3. `AIMessage`: Batata hai ki ye baat AI model ne boli hai, taaki agle sawal me context maintain rahe.

---

## 3. Extension: System Prompt (Bot Persona / Rules)

Bot ko koi role ya personality dene ke liye list ke sabse shuru me `SystemMessage` daal do:

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Pehla message system ka: bot ko batao wo kaun hai
chat_history = [
    SystemMessage(content="Tum ek friendly coding teacher ho. Hamesha simple Hindi aur relatable examples ke sath jawab do.")
]
```

### Board Point:
- `SystemMessage`: Ye list ka sabse pehla message hota hai jo bot ka behavior aur role define karta hai; user ko ye screen par nahi dikhta.

---

## 4. Extension: Streaming (Typing Effect)

Terminal par ChatGPT jaisa live typing effect lane ke liye `invoke` ki jagah `stream` use karo:

```python
    # Reply ko tukdon (chunks) me lo aur turant screen par print karo
    print("\nBot: ", end="")
    full_reply = ""
    for chunk in llm.stream(chat_history):
        print(chunk.content, end="", flush=True)
        full_reply += chunk.content
    print("\n")

    # Poora reply history me jodo
    chat_history.append(AIMessage(content=full_reply))
```

### Board Point:
- `llm.stream(...)`: `invoke` poora jawab aane tak wait karta hai, jabki `stream` jaise-jaise tokens bante hain waise-waise deta hai.

---

## 5. Extension: Model Parameters (Temperature, etc.)

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,   # 0 = exact aur focused jawab, 1 = creative aur imaginative jawab
    max_tokens=1000,   # Maximum reply length limit karne ke liye
)
```

---

## 6. Extension: Limiting History (Token Saving)

History bahut lambi ho jaye toh model slow ya mehenga ho sakta hai. List slicing se sirf aakhri messages retain karo:

```python
    # Sirf aakhri 10 messages rakho
    chat_history = chat_history[-10:]

    # Agar SystemMessage shuru me tha toh usko retain karo:
    # chat_history = [chat_history[0]] + chat_history[-10:]
```

---

## 7. `.env` File Configuration

Project root directory me `.env` naam ki file banao:

```env
GOOGLE_API_KEY=AIzaSyYourGeminiApiKeyHere
```

> **Hinglish Note for Students:**
> "Project folder me `.env` naam ki file banao aur usme apni API key rakho. `load_dotenv()` ise khud padh leta hai, isliye API key ko Python code ke andar hardcode karne ki zaroorat nahi hoti."

# Teaching Notes & Lesson Templates (Hinglish)

Ye reference file teacher ke liye ready-made lesson structures aur classroom templates provide karti hai.

---

## 📌 Standard 3-Section Lesson Template

Har note is structure me likha hona chahiye:

```text
<Topic Ka Naam> — <1-line summary>

1. Library Install
Bash
pip install langchain-google-genai python-dotenv

2. <Topic Ka Sabse Simple Form>
<Hinglish me 1-2 line explanation ki code kya karta hai>
Python
<Code block>

3. <Next Step Up — Live Demo / Loop / Streaming>
<Hinglish me explanation, e.g. "Students ko live chalake dikhane ke liye...">
Python
<Code block>

Board/Slides par Samjhane ke 3 Points
1. `Point 1`: Hinglish me 1 line.
2. `Point 2`: Hinglish me 1 line.
3. `Point 3`: Hinglish me 1 line.
```

---

## 📚 Example Lesson 1: Model Load & First Prompt

```text
Gemini Model Load Karna aur First Question Puchhna

1. Library Install
Bash
pip install langchain-google-genai python-dotenv

2. Sabse Pehla Single-Turn Program
Ek simple script jo Gemini se sawal puchh kar console par answer print karti hai.
Python
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
response = llm.invoke("Newton ka pehla niyam kya hai?")

print(response.content)

3. Temperature Control Karke Output Badlna
Live demo me dikhao ki temperature badhane se model kitna creative hota hai.
Python
llm_creative = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9)
response = llm_creative.invoke("Ek short funny shayari likho coding par.")
print(response.content)

Board/Slides par Samjhane ke 3 Points
1. `ChatGoogleGenerativeAI`: Google Gemini ke models ko connect karne wali LangChain class.
2. `llm.invoke(...)`: Sawal ko cloud par bhej kar AI ka javab wapas laane wala main function.
3. `response.content`: AI ke pure packet me se text reply bahar nikalne ka tareeqa.
```

---

## 📚 Example Lesson 2: Memory & Multi-Turn Chatbot

```text
Chatbot me Memory Add Karna (Conversation History)

1. Library Install
Bash
pip install langchain-google-genai langchain-core python-dotenv

2. Ek Simple List se Memory Kaise Banti Hai
Bina kisi complex library ke, Python ki plain list me HumanMessage aur AIMessage jodte jao.
Python
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [
    HumanMessage(content="Mera naam Rahul hai."),
    AIMessage(content="Namaste Rahul! Mai aapki kya madad kar sakta hoon?"),
    HumanMessage(content="Mera naam kya tha?")
]

response = llm.invoke(chat_history)
print(response.content)

3. Live Terminal Chatbot Demo (Interactive Loop)
Students ko real chatbot jaisa feel karwane ke liye terminal loop.
Python
chat_history = []
print("Chatbot chalu ho gaya! ('exit' likhein band karne ke liye)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Bye!")
        break

    chat_history.append(HumanMessage(content=user_input))
    response = llm.invoke(chat_history)
    print(f"\nBot: {response.content}\n")
    chat_history.append(AIMessage(content=response.content))

Board/Slides par Samjhane ke 3 Points
1. `chat_history`: Saari purani baatein ek list me rakhne se bot ko context yaad rehta hai.
2. `HumanMessage`: User ke bole huye har sawal ko represent karta hai.
3. `AIMessage`: Bot ke purane javabo ko represent karta hai taaki loop me dono ki conversation bani rahe.
```

---

## 💡 Student Pitfalls & Quick Solutions

1. **Error: `API key not found`**
   - *Reason*: `.env` file save nahi ki ya root directory me nahi hai, ya `load_dotenv()` call karna bhool gaye.
   - *Fix*: `from dotenv import load_dotenv; load_dotenv()` sabse pehle likho.

2. **Error: `Model bhool gaya ki maine pehle kya kaha`**
   - *Reason*: `chat_history.append(AIMessage(...))` miss ho gaya tha.
   - *Fix*: AI ka reply bhi list me daalna zaroori hai.

3. **Error: `Quota Exceeded / Rate Limit`**
   - *Reason*: Free tier me limit cross ho gayi.
   - *Fix*: Model ko `gemini-1.5-flash` par rakho ya thoda delay daalo.

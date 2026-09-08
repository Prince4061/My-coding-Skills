# LangChain Prompt Templates — Hinglish Notes & Study Guide 📝

> **Format Rule**: Har concept ka structure hoga: **Kya hai?** ➔ **Real-Life Example** ➔ **Code** ➔ **Board Points / Simple Definition**.

---

## 🌟 Big Picture: F-string vs PromptTemplate?

### Kya hai?
Python me hum `f"Translate {text} to {lang}"` likh sakte hain. Toh phir LangChain ka `PromptTemplate` kyu chahiye?
F-string sirf text replace karta hai. `PromptTemplate`:
1. Input variables ko validate karta hai (galti se koi variable chhoot gaya to crash hone se pehle batata hai).
2. LangChain ke LCEL (`prompt | model | parser`) ke sath direct pipe hota hai.
3. Chat roles (`system`, `human`, `ai`) ko structure deta hai.
4. Prompt ko `.json` ya `.yaml` file me save/load karne ki suvidha deta hai.

---

## 🧠 Memory Formula: P ➔ C ➔ M ➔ F

Jab bhi prompt banana ho, dimag me ye 4 steps chalao:
- **P** (Plain Text) ➔ `PromptTemplate` (agar basic completion model ho).
- **C** (Chat Model) ➔ `ChatPromptTemplate` (system + human roles ke liye).
- **M** (Messages / History) ➔ `MessagesPlaceholder` (agar chatbot ko purani baatein yaad rakhni hon).
- **F** (Few-Shot) ➔ `FewShotChatMessagePromptTemplate` (agar model ko example dekar sikhana ho).

---

## 1. `PromptTemplate` (Plain Text Template)

### Kya hai?
Ek aisi template jisme variable slots `{variable_name}` hote hain. Ye single string banata hai.

### Real-Life Example
Jaise school ka leave application letter format — bas Date, Student Name, aur Reason ki jagah blank hoti hai, baaki sab pehle se chhap ke tayyar rehta hai.

### Code
```python
from langchain_core.prompts import PromptTemplate

# Template define karo
template = PromptTemplate.from_template(
    "Tum ek Hindi teacher ho. Is English sentence ko shuddh Hindi me translate karo: {sentence}"
)

# Invoke karke values bharo
prompt_value = template.invoke({"sentence": "Consistency is the key to success."})

print(prompt_value.to_string())
```

### Board Points:
1. `from_template()`: Text se automatic variables dhoondh kar template banata hai.
2. `{variable}`: Braces ke andar variable ka naam likha jata hai.
3. `.invoke(dict)`: Dictionary pass karke final prompt banaya jata hai.

---

## 2. `ChatPromptTemplate` (Chat Models ke liye System + User)

### Kya hai?
Modern LLMs (Gemini, GPT-4, Claude) plain text nahi, balki **Roles** samajhte hain:
- **System**: Model ka role ya personality (e.g., "Tum ek polite doctor ho").
- **Human / User**: Jo sawal aam insaan puch raha hai.
- **AI / Assistant**: Model ka jawab.

### Real-Life Example
Court room me Judge (System instructions set karta hai), Lawyer (Human sawal puchta hai), aur Witness (AI jawab deta hai). Teeno ki alag pehchan hoti hai.

### Code
```python
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tum ek funny standup comedian ho jo har sawal ka jawab joke me deta hai."),
    ("human", "Bhai, {topic} kya hota hai?"),
])

# Invoke karo
messages = chat_prompt.invoke({"topic": "Newton ka law"})
print(messages.to_messages())
```

### Board Points:
1. `from_messages()`: List of tuples `[("role", "message")]` se chat prompt banata hai.
2. Roles: `"system"`, `"human"`, `"ai"`.
3. Output: Plain string ki jagah `[SystemMessage(...), HumanMessage(...)]` banta hai.

---

## 3. `MessagesPlaceholder` (Chatbot ki Purani Yaadein / Memory)

### Kya hai?
Jab user chatbot se lagataar baat karta hai, to model ko purani baatein yaad dilani padti hain. `MessagesPlaceholder` prompt ke andar ek "khali slot" chhod deta hai jahan purani chat history ki list directly fit ho sake.

### Real-Life Example
Jaise doctor ki file — har baar jab aap doctor ke paas jaate ho, to purani prescription file (`chat_history`) table par rakh di jaati hai, fir naya sawal pucha jaata hai.

### Code
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "Aap ek helpful shopping assistant ho."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{user_query}"),
])

# Purani baatein (History)
history = [
    HumanMessage(content="Mujhe ek laptop lena hai under 50k."),
    AIMessage(content="Badhiya! Aap coding ke liye chahte hain ya gaming ke liye?"),
]

# Invoke
result = prompt.invoke({
    "chat_history": history,
    "user_query": "Coding ke liye chahiye, jisme 16GB RAM ho."
})
```

### Board Points:
1. `MessagesPlaceholder(variable_name="chat_history")`: Messages ki puri list ko prompt me ghusata hai.
2. `optional=True`: Hamesha lagao taaki pehli baari jab koi history na ho, tab program crash na ho.
3. Consistent naam: Variable ka naam hamesha `"chat_history"` rakhein.

---

## 4. Few-Shot Prompting (Examples Dekar Model ko Sikhana)

### Kya hai?
Jab model ko sirf instruction dene se samajh nahi aata ki format kya chahiye, tab hum usko 2–3 examples (solwaal + jawaab) dikha dete hain. Isko **Few-Shot Learning** kehte hain. "1 Example is worth 100 instructions!"

### Real-Life Example
Jaise bachpan me maths ki book me pehle 2 solved examples diye hote the, fir teesra sawal student ko solve karne diya jata tha.

### Code
```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 1. Kuch acche examples
examples = [
    {"review": "Khaana bahut swadisht tha, delivery bhi fast thi!", "sentiment": "POSITIVE"},
    {"1 ghante late aaya aur pizza thanda tha.", "sentiment": "NEGATIVE"},
    {"Packaging theek-thaak thi.", "sentiment": "NEUTRAL"},
]

# 2. Example ka format kaisa hoga
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{review}"),
    ("ai", "{sentiment}"),
])

# 3. Few-shot component
few_shot = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt
)

# 4. Main prompt me jodo
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Customer review padho aur sirf ek word me sentiment batao: POSITIVE, NEGATIVE, ya NEUTRAL."),
    few_shot,
    ("human", "{review}"),
])

print(final_prompt.invoke({"review": "Biryani lajawab thi yaar!"}).to_messages())
```

### Board Points:
1. `FewShotChatMessagePromptTemplate`: Chat format me examples jodne ke liye use hota hai.
2. Balanced examples: Har category (Positive, Negative, Neutral) ka kam se kam ek example hona chahiye.
3. Model hallucination zero ho jati hai aur output exact format me milta hai.

---

## 5. `prompt.partial()` (Fixed Values Pehle se Bharna)

### Kya hai?
Agar prompt me 5 variables hain, par 2 variables har jagah same hain (jaise Company Name, ya Today's Date), to unhe baar-baar invoke me pass karne ki zaroorat nahi hai. Pehle se "freeze" kar do.

### Code
```python
from langchain_core.prompts import ChatPromptTemplate

base_prompt = ChatPromptTemplate.from_messages([
    ("system", "You work for {company}. Your department is {department}."),
    ("human", "{question}"),
])

# Company aur department fix kar diya
support_prompt = base_prompt.partial(company="Zomato", department="Customer Refunds")

# Ab invoke me sirf user ka question dena hoga!
res = support_prompt.invoke({"question": "Mera refund kab aayega?"})
```

---

## 6. LCEL Chain (`prompt | model | parser`)

### Kya hai?
LangChain Expression Language ka pipe operator (`|`). Ye Linux ke pipe `|` ki tarah kaam karta hai:
`Data` ➔ `Prompt me gaya` ➔ `Model ne process kiya` ➔ `Parser ne plain text bana diya`.

### Code
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_google_genai import ChatGoogleGenerativeAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "Tum ek concise expert ho."),
    ("human", "{query}")
])

# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# chain = prompt | model | StrOutputParser()
# output = chain.invoke({"query": "Photosynthesis kya hota hai 1 line me?"})
```

---

## 7. Galti Mat Karna (Common Traps & Exam Tips)

1. **Double Curly Braces**: Agar prompt me JSON schema dikhana ho jaise `{"name": "xyz"}`, to Python confuse ho jayega. Hamesha `{{` aur `}}` likho:
   `{{"status": "ok", "user": "{username}"}}`
2. **Chat Model + PromptTemplate**: Agar Chat model (Gemini/GPT) use kar rahe ho, to plain `PromptTemplate` mat do. System prompt ka asar kam ho jata hai. Hamesha `ChatPromptTemplate` use karo.
3. **Optional History**: `MessagesPlaceholder("chat_history", optional=True)` me `optional=True` lagana mat bhoolna, varna pehle message par KeyError aayega!

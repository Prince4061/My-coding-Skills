# LangChain Prompt Templates — API & Technical Reference

Technical reference guide for LangChain prompt templates, message representations, few-shot prompting, serialization, and LCEL integration.

---

## 1. Imports & Core Classes

All modern LangChain code imports prompt components from `langchain_core.prompts` (never use the legacy `langchain.prompts` package).

```python
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotPromptTemplate,
    FewShotChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    load_prompt,
)
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage,
)
```

---

## 2. `PromptTemplate` (String / Completion Models)

Used when producing a raw text string (typically for text-completion models or non-chat pipelines).

### Instantiation

```python
# Method A: from_template (Auto-detects input_variables)
prompt = PromptTemplate.from_template(
    "Translate this text to {target_language}:\n{text}"
)

# Method B: Explicit constructor with validation
prompt = PromptTemplate(
    template="Explain {topic} in {word_count} words for a {audience}.",
    input_variables=["topic", "word_count", "audience"],
    validate_template=True,
)
```

### Formatting & Invocation

```python
# Preferred in LCEL: returns PromptValue
prompt_val = prompt.invoke({"target_language": "Hindi", "text": "Good morning"})
# prompt_val.to_string() -> 'Translate this text to Hindi:\nGood morning'
# prompt_val.to_messages() -> [HumanMessage(content='...')]

# Legacy format method: returns raw string
raw_str = prompt.format(target_language="Hindi", text="Good morning")
```

### Partial Variables (`.partial()`)

Bind some variables upfront so callers don't repeat them on every invoke.

```python
# Static partial
base_prompt = PromptTemplate.from_template("Organization: {org}\nUser: {user}\nQuery: {query}")
user_prompt = base_prompt.partial(org="Acme Corp")
output = user_prompt.invoke({"user": "Rahul", "query": "Check leave status"})

# Dynamic partial with callable (e.g. current date/time)
from datetime import datetime
prompt_with_date = PromptTemplate(
    template="Today's date is {current_date}. Answer this: {question}",
    input_variables=["question"],
    partial_variables={"current_date": lambda: datetime.now().strftime("%Y-%m-%d")}
)
```

---

## 3. `ChatPromptTemplate` (Chat Models)

Chat models (Gemini, GPT, Claude, Groq) require structured role-based messages (`system`, `human`, `ai`).

### Instantiation via `from_messages`

Tuple shorthand is the cleanest and most idiomatic:

```python
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Python engineer named {bot_name}."),
    ("human", "How do I do {task} in Python?"),
])

# Invoke returns ChatPromptValue
val = chat_prompt.invoke({"bot_name": "PyBot", "task": "reverse a list"})
messages = val.to_messages()
# [
#   SystemMessage(content="You are an expert Python engineer named PyBot."),
#   HumanMessage(content="How do I do reverse a list in Python?")
# ]
```

### Explicit Message Prompt Templates

Useful when adding custom metadata or building templates programmatically:

```python
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("System context: {system_context}"),
    HumanMessagePromptTemplate.from_template("{query}"),
])
```

---

## 4. `MessagesPlaceholder` (Chat History & Dynamic Message Lists)

Injects a variable-length list of chat messages directly into the prompt without converting them to strings.

### Syntax & Usage

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support agent for {company}."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{user_input}"),
])

# Calling with history
history = [
    HumanMessage(content="Hi, what is my account balance?"),
    AIMessage(content="Your balance is $250. How else can I help?"),
]

val = prompt.invoke({
    "company": "FastBank",
    "chat_history": history,
    "user_input": "Can I transfer $50 to Bob?"
})
```

> [!IMPORTANT]
> Always add `optional=True` to `MessagesPlaceholder` if the chain might be invoked on the very first turn before `chat_history` is created, preventing `KeyError`.

---

## 5. Few-Shot Prompt Templates

Used when the LLM needs demonstrations to reliably follow formatting or classification rules.

### A. For Chat Models: `FewShotChatMessagePromptTemplate` (Recommended)

Keeps turns clean as alternating `human` and `ai` messages.

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

# 1. Provide balanced, diverse examples
examples = [
    {"input": "The screen is sharp and battery lasts all day.", "output": "POSITIVE"},
    {"input": "Arrived broken, customer service ignored me.", "output": "NEGATIVE"},
    {"input": "The package was delivered on Tuesday.", "output": "NEUTRAL"},
]

# 2. Define example prompt format
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

# 3. Create FewShotChatMessagePromptTemplate
few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

# 4. Assemble final ChatPromptTemplate
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the sentiment of user reviews into POSITIVE, NEGATIVE, or NEUTRAL. Respond ONLY with the class name."),
    few_shot_prompt,
    ("human", "{input}"),
])

# 5. Invoke
result = final_prompt.invoke({"input": "Amazing sound quality, but a bit heavy."})
```

### B. For Text/Completion Models: `FewShotPromptTemplate`

Used when compiling into a single formatted string.

```python
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example_prompt = PromptTemplate.from_template("Input: {input}\nOutput: {output}")

few_shot = FewShotPromptTemplate(
    examples=[
        {"input": "happy", "output": "sad"},
        {"input": "tall", "output": "short"},
    ],
    example_prompt=example_prompt,
    prefix="Give the antonym of the word:",
    suffix="Input: {word}\nOutput:",
    input_variables=["word"],
    example_separator="\n\n",
)

text_val = few_shot.invoke({"word": "fast"}).to_string()
```

---

## 6. Escaping Literal Braces & JSON Prompts

LangChain uses Python `str.format` syntax by default.
- Variable: `{variable_name}`
- Literal brace: `{{` and `}}`

```python
# WRONG: causes KeyError: 'status'
bad_prompt = PromptTemplate.from_template(
    'Return output as JSON: {"status": "{status_code}", "text": "{text}"}'
)

# CORRECT: Double the braces for literal JSON
good_prompt = PromptTemplate.from_template(
    'Return output as JSON: {{"status": "{status_code}", "text": "{text}"}}'
)
```

---

## 7. Serialization (Save & Load Prompts)

Store prompts in external `.json` or `.yaml` files for version control, collaboration, and separating code from prompt engineering.

### Saving a Prompt

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise AI tutor."),
    ("human", "Explain {concept} in 2 sentences.")
])

# Save as JSON
prompt.save("tutor_prompt.json")

# Save as YAML
prompt.save("tutor_prompt.yaml")
```

### Loading a Prompt

```python
from langchain_core.prompts import load_prompt

loaded_prompt = load_prompt("tutor_prompt.json")
output = loaded_prompt.invoke({"concept": "Recursion"})
```

---

## 8. LCEL Integration (`prompt | model | parser`)

Prompt templates are the entry point of the LangChain Expression Language (LCEL).

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_google_genai import ChatGoogleGenerativeAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarize tech articles in 3 bullet points."),
    ("human", "{article_text}")
])

# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# chain = prompt | model | StrOutputParser()

# Invoke
# response = chain.invoke({"article_text": "LangChain provides composable primitives..."})
```

### Passing Additional Keys with `RunnablePassthrough`

```python
from langchain_core.runnables import RunnablePassthrough

# When downstream steps need both the model output and the original input
chain = (
    {"question": RunnablePassthrough(), "context": retriever}
    | prompt
    | model
    | StrOutputParser()
)
```

---

## 9. Debugging & Common Errors Checklist

| Error / Issue | Root Cause | Solution |
|---|---|---|
| `KeyError: 'foo'` | Variable `{foo}` in template was not provided in `.invoke()` dict | Pass `"foo"` in dict, use `prompt.partial(foo=...)`, or add `optional=True` if `MessagesPlaceholder`. |
| `KeyError` on JSON schema `{ "key": "val" }` | Python format parser thinks `{ "key"` is an input variable | Escape with double braces `{{ "key": "val" }}`. |
| Model ignores persona / system prompt | Used `PromptTemplate` (plain string) instead of `ChatPromptTemplate` | Switch to `ChatPromptTemplate.from_messages([("system", ...), ("human", ...)])`. |
| Model biased towards one output class | Few-shot examples only contained 1 class label | Ensure balanced class representation in `examples` list. |
| Chat history injected as single string | Used `{chat_history}` string instead of `MessagesPlaceholder` | Use `MessagesPlaceholder("chat_history")` and pass a list of `BaseMessage` objects. |

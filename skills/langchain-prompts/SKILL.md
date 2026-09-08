---
name: langchain-prompt-templates
description: Build LangChain prompts the right way — PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, FewShotPromptTemplate, prompt serialization (JSON/YAML) and LCEL chains (prompt | model | parser). Use this skill whenever the user wants to create, refactor, or debug a prompt for a LangChain app, asks how to pass variables/roles/chat history/examples into an LLM prompt, mentions PromptTemplate, ChatPromptTemplate, few-shot, chat_history, LCEL, or wants Hinglish explanations/notes of LangChain prompt concepts — even if they just say "LangChain me prompt banao".
---

# LangChain Prompt Templates

Is skill ka kaam: user ke use-case ke liye **sahi prompt template type chunna**, clean aur reusable code likhna, aur (agar user chahe) Hinglish me short explanation dena.

Prompt engineering = sirf question poochna nahi; model ko **correct instructions + correct context + correct format** dena. Template isko reusable, validated aur chainable banata hai.

## Step 1 — Use-case se template type decide karo

Pehle user se ye 3 cheezein clear karo (ya conversation se infer karo):

1. **Model kaisa hai?** Text/completion model → `PromptTemplate`. Chat model (GPT, Claude, Gemini, Llama-chat) → `ChatPromptTemplate`. Doubt ho to chat maano — aaj kal almost sab chat models hain.
2. **Chat history chahiye?** Haan → `MessagesPlaceholder` add karo.
3. **Output format/style model samajh nahi raha?** Haan → few-shot examples (`FewShotPromptTemplate` ya `FewShotChatMessagePromptTemplate`).

Quick decision table:

| Situation | Use |
|---|---|
| Simple text prompt with variables (translate, summarize) | `PromptTemplate` |
| Chat model, system role + user turn | `ChatPromptTemplate.from_messages` |
| Multi-turn chatbot, pichli baatein yaad rakhni hain | `ChatPromptTemplate` + `MessagesPlaceholder("chat_history")` |
| Classification / strict output format, model galti kar raha hai | Few-shot template (2–5 examples) |
| Prompt ko code se alag rakhna hai (versioning, non-dev team edit kare) | Serialization → `.json`/`.yaml` + `load_prompt` |

Memory trick: **P → C → M → F** (Plain text → Chat → Messages/history → Few-shot).

## Step 2 — Code likho (rules)

- Imports hamesha `langchain_core.prompts` se (na ki purane `langchain.prompts`).
- Variables `{curly_braces}` me; literal braces chahiye to `{{ }}`.
- Har template `.invoke(dict)` se format hota hai — `.format()` ki jagah `.invoke()` prefer karo taaki LCEL me directly chain ho.
- Prompt ko chain me lagao: `chain = prompt | model | parser`, phir `chain.invoke({...})`.
- `input_variables` explicitly dena zaroori nahi (`from_template` auto-detect karta hai), par jab validation/`validate_template=True` chahiye tab dedo.
- Partial values (date, tenant name) ke liye `prompt.partial(...)` use karo, har call me repeat mat karo.
- Chat history variable ka naam consistent rakho (`chat_history`) — `RunnableWithMessageHistory` / LangGraph ke saath seamless rehta hai.
- Few-shot me examples **diverse aur balanced** rakho (har class ka kam se kam 1), aur suffix me actual input ka slot rakho.
- Code me sirf zaroori comments; secrets/API keys kabhi hardcode mat karo (`os.environ`).

## Step 3 — Output format

Jab user prompt banwaye, ye do:

1. **Ek line me choice + reason** ("Chat model + history chahiye → ChatPromptTemplate + MessagesPlaceholder").
2. **Runnable code block** — imports, template, ek `.invoke()` example, aur LCEL chain (`prompt | model | parser`) agar model context me ho.
3. **Formatted prompt ka preview** (final text/messages kaisa dikhega) — ye user ko debug me bahut help karta hai.
4. Agar user Hinglish me baat kar raha hai to explanation Hinglish me, code/identifiers English me.

Notes/explanation maange to `references/hinglish-notes.md` ki structure follow karo: Kya hai? → Example → Simple Definition.

## Canonical snippets

**PromptTemplate**
```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Translate the following sentence into {language}: {text}"
)
prompt.invoke({"language": "Hindi", "text": "Hello, how are you?"})
```

**ChatPromptTemplate + MessagesPlaceholder**
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a customer support agent for {company}."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{user_query}"),
])
chat_prompt = chat_prompt.partial(company="Acme")
```

**Few-shot (chat style — preferred for chat models)**
```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"input": "I love this product.", "output": "Positive"},
    {"input": "This product is terrible.", "output": "Negative"},
]
example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "{output}")])
few_shot = FewShotChatMessagePromptTemplate(examples=examples, example_prompt=example_prompt)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the sentiment as Positive or Negative. Reply with one word."),
    few_shot,
    ("human", "{input}"),
])
```

**LCEL chain**
```python
from langchain_core.output_parsers import StrOutputParser

chain = final_prompt | model | StrOutputParser()
chain.invoke({"input": "This product is amazing."})
```

Text-model few-shot (`FewShotPromptTemplate` with prefix/suffix), serialization (`save`/`load_prompt`) aur full explanations ke liye `references/api-reference.md` padho.

## Common mistakes (check karo before delivering)

- Chat model ko `PromptTemplate` (plain string) dena — roles kho jaate hain.
- `MessagesPlaceholder` variable ko invoke me pass na karna → KeyError; ya `optional=True` lagao.
- Few-shot examples me sirf ek class ke examples → model biased.
- JSON output chahiye par examples/instructions me format specify nahi — parser fail hoga.
- Template me `{}` literal (JSON schema) bina escape ke — `{{ }}` use karo.

## References

- `references/api-reference.md` — har class ka syntax, params, serialization, LCEL flow (jab exact API detail chahiye).
- `references/hinglish-notes.md` — user ke original Hinglish notes; jab Hinglish me samjhana/notes banana ho to ye tone aur structure copy karo.

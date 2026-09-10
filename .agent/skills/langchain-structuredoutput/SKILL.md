---
name: langchain-structured-output
description: Extract structured, validated data from LLMs using LangChain's with_structured_output() with Pydantic, TypedDict, and JSON Schema. Always follows Devesh's exact "Why → What → How → Code" pedagogical pattern with Hinglish comments and a summary "yaad rakho" block. Use this skill whenever the user asks for structured output, JSON extraction, entity extraction, data validation, Pydantic schemas in LangChain, mentions with_structured_output, or asks to explain/code structured outputs in Devesh's teaching style ("teaching notes", "class mein explain karna", "students ko samjhana hai", "same style mein").
---

# LangChain Structured Output & Devesh's Teaching Style

Is skill ka kaam: LLM se unstructured text ki jagah **strictly typed, validated structured output** (Pydantic / TypedDict / JSON Schema) nikalna, aur har concept ko **Devesh ke "Why → What → How → Code" teaching style** mein explain karna.

---

## 🎯 Devesh's Core Pedagogical Pattern

Har code output aur explanation hamesha is fixed order mein hona chahiye:

1. **WHY — Problem Statement**: Relatable scenario jisme dikhao ki bina structured output ke kya dikkat aati hai (`# ❌ Problem: AI plain text deta hai, machine samajh nahi sakti`).
2. **WHAT — One-Line Definition**: Ek single memorable "yaad rakhne wali line" jo concept ka essence bataye (`# ✅ Structured Output = AI ka response ek fixed format/schema mein lena`).
3. **HOW — Concept Explanation with Analogy & ASCII Flow**: Blueprint analogy (`Ghar ka blueprint jaisa`) + ASCII dataflow diagram.
4. **CODE — The Actual Implementation**: Clean, runnable Python code jisme Hinglish comments *kyun* (why) explain karein, *kya* (what) nahi.
5. **YAAD RAKHO — Summary Block**: End mein `# 🔥 Yaad Rakho` bullet-point block jo revision takeaway de.

---

## 🧭 Step 1 — Schema Type Choose Karo

LLM ke response ke liye kaun sa schema structure use karna hai:

| Situation | Recommended Schema | Reason |
|---|---|---|
| **Production apps, data validation, DB insertion** | **Pydantic (`BaseModel`)** | Best choice. Type checking, range validation (`ge`, `le`), nested models aur auto-conversion. |
| **Simple scripts, lightweight dictionaries, no extra dependencies** | **`TypedDict`** | Python built-in `typing` module, lightweight structure bina validation overhead ke. |
| **External API contract, dynamic runtime schemas, non-Python consumers** | **JSON Schema (`dict`)** | Universal, language-independent standard. |

Memory Formula: **P ➔ T ➔ J** (Pydantic for validation, TypedDict for lightweight dicts, JSON Schema for universal).

---

## ⚙️ Step 2 — Code Rules & Style

- **Method**: Hamesha `llm.with_structured_output(schema)` use karo (purane `PydanticOutputParser` ya raw prompt parsing se 100x better aur reliable hai kyunki ye native Function Calling / Tool Calling use karta hai).
- **Field Descriptions**: Pydantic mein har field par `Field(description="...")` lagao — ye LLM ko hint deta hai ki kya extract karna hai.
- **Constraints**: Constraints lagao jaise `ge=0, le=100` (marks/age ke liye) ya `Literal["pass", "fail"]` (fixed categories ke liye).
- **Include Raw Metadata**: Jab token usage, raw AI message ya error inspect karna ho toh `llm.with_structured_output(schema, include_raw=True)` pass karo.
- **Variable Names**: Hamesha relatable names rakho (`student`, `product_review`, `rahul`, `resume`) — kabhi abstract variables (`x`, `data`, `obj`) mat use karo.
- **Hinglish Comments**: Comments hamesha Hinglish mein hon aur batayein *kyun* ye code likha gaya hai.

---

## 📐 Canonical ASCII Flow Diagram

Har pipeline ya data extraction code mein ye diagram comment add karo:

```text
# Flow:
#   Raw Text / User Prompt
#            ↓
#          LLM
#            ↓
#   Function/Tool Calling (with_structured_output)
#            ↓
#   Schema Validation (Pydantic / TypedDict)
#            ↓
#   Structured Object (model_dump() → Dict / JSON)
#            ↓
#   Database / API / Downstream Agent
```

---

## 🚀 Canonical Template

```python
# ═══════════════════════════════════════════════════════════════
# TOPIC: Structured Output with Pydantic
# ═══════════════════════════════════════════════════════════════

# ❌ WHY — Problem:
# Normal AI response string hota hai — isme se programmatically age aur name nikalna mushkil hai
raw_response = "Rahul is 18 years old, scored 85 marks in Maths, and lives in Delhi."
# Regex toot sakta hai agar format badal gaya!

# ─────────────────────────────────────────────────────────────
# ✅ WHAT — Concept:
# Structured Output = AI ka response ek fixed schema (Pydantic) mein lena
# ─────────────────────────────────────────────────────────────

# HOW — Data ka blueprint define karte hain (Ghar ke nakshay jaisa)
from pydantic import BaseModel, Field
from typing import Optional, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
# Ya ChatOpenAI / ChatGroq

class StudentRecord(BaseModel):
    """Student ka verified academic data model."""

    name: str = Field(description="Student ka poora naam")
    age: int = Field(ge=5, le=100, description="Student ki umar saalon mein")
    marks: int = Field(ge=0, le=100, description="Exam ke marks (0-100)")
    status: Literal["pass", "fail"] = Field(description="Exam result status")
    city: Optional[str] = Field(default=None, description="City ya location")

# 1. Model setup karo
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 2. with_structured_output se LLM ko schema bind karo
structured_llm = llm.with_structured_output(StudentRecord)

# 3. Invoke karo unstructured text ke sath
result = structured_llm.invoke("Rahul is 18 years old, scored 85 marks in Maths, and lives in Delhi.")

# Pydantic object milta hai — type safe & validated!
print(f"Name: {result.name}, Status: {result.status}, Marks: {result.marks}")

# Dictionary aur JSON export
data_dict = result.model_dump()
data_json = result.model_dump_json()

# ─────────────────────────────────────────────────────────────
# 🔥 Yaad Rakho:
# Pydantic BaseModel → Structure + Validation (Recommended)
# Field(description) → LLM ko batata hai ki field mein kya daalna hai
# with_structured_output() → Native tool-calling se 100% reliable schema output deta hai
# model_dump()       → Pydantic object se Python dict banata hai
# model_dump_json()  → Pydantic object se JSON string banata hai
# ─────────────────────────────────────────────────────────────
```

---

## 📚 References & Resources

- `references/api-reference.md` — Complete technical breakdown: Pydantic v2 vs TypedDict vs JSON Schema, `method="function_calling"` vs `json_mode`, `include_raw=True`, nested models, and exception handling.
- `references/devesh-coding-style.md` — Devesh's complete Teaching & Code Style specification guide.
- `references/hinglish-notes.md` — Student classroom teaching notes formatted in Why → What → How → Code with board points.
- `scripts/` — Runnable Python scripts demonstrating Pydantic, TypedDict, JSON Schema, nested models, and debugging modes.

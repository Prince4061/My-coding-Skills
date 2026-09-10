# LangChain Structured Output — Hinglish Teaching Notes 📝

Devesh's classroom lecture notes and board summaries for students learning LangChain Structured Output.

---

## 📌 LESSON 1: Unstructured Text Ki Problem & Solution

### ❌ 1. WHY — Problem Statement
Socho tumne AI se poocha kisi customer ke baare mein. AI ne jawab diya:
```text
"Rahul Sharma is 18 years old, lives in New Delhi, and his exam score in Mathematics was 88."
```
Ab agar computer / Python program ko bolna ho: "Bhai, database mein save kar do" — toh computer kaise samjhega?
- String split karoge? Kal ko AI bol dega: "Score: 88, Name: Rahul" — tumhara regex aur split code turant crash!
- Computer ko chahiye **key-value pairs**, na ki kahani!

### ✅ 2. WHAT — One-Line Definition
> **Structured Output = AI ka response ek fixed format/schema (Pydantic / Dict) mein lena taaki machine usko directly samajh sake.**

### 💡 3. HOW — Analogy & Data Flow
**Ghar ka blueprint socho:**
Jab architect ghar banata hai, toh pehle blueprint tayyar karta hai:
- Master Bedroom: 14x12 ft
- Kitchen: 10x8 ft
Waise hi hum LLM ko ek blueprint (Schema) de dete hain ki mujhe ye 4 cheezein isi type mein chahiye.

```text
# Flow:
#   Unstructured Text ("Rahul is 18...")
#             ↓
#           LLM
#             ↓
#    with_structured_output(Student)
#             ↓
#     Schema Validation (Pydantic)
#             ↓
#   Validated Python Object: Student(name="Rahul", age=18)
#             ↓
#   Database / Frontend API
```

### 💻 4. CODE — Implementation
```python
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Blueprint (Schema) define karo
class Student(BaseModel):
    """Student ka verified academic blueprint."""
    name: str = Field(description="Student ka poora naam")
    age: int = Field(ge=5, le=100, description="Umar saalon mein")
    marks: int = Field(ge=0, le=100, description="Maths ke marks")

# 2. Model setup
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 3. LLM ko blueprint ke sath jod do
structured_llm = llm.with_structured_output(Student)

# 4. Invoke karo
raw_text = "Rahul Sharma is 18 years old and his exam score in Mathematics was 88."
student_obj = structured_llm.invoke(raw_text)

print("Student Name:", student_obj.name)
print("Student Marks:", student_obj.marks)
```

### 🔥 5. YAAD RAKHO
```python
# 🔥 Yaad Rakho:
# 1. Unstructured text string hota hai, jo database ke liye unfit hai.
# 2. with_structured_output() LLM ko direct JSON/Pydantic object return karne par majboor karta hai.
# 3. Field(description=...) LLM ka guiding compass hota hai.
```

---

## 📌 LESSON 2: Pydantic Constraints & Types

### ❌ 1. WHY — Problem Statement
Agar LLM ko sirf `age: int` bol diya, toh ho sakta hai LLM galti se negative umar bhej de: `age = -5` ya `marks = 999`.

### ✅ 2. WHAT — One-Line Definition
> **Pydantic Validation = Data ko type ke saath-saath minimum, maximum aur allowed values par restrict karna.**

### 💡 3. HOW — Constraints & Types
- `ge`: Greater than or equal to (e.g., `ge=0`)
- `le`: Less than or equal to (e.g., `le=100`)
- `Literal["pass", "fail"]`: Sirf ye 2 values accept hongi, koi teesri nahi!
- `Optional[str]`: Compulsory nahi hai, agar mila toh theek, nahi mila toh `None`.

### 💻 4. CODE — Implementation
```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class ExamReport(BaseModel):
    """Student ka complete report card with strict validation."""

    student_name: str = Field(description="Full name")
    percentage: float = Field(ge=0.0, le=100.0, description="Percentage score")
    result: Literal["pass", "fail", "compartment"] = Field(description="Strict final outcome")
    remarks: Optional[str] = Field(default=None, description="Teacher ka remark if any")

# Agar result mein "pass" ya "fail" ke alawa kuch aaya, Pydantic turant error raise kar dega!
```

### 🔥 5. YAAD RAKHO
```python
# 🔥 Yaad Rakho:
# ge / le        → Min and Max number bounds (range validation)
# Literal[...]   → Fixed allowed categories (e.g. sentiment, pass/fail)
# Optional[...]  → Optional fields jo missing ho sakte hain
# model_dump()   → Pydantic object ko Python dictionary mein badalna
```

---

## 📌 LESSON 3: TypedDict vs Pydantic (Kaun sa Kab?)

### ❌ 1. WHY — Confusion
Beginners aksar puchte hain: "Bhai, jab Python mein `TypedDict` pehle se hai, toh alag se `Pydantic` kyu seekhein?"

### ✅ 2. WHAT — Difference
> **TypedDict = Sirf keys ka structure (no runtime check). Pydantic = Structure + Runtime Data Validation.**

### 💡 3. HOW — Comparison
- **TypedDict**: Jaise note-pad par list likh di. Kisi ne galat likh diya toh koi rokne wala nahi.
- **Pydantic**: Jaise airport ka security guard. Agar rule toota (age negative hui), toh aage badhne nahi dega!

```python
# ─────────────────────────────────────────────
# OPTION A: TypedDict (Lightweight)
# ─────────────────────────────────────────────
from typing import TypedDict, Annotated

class QuickBook(TypedDict):
    title: Annotated[str, ..., "Book title"]
    author: Annotated[str, ..., "Author name"]

# ─────────────────────────────────────────────
# OPTION B: Pydantic (Heavy-duty with rules)
# ─────────────────────────────────────────────
from pydantic import BaseModel, Field

class ValidatedBook(BaseModel):
    title: str = Field(min_length=1, description="Book title")
    price: float = Field(gt=0, description="Positive price in INR")
```

### 🔥 4. YAAD RAKHO
```python
# 🔥 Yaad Rakho:
# Simple script / quick prototyping  → TypedDict use karo
# Production API / Database / Agents → Pydantic use karo
```

---

## 📌 LESSON 4: Nested Schemas (Resume / Invoice Extraction)

### ❌ 1. WHY — Problem Statement
Duniya ka sara data flat nahi hota. Ek resume mein multiple jobs hoti hain, ek bill mein multiple items hote hain.

### ✅ 2. WHAT — One-Line Definition
> **Nested Model = Ek Pydantic class ke andar doosri Pydantic class ki list rakhna.**

### 💡 3. HOW — Blueprint within Blueprint
Jaise ek shopping cart mein multiple Items hote hain:
```text
Invoice
 ├── customer_name: str
 └── items: List[Item]
             ├── name: str
             ├── price: float
             └── qty: int
```

### 💻 4. CODE — Implementation
```python
from pydantic import BaseModel, Field
from typing import List

class WorkExperience(BaseModel):
    """Ek company ka past experience."""
    company_name: str = Field(description="Company ka naam")
    role: str = Field(description="Job role/designation")
    years: float = Field(ge=0, description="Kitne saal kaam kiya")

class CandidateProfile(BaseModel):
    """Candidate ka complete resume profile."""
    candidate_name: str = Field(description="Candidate ka naam")
    experience_history: List[WorkExperience] = Field(description="Past work experience list")
```

### 🔥 5. YAAD RAKHO
```python
# 🔥 Yaad Rakho:
# List[ChildModel] se 1-to-many relationship define hota hai.
# LLM accurately array of objects generate karta hai.
```

---

## 📌 LESSON 5: Debugging with `include_raw=True`

### ❌ 1. WHY — Problem Statement
Kabhi-kabhi extraction fail ho jaata hai ya tokens check karne hote hain. Agar direct object aayega toh raw message kaise milega?

### ✅ 2. WHAT — One-Line Definition
> **`include_raw=True` = Parsed object ke saath-saath model ka raw AIMessage aur errors bhi ek dictionary mein lena.**

### 💻 3. CODE
```python
structured_llm = llm.with_structured_output(Student, include_raw=True)
response = structured_llm.invoke("Rahul ki age 20 hai.")

# Output dictionary format:
# response["raw"]           → Original AIMessage (metadata + token count)
# response["parsed"]        → Validated Student object
# response["parsing_error"] → Agar parse fail hua toh exception, warna None
```

### 🔥 4. YAAD RAKHO
```python
# 🔥 Yaad Rakho:
# include_raw=True debugging aur logging ke liye zaroori hai.
# response["parsed"] se schema object access hota hai.
```

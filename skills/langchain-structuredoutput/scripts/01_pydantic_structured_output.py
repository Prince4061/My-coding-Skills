"""
01_pydantic_structured_output.py
---------------------------------
Topic: LangChain Structured Output with Pydantic BaseModel
Author: Devesh's Coding Style (Why -> What -> How -> Code)
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, Literal
from langchain_core.runnables import RunnableLambda

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 1. ❌ WHY — Problem Statement
# ═══════════════════════════════════════════════════════════════
# Normal LLM response unstructured plain string hota hai:
raw_ai_text = "Rahul Sharma is 19 years old, scored 88 marks in Physics, and lives in New Delhi."
# Computer / Database ko nahi pata ki 'Rahul Sharma' name hai ya 'New Delhi'!
# Agar regex ya split use karenge, toh AI ke sentence structure badalte hi code toot jayega.

# ─────────────────────────────────────────────────────────────
# 2. ✅ WHAT — One-Line Definition
# ─────────────────────────────────────────────────────────────
# Structured Output = AI ka response ek fixed Pydantic blueprint mein lena taaki machine usko directly process kar sake.

# ─────────────────────────────────────────────────────────────
# 3. 💡 HOW — Blueprint & Data Flow
# ─────────────────────────────────────────────────────────────
# Socho school admission form ka fixed format:
#   Student Form
#    ├── name   → str (Poora naam)
#    ├── age    → int (5 se 100 ke beech)
#    ├── marks  → int (0 se 100 ke beech)
#    └── result → 'pass' ya 'fail'

# Flow:
#   Unstructured Text
#          ↓
#        LLM
#          ↓
#   with_structured_output(StudentProfile)
#          ↓
#   Pydantic Validation (Checks types & limits)
#          ↓
#   Python Object: student.name, student.marks
#          ↓
#   Database / API


class StudentProfile(BaseModel):
    """Student ka validated data model."""

    name: str = Field(description="Student ka poora naam")
    age: int = Field(ge=5, le=100, description="Student ki umar saalon mein")
    subject: str = Field(description="Subject ka naam jisme marks mile")
    marks: int = Field(ge=0, le=100, description="Marks scored out of 100")
    result: Literal["pass", "fail"] = Field(description="Result status — sirf 'pass' ya 'fail'")
    city: Optional[str] = Field(default=None, description="City ya location agar di gayi ho")


def run_pydantic_demo():
    print("=" * 65)
    print("1. PYDANTIC STRUCTURED OUTPUT DEMO")
    print("=" * 65)

    api_key = os.getenv("GOOGLE_API_KEY")
    llm = None

    if api_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
            print("[INFO] Google Gemini (gemini-2.5-flash) se connect ho gaya.")
        except Exception as e:
            print(f"[WARN] Gemini initialization failed: {e}. Fallback mock use karenge.")
            llm = None

    # Offline / No API Key Fallback Mock
    if llm is None:
        print("[INFO] Running in Demo/Mock mode (No API Key needed).")
        def mock_structured_call(prompt_text):
            return StudentProfile(
                name="Rahul Sharma",
                age=19,
                subject="Physics",
                marks=88,
                result="pass",
                city="New Delhi"
            )
        structured_llm = RunnableLambda(mock_structured_call)
    else:
        # with_structured_output() se LLM ko schema bind karo
        structured_llm = llm.with_structured_output(StudentProfile)

    # Input unstructured text
    user_input = "Rahul Sharma is 19 years old, scored 88 marks in Physics, and lives in New Delhi."
    print(f"\n[Raw Input Text]:\n\"{user_input}\"\n")

    # LLM ko invoke karo
    student: StudentProfile = structured_llm.invoke(user_input)

    # 4. 💻 CODE — Output and Verification
    print("[Structured Object Result]:")
    print(f"Name    : {student.name}")
    print(f"Age     : {student.age}")
    print(f"Subject : {student.subject}")
    print(f"Marks   : {student.marks}")
    print(f"Result  : {student.result}")
    print(f"City    : {student.city}")

    # Pydantic se dictionary aur JSON nikalna
    student_dict = student.model_dump()
    student_json = student.model_dump_json(indent=2)

    print("\n[Exported Dictionary]:", student_dict)
    print("\n[Exported JSON String]:\n", student_json)


if __name__ == "__main__":
    run_pydantic_demo()

# ─────────────────────────────────────────────────────────────
# 🔥 5. YAAD RAKHO:
# Pydantic BaseModel    → Structure + Validation dono deta hai (Recommended)
# Field(description=..) → LLM ko batata hai ki har field mein kya extract karna hai
# ge / le               → Greater-equal aur Less-equal range validation
# Literal[...]          → Strict allowed categories (e.g. 'pass' ya 'fail')
# with_structured_output() → Native function calling se 100% reliable output deta hai
# model_dump()          → Pydantic object ko Python dictionary mein badalta hai
# ─────────────────────────────────────────────────────────────

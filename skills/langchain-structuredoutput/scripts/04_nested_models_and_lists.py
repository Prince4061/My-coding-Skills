"""
04_nested_models_and_lists.py
------------------------------
Topic: Nested Pydantic Models & Lists (Resume Parsing)
Author: Devesh's Coding Style (Why -> What -> How -> Code)
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.runnables import RunnableLambda

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 1. ❌ WHY — Problem Statement
# ═══════════════════════════════════════════════════════════════
# Asli duniya ka data flat nahi hota!
# Ek candidate ke resume mein 3 alag-alag companies ka experience ho sakta hai,
# 5 alag skills ho sakti hain. Single level dictionary mein list of objects
# handle karna mushkil hota hai.

# ─────────────────────────────────────────────────────────────
# 2. ✅ WHAT — One-Line Definition
# ─────────────────────────────────────────────────────────────
# Nested Models = Ek parent Pydantic model ke andar doosre child models ki list banana (Hierarchical Data).

# ─────────────────────────────────────────────────────────────
# 3. 💡 HOW — Blueprint Hierarchy
# ─────────────────────────────────────────────────────────────
# CandidateResume
#  ├── candidate_name   → str
#  ├── total_years_exp  → float
#  ├── key_skills       → list[str]
#  └── past_experience  → list[WorkExperience]
#                           ├── company_name → str
#                           ├── role         → str
#                           ├── years        → float
#                           └── is_current   → bool


class WorkExperience(BaseModel):
    """Ek single company ka past work experience."""
    company_name: str = Field(description="Company ya organization ka naam")
    role: str = Field(description="Job designation / profile")
    years: float = Field(ge=0, description="Duration in years")
    is_current: bool = Field(default=False, description="Kya ye candidate ki current company hai?")


class CandidateResume(BaseModel):
    """Complete candidate resume profile with nested experience."""
    candidate_name: str = Field(description="Candidate ka pura naam")
    email: Optional[str] = Field(default=None, description="Contact email address")
    total_years_exp: float = Field(ge=0, description="Kul kitne saalon ka experience hai")
    key_skills: List[str] = Field(default_factory=list, description="Top skills list")
    past_experience: List[WorkExperience] = Field(description="Har company ke experience ki list")


def run_nested_models_demo():
    print("=" * 65)
    print("4. NESTED MODELS & LISTS DEMO (RESUME PARSER)")
    print("=" * 65)

    api_key = os.getenv("GOOGLE_API_KEY")
    llm = None

    if api_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
            print("[INFO] Google Gemini (gemini-2.5-flash) se connect ho gaya.")
        except Exception as e:
            print(f"[WARN] Model setup error: {e}. Fallback mock use karenge.")
            llm = None

    # Offline Fallback Mock
    if llm is None:
        print("[INFO] Running in Demo/Mock mode (No API Key needed).")
        def mock_resume_call(prompt_text):
            return CandidateResume(
                candidate_name="Priya Sharma",
                email="priya.sharma@example.com",
                total_years_exp=4.5,
                key_skills=["Python", "FastAPI", "Docker", "LangChain"],
                past_experience=[
                    WorkExperience(company_name="Infosys", role="Junior Software Engineer", years=2.0, is_current=False),
                    WorkExperience(company_name="Swiggy", role="Senior Backend Engineer", years=2.5, is_current=True),
                ]
            )
        structured_llm = RunnableLambda(mock_resume_call)
    else:
        structured_llm = llm.with_structured_output(CandidateResume)

    resume_text = (
        "Hi, I am Priya Sharma (priya.sharma@example.com). I have over 4.5 years of experience in backend development. "
        "I started my career at Infosys as a Junior Software Engineer where I spent 2 years working on Python APIs. "
        "After that, I joined Swiggy as a Senior Backend Engineer and have been working there for the last 2.5 years till now. "
        "My primary skills include Python, FastAPI, Docker, and LangChain."
    )

    print(f"\n[Raw Resume Text]:\n\"{resume_text}\"\n")

    # 4. 💻 CODE — Invoke and Inspection
    resume: CandidateResume = structured_llm.invoke(resume_text)

    print("[Parsed Candidate Profile]:")
    print(f"Name         : {resume.candidate_name}")
    print(f"Email        : {resume.email}")
    print(f"Total Exp    : {resume.total_years_exp} years")
    print(f"Key Skills   : {', '.join(resume.key_skills)}")

    print(f"\n[Past Experience Entries ({len(resume.past_experience)})]:")
    for i, exp in enumerate(resume.past_experience, 1):
        status = " (CURRENT)" if exp.is_current else ""
        print(f"  {i}. {exp.company_name} - {exp.role} ({exp.years} years){status}")


if __name__ == "__main__":
    run_nested_models_demo()

# ─────────────────────────────────────────────────────────────
# 🔥 5. YAAD RAKHO:
# List[ChildModel]  → 1-to-many relationship define karne ke liye use hota hai
# Nested Pydantic   → Complex real-world data (Resumes, Invoices, Orders) ke liye best hai
# model_dump()      → Poori nested hierarchy ko clean dictionary mein convert kar deta hai
# ─────────────────────────────────────────────────────────────

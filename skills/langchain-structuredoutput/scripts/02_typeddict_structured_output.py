"""
02_typeddict_structured_output.py
----------------------------------
Topic: LangChain Structured Output with TypedDict
Author: Devesh's Coding Style (Why -> What -> How -> Code)
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langchain_core.runnables import RunnableLambda

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 1. ❌ WHY — Problem Statement
# ═══════════════════════════════════════════════════════════════
# Pydantic powerful hai, par kabhi-kabhi humein extra validation ki zaroorat nahi hoti.
# Humein sirf ek halka-phulka, native Python dictionary chahiye jisme keys pehle se fix hon.

# ─────────────────────────────────────────────────────────────
# 2. ✅ WHAT — One-Line Definition
# ─────────────────────────────────────────────────────────────
# TypedDict = Python ka built-in dictionary structure (zero extra overhead, seedha dict return hota hai).

# ─────────────────────────────────────────────────────────────
# 3. 💡 HOW — Analogy & Data Flow
# ─────────────────────────────────────────────────────────────
# Jaise ek standard receipt jisme sirf 4 columns hain:
#   Receipt
#    ├── item_name   → str
#    ├── sentiment   → str
#    ├── rating      → int
#    └── highlights  → list[str]

# Flow:
#   Customer Review Text
#            ↓
#          LLM
#            ↓
#   with_structured_output(MovieReview)
#            ↓
#   Native Python Dictionary (No Pydantic dependency)


class MovieReview(TypedDict):
    """Customer movie review ka structured dictionary schema."""
    movie_title: Annotated[str, ..., "Film ka naam"]
    sentiment: Annotated[str, ..., "Review ka sentiment: POSITIVE, NEGATIVE, ya MIXED"]
    rating_out_of_10: Annotated[int, ..., "Numerical rating score out of 10"]
    positive_aspects: Annotated[List[str], ..., "Achhi baaton ki list"]
    criticisms: Annotated[List[str], ..., "Kamiyon ya buri baaton ki list"]


def run_typeddict_demo():
    print("=" * 65)
    print("2. TYPEDDICT STRUCTURED OUTPUT DEMO")
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
        def mock_typeddict_call(prompt_text):
            return {
                "movie_title": "Inception",
                "sentiment": "POSITIVE",
                "rating_out_of_10": 9,
                "positive_aspects": ["Mind-bending plot", "Hans Zimmer background score"],
                "criticisms": ["Thoda complex hai, 2 baar dekhna padta hai"]
            }
        structured_llm = RunnableLambda(mock_typeddict_call)
    else:
        # with_structured_output() with TypedDict returns a pure Python dict
        structured_llm = llm.with_structured_output(MovieReview)

    raw_review = (
        "I watched Inception yesterday. The concept of dream within a dream and "
        "Hans Zimmer's background music were unbelievable! It was a bit complicated "
        "to follow at times, but easily a solid 9 out of 10 masterclass."
    )

    print(f"\n[Raw Review Text]:\n\"{raw_review}\"\n")

    # 4. 💻 CODE — Invoke and Inspection
    review_data: MovieReview = structured_llm.invoke(raw_review)

    print("[Extracted Native Dictionary]:")
    print("Type of output :", type(review_data))
    print("Movie Title    :", review_data.get("movie_title"))
    print("Sentiment      :", review_data.get("sentiment"))
    print("Rating (/10)   :", review_data.get("rating_out_of_10"))
    print("Positives      :", review_data.get("positive_aspects"))
    print("Criticisms     :", review_data.get("criticisms"))


if __name__ == "__main__":
    run_typeddict_demo()

# ─────────────────────────────────────────────────────────────
# 🔥 5. YAAD RAKHO:
# TypedDict       → Python built-in typing module ka part hai (no extra installs)
# Annotated[..., "desc"] → Har field ke liye LLM ko description guideline dene ka tareeqa
# Output Type     → Seedha native Python dictionary milta hai (model_dump ki zaroorat nahi)
# Validation      → TypedDict mein runtime validation nahi hoti; agar validation chahiye toh Pydantic use karo
# ─────────────────────────────────────────────────────────────

"""
05_include_raw_and_error_handling.py
-------------------------------------
Topic: include_raw=True and Production Error Handling
Author: Devesh's Coding Style (Why -> What -> How -> Code)
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from langchain_core.runnables import RunnableLambda

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 1. ❌ WHY — Problem Statement
# ═══════════════════════════════════════════════════════════════
# Production mein sirf schema object milna kaafi nahi hota:
# 1. Humein token usage aur latency dekhni hoti hai.
# 2. Agar user ne invalid input diya aur parsing fail ho gayi, toh pura server crash nahi hona chahiye!

# ─────────────────────────────────────────────────────────────
# 2. ✅ WHAT — One-Line Definition
# ─────────────────────────────────────────────────────────────
# include_raw=True = Model ka raw AIMessage + Parsed Object + Error teeno ek dictionary mein lena.

# ─────────────────────────────────────────────────────────────
# 3. 💡 HOW — Dictionary Structure
# ─────────────────────────────────────────────────────────────
# structured_response = {
#     "raw": AIMessage(...),           # Raw message + Token counts
#     "parsed": UserScore(...),        # Validated Pydantic object
#     "parsing_error": None ya Exception
# }


class UserScore(BaseModel):
    """User performance score with strict validation."""
    username: str = Field(description="Player username")
    score: int = Field(ge=0, le=1000, description="Game score between 0 and 1000")
    tier: Literal["bronze", "silver", "gold", "diamond"] = Field(description="Rank tier")


def run_error_handling_demo():
    print("=" * 65)
    print("5. INCLUDE_RAW=TRUE & ERROR HANDLING DEMO")
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
        def mock_include_raw_call(prompt_text):
            return {
                "raw": type("AIMessage", (), {"content": "tool_call", "response_metadata": {"token_usage": {"total_tokens": 42}}})(),
                "parsed": UserScore(username="ProGamer99", score=850, tier="diamond"),
                "parsing_error": None
            }
        structured_llm = RunnableLambda(mock_include_raw_call)
    else:
        # include_raw=True returns dict with 'raw', 'parsed', and 'parsing_error'
        structured_llm = llm.with_structured_output(UserScore, include_raw=True)

    # --- PART A: Happy Path with include_raw=True ---
    print("\n--- PART A: Happy Path (Valid Extraction) ---")
    valid_prompt = "Player ProGamer99 has achieved an epic score of 850 points and unlocked the diamond tier!"
    response = structured_llm.invoke(valid_prompt)

    print("Keys in response:", list(response.keys()))
    print(f"Parsing Error   : {response['parsing_error']}")
    print(f"Parsed Object   : {response['parsed']}")
    print(f"Raw Object Type : {type(response['raw'])}")

    # --- PART B: Manual Pydantic Validation Error Simulation ---
    print("\n--- PART B: Edge Case Validation Catching ---")
    print("Simulating an out-of-range value (score = 5000, max is 1000)...")
    try:
        # Attempting to construct model with invalid bounds
        invalid_user = UserScore(username="HackerX", score=5000, tier="bronze")
        print("Success:", invalid_user)
    except ValidationError as err:
        print("[OK] [CAUGHT EXPECTED VALIDATION ERROR]:")
        for error in err.errors():
            print(f"  Field: {error['loc'][0]} -> Message: {error['msg']}")


if __name__ == "__main__":
    run_error_handling_demo()

# ─────────────────────────────────────────────────────────────
# 🔥 5. YAAD RAKHO:
# include_raw=True   → Raw AIMessage aur Parsed object dono return karta hai
# response["raw"]    → Token usage aur metadata inspect karne ke liye
# response["parsed"] → Actual Pydantic / TypedDict schema object
# ValidationError    → Pydantic ka safety net jo invalid data ko reject karta hai
# ─────────────────────────────────────────────────────────────

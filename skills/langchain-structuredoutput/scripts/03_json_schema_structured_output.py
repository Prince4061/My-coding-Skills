"""
03_json_schema_structured_output.py
------------------------------------
Topic: LangChain Structured Output with Pure JSON Schema (Dict)
Author: Devesh's Coding Style (Why -> What -> How -> Code)
"""

import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 1. ❌ WHY — Problem Statement
# ═══════════════════════════════════════════════════════════════
# Agar humara schema database mein JSON file ki tarah save ho, ya kisi doosri language
# (Node.js, Java, Go) se aa raha ho, toh hum Python ki Pydantic class nahi bana sakte.
# Humein ek standard JSON dictionary format mein schema pass karna hota hai.

# ─────────────────────────────────────────────────────────────
# 2. ✅ WHAT — One-Line Definition
# ─────────────────────────────────────────────────────────────
# JSON Schema = Universal, language-independent blueprint jo kisi bhi framework mein chalta hai.

# ─────────────────────────────────────────────────────────────
# 3. 💡 HOW — Universal Schema Dict
# ─────────────────────────────────────────────────────────────
# Ek standard Python dictionary banate hain JSON Schema specifications ke hisaab se:
# {
#    "title": "...",
#    "type": "object",
#    "properties": { ... },
#    "required": [ ... ]
# }

delivery_order_schema = {
    "title": "FoodDeliveryOrder",
    "description": "Customer ke chat message se food order ki details extract karna",
    "type": "object",
    "properties": {
        "restaurant_name": {
            "type": "string",
            "description": "Restaurant ya dhaba ka naam"
        },
        "food_item": {
            "type": "string",
            "description": "Khaane ka item jo order kiya gaya"
        },
        "quantity": {
            "type": "integer",
            "description": "Kitne plates ya units chahiye"
        },
        "delivery_address": {
            "type": "string",
            "description": "Pura delivery address jahan deliver karna hai"
        },
        "is_urgent": {
            "type": "boolean",
            "description": "Kya customer ne jaldi / express delivery maangi hai?"
        }
    },
    "required": ["restaurant_name", "food_item", "quantity", "delivery_address"]
}


def run_json_schema_demo():
    print("=" * 65)
    print("3. PURE JSON SCHEMA STRUCTURED OUTPUT DEMO")
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
        def mock_json_schema_call(prompt_text):
            return {
                "restaurant_name": "Haldiram",
                "food_item": "Paneer Butter Masala & Butter Naan",
                "quantity": 2,
                "delivery_address": "Flat 402, Sunshine Apartments, Sector 62, Noida",
                "is_urgent": True
            }
        structured_llm = RunnableLambda(mock_json_schema_call)
    else:
        # with_structured_output() with raw JSON Schema dict
        structured_llm = llm.with_structured_output(delivery_order_schema)

    raw_chat = (
        "Bhai Haldiram se 2 plate Paneer Butter Masala aur Butter Naan order kar do. "
        "Delivery address hai Flat 402, Sunshine Apartments, Sector 62, Noida. "
        "Guests baithe hain please bohot jaldi bhejna urgent hai!"
    )

    print(f"\n[Raw Chat Input]:\n\"{raw_chat}\"\n")

    # 4. 💻 CODE — Invoke and Inspection
    order_data = structured_llm.invoke(raw_chat)

    print("[Extracted JSON Schema Data]:")
    print("Restaurant :", order_data.get("restaurant_name"))
    print("Item       :", order_data.get("food_item"))
    print("Quantity   :", order_data.get("quantity"))
    print("Address    :", order_data.get("delivery_address"))
    print("Is Urgent? :", order_data.get("is_urgent"))


if __name__ == "__main__":
    run_json_schema_demo()

# ─────────────────────────────────────────────────────────────
# 🔥 5. YAAD RAKHO:
# JSON Schema       → Universal format (Python, JS, Java sab jagah chalta hai)
# required array    → LLM ko batata hai ki kaun se fields mandatory hain
# properties dict   → Har field ka datatype ("string", "integer", "boolean") define karta hai
# Output Type       → Plain Python dictionary return hota hai
# ─────────────────────────────────────────────────────────────

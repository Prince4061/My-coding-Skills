import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 1. Environment load karo
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("\n[ERROR] GOOGLE_API_KEY nahi mili!")
    print("Kripya .env file me GOOGLE_API_KEY set karein.\n")
    sys.exit(1)

# 2. Model setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5
)

# 3. System Message ke sath chat history initialize karo
# System message bot ka role aur behavior set karta hai
system_instruction = (
    "Tum ek bahut friendly Python aur AI teacher ho. "
    "Hamesha aasan Hinglish bhasha me chhota aur clear explanation do."
)

chat_history = [
    SystemMessage(content=system_instruction)
]

print("=" * 60)
print("  ⚡ Gemini Live Streaming Chatbot (Typing Effect)")
print("  Personality: Friendly AI Teacher")
print("  Type 'exit' or 'quit' to terminate")
print("=" * 60)
print()

while True:
    try:
        user_input = input("You: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nChat band ho gayi.")
        break

    if not user_input:
        continue

    if user_input.lower() in ["exit", "quit"]:
        print("\nDhanyawad! Agli class me milte hain.")
        break

    # 1. User input ko history me jodo
    chat_history.append(HumanMessage(content=user_input))

    print("\nBot: ", end="", flush=True)
    full_reply = ""

    try:
        # 2. llm.stream() se tokens aate hi turant screen par print karo
        for chunk in llm.stream(chat_history):
            content = chunk.content
            print(content, end="", flush=True)
            full_reply += content
        print("\n")

        # 3. Poora reply history me jod do
        chat_history.append(AIMessage(content=full_reply))

        # Memory limit: System message ko preserve karo aur last 10 messages rakho
        if len(chat_history) > 11:
            chat_history = [chat_history[0]] + chat_history[-10:]

    except Exception as e:
        print(f"\n[Error aayi]: {e}\n")

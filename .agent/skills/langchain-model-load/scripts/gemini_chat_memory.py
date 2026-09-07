import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# 1. Environment load karo
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("\n[ERROR] GOOGLE_API_KEY nahi mili!")
    print("Kripya .env file me GOOGLE_API_KEY set karein.\n")
    sys.exit(1)

# 2. Model initialize karo
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7
)

# 3. Memory ke liye plain Python list
chat_history = []

print("=" * 60)
print("  🤖 Gemini Chatbot (List Memory Demo)")
print("  Type 'exit' or 'quit' to terminate chat")
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
        print("\nChatbot band ho gaya. Alvida!")
        break

    # 1. User ka message history me add karo
    chat_history.append(HumanMessage(content=user_input))

    try:
        # 2. Poori chat history model ko pass karo
        response = llm.invoke(chat_history)

        # 3. Model ka reply display karo
        print(f"\nBot: {response.content}\n")

        # 4. Model ka reply bhi history me add karo (taaki next round me yaad rahe)
        chat_history.append(AIMessage(content=response.content))

        # Optional: memory ko 20 messages tak limit rakhna
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

    except Exception as e:
        print(f"\n[Error aayi]: {e}\n")

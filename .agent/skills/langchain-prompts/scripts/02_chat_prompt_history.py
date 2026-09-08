"""
02_chat_prompt_history.py
--------------------------
Demonstrates ChatPromptTemplate with MessagesPlaceholder for multi-turn chat applications:
1. Creating role-based chat prompts (System + Human + AI)
2. MessagesPlaceholder for passing conversation memory
3. Using optional=True to avoid KeyError when history is empty
4. Formatting multi-turn chat conversations
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def demo_chat_prompt_with_history():
    print("=" * 60)
    print("CHATPROMPTTEMPLATE + MESSAGESPLACEHOLDER DEMO")
    print("=" * 60)

    # 1. Define prompt template with system role, placeholder, and human input
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligent code review assistant for {language}. Respond concisely."),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{user_input}"),
    ])

    print("Input variables required:", chat_prompt.input_variables)

    # Turn 1: No chat history yet (optional=True allows chat_history to be omitted or empty)
    print("\n--- TURN 1 (Initial Question, No Prior History) ---")
    turn1_result = chat_prompt.invoke({
        "language": "Python",
        "chat_history": [],
        "user_input": "How do I reverse a dictionary in one line?"
    })

    for i, msg in enumerate(turn1_result.to_messages(), 1):
        print(f"[{i}] {msg.__class__.__name__}: {msg.content}")

    # Turn 2: With conversation history
    print("\n--- TURN 2 (Follow-up Question With History) ---")
    chat_history = [
        HumanMessage(content="How do I reverse a dictionary in one line?"),
        AIMessage(content="You can use dictionary comprehension: `{v: k for k, v in my_dict.items()}`."),
    ]

    turn2_result = chat_prompt.invoke({
        "language": "Python",
        "chat_history": chat_history,
        "user_input": "What happens if there are duplicate values?"
    })

    for i, msg in enumerate(turn2_result.to_messages(), 1):
        print(f"[{i}] {msg.__class__.__name__}: {msg.content}")


if __name__ == "__main__":
    demo_chat_prompt_with_history()

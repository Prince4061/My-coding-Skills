"""
04_lcel_chain_runner.py
------------------------
Demonstrates LCEL (LangChain Expression Language) prompt chaining:
  chain = prompt | model | StrOutputParser()

Loads environment variables using dotenv.
Connects to ChatGoogleGenerativeAI (gemini-2.5-flash) if GOOGLE_API_KEY is available.
If no key is set or offline, falls back gracefully to a RunnableLambda mock.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()


def build_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are an expert software architect. Give 3 clear, numbered architectural principles for {topic}."),
        ("human", "Target Audience: {audience}\nProvide the principles:"),
    ])


def run_lcel_chain():
    print("=" * 60)
    print("LCEL CHAIN RUNNER: prompt | model | StrOutputParser()")
    print("=" * 60)

    prompt = build_prompt()
    parser = StrOutputParser()

    api_key = os.getenv("GOOGLE_API_KEY")
    model = None

    if api_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            # Using gemini-2.5-flash / gemini-flash-latest
            model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
            print("[INFO] Successfully initialized ChatGoogleGenerativeAI (gemini-2.5-flash).")
        except Exception as e:
            print(f"[WARN] Error initializing Gemini model: {e}")
            model = None

    # Fallback demo runnable if no API key or network error occurs
    if model is None:
        print("[INFO] Running with demo Mock LLM (No API key needed).")
        def mock_llm(messages):
            return (
                "1. Decouple services using asynchronous event-driven messaging.\n"
                "2. Maintain strict database-per-service boundaries to avoid shared state.\n"
                "3. Implement centralized distributed tracing and health monitoring."
            )
        model = RunnableLambda(mock_llm)

    # Core LCEL expression: prompt -> model -> output parser
    chain = prompt | model | parser

    input_payload = {
        "topic": "Microservices in Cloud Native Environments",
        "audience": "Senior Backend Engineers"
    }

    print("\n[Input Payload]:", input_payload)
    print("\n[Executing LCEL Chain: prompt | model | parser]...\n")
    try:
        result = chain.invoke(input_payload)
        print("[Chain Output]:")
        print(result)
    except Exception as err:
        print(f"[Error invoking chain]: {err}")


if __name__ == "__main__":
    run_lcel_chain()

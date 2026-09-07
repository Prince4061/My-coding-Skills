"""
Multi-Provider Model Loader Demo for LangChain
Is script me dikhaya gaya hai ki alag-alag LLM providers (Gemini, Groq, OpenAI, Ollama)
ko LangChain me kaise switch aur test kiya ja sakta hai.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def get_model(provider: str, model_name: str = None, temperature: float = 0.5):
    """
    Requested provider ke hisab se LangChain LLM instance return karta hai.
    """
    provider = provider.lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        model = model_name or "gemini-1.5-flash"
        return ChatGoogleGenerativeAI(model=model, temperature=temperature)

    elif provider == "groq":
        from langchain_groq import ChatGroq
        model = model_name or "llama-3.3-70b-versatile"
        return ChatGroq(model=model, temperature=temperature)

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        model = model_name or "gpt-4o-mini"
        return ChatOpenAI(model=model, temperature=temperature)

    elif provider == "ollama":
        from langchain_ollama import ChatOllama
        model = model_name or "llama3.2"
        return ChatOllama(model=model, temperature=temperature)

    else:
        raise ValueError(f"Unknown provider '{provider}'. Choose from: gemini, groq, openai, ollama")


def main():
    print("=" * 60)
    print("  LangChain Multi-Provider Model Loader")
    print("=" * 60)
    print("Options:")
    print("1. Google Gemini (gemini-1.5-flash)")
    print("2. Groq (llama-3.3-70b-versatile)")
    print("3. OpenAI (gpt-4o-mini)")
    print("4. Ollama Local (llama3.2)")
    print("=" * 60)

    choice = input("Select provider [1-4] (Default 1): ").strip() or "1"
    provider_map = {
        "1": "gemini",
        "2": "groq",
        "3": "openai",
        "4": "ollama"
    }

    selected_provider = provider_map.get(choice, "gemini")
    print(f"\nLoading provider: {selected_provider.upper()}...")

    try:
        llm = get_model(selected_provider)
        prompt = input("\nEnter your question/prompt: ").strip() or "What is artificial intelligence in one sentence?"
        print("\nWaiting for response...\n")
        
        response = llm.invoke(prompt)
        print(f"[{selected_provider.upper()} Response]:\n")
        print(response.content)
        print("\n" + "=" * 60)
        print("Success! Model loaded and invoked properly.")

    except ImportError as e:
        print(f"\n[Import Error]: Package missing! {e}")
        print(f"Please install provider package (e.g., pip install langchain-{selected_provider})")
    except Exception as e:
        print(f"\n[Execution Error]: {e}")
        print("Tip: Make sure your API key is correctly set in your .env file.")


if __name__ == "__main__":
    main()

"""
05_prompt_serialization.py
---------------------------
Demonstrates saving and loading LangChain prompts (JSON & YAML):
Method 1: Modern langchain_core.load (dumps / loads / dumpd) - Recommended
Method 2: Classic prompt.save() & load_prompt()
"""

import json
from pathlib import Path
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, load_prompt
from langchain_core.load import dumps, loads


def demo_serialization():
    print("=" * 60)
    print("PROMPT SERIALIZATION & DESERIALIZATION")
    print("=" * 60)

    output_dir = Path(__file__).parent / "saved_prompts"
    output_dir.mkdir(exist_ok=True)

    json_path = output_dir / "summary_prompt.json"
    modern_json_path = output_dir / "modern_chat_prompt.json"

    # --- METHOD 1: Modern Serialization via langchain_core.load (dumps / loads) ---
    print("\n--- 1. MODERN SERIALIZATION (dumps / loads) ---")
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI research assistant specializing in {domain}."),
        ("human", "Explain the concept of {concept} with real-world examples."),
    ])

    # Serialize to JSON string
    serialized_json_str = dumps(chat_prompt, pretty=True)
    with open(modern_json_path, "w", encoding="utf-8") as f:
        f.write(serialized_json_str)
    print(f"Serialized ChatPromptTemplate saved to: {modern_json_path.name}")

    # Load back using loads()
    with open(modern_json_path, "r", encoding="utf-8") as f:
        loaded_chat_prompt = loads(f.read())

    res = loaded_chat_prompt.invoke({"domain": "Quantum Computing", "concept": "Superposition"})
    print("[Loaded Chat Prompt Output Preview]:")
    for msg in res.to_messages():
        print(f"  {msg.__class__.__name__}: {msg.content}")

    # --- METHOD 2: Classic .save() and load_prompt() ---
    print("\n--- 2. CLASSIC SERIALIZATION (.save() & load_prompt()) ---")
    original_prompt = PromptTemplate.from_template(
        "Summarize the following document for an audience of {target_audience}:\n\n{document_text}\n\nKey constraints: Max {max_bullets} bullet points."
    )

    original_prompt.save(json_path)
    print(f"Saved PromptTemplate to: {json_path.name}")

    loaded_from_json = load_prompt(str(json_path))
    prompt_val = loaded_from_json.invoke({
        "target_audience": "Product Managers",
        "document_text": "LangChain provides composable components for LLM application workflows.",
        "max_bullets": 3
    })

    print("\n[Loaded Prompt Invocation Output]:")
    print(prompt_val.to_string())


if __name__ == "__main__":
    demo_serialization()

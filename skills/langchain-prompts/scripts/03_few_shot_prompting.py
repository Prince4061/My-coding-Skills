"""
03_few_shot_prompting.py
-------------------------
Demonstrates few-shot prompting in LangChain:
1. FewShotChatMessagePromptTemplate (for Chat models like Gemini, GPT, Claude)
2. FewShotPromptTemplate (for Text/Completion models)
3. Balanced examples and strict formatting
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    PromptTemplate,
    FewShotPromptTemplate,
)


def demo_chat_few_shot():
    print("=" * 60)
    print("1. FEW-SHOT FOR CHAT MODELS (FewShotChatMessagePromptTemplate)")
    print("=" * 60)

    # Balanced examples covering all classes (Positive, Negative, Neutral)
    examples = [
        {
            "review": "Battery lasts 2 full days and the camera is crystal clear.",
            "sentiment": "POSITIVE",
            "reason": "Battery life and camera quality praised."
        },
        {
            "review": "App crashes immediately upon startup after the latest update.",
            "sentiment": "NEGATIVE",
            "reason": "App crash bug reported."
        },
        {
            "review": "The product arrived in a standard cardboard shipping box.",
            "sentiment": "NEUTRAL",
            "reason": "Neutral statement of fact without opinion."
        },
    ]

    # Template for each example turn
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "Review: {review}"),
        ("ai", "Sentiment: {sentiment}\nReason: {reason}"),
    ])

    # Assemble few-shot component
    few_shot = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt
    )

    # Final prompt with System instructions, Examples, and the New Input
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sentiment classification model. Analyze the review and output strictly Sentiment and Reason."),
        few_shot,
        ("human", "Review: {review}"),
    ])

    # Test invocation
    result = final_prompt.invoke({"review": "Super lightweight headphones, but audio volume is a bit low."})

    print(f"Generated {len(result.to_messages())} messages in the prompt pipeline:\n")
    for i, msg in enumerate(result.to_messages(), 1):
        role = msg.__class__.__name__.replace("Message", "")
        print(f"[{i}] {role.upper()}:")
        print(f"    {msg.content.replace(chr(10), chr(10) + '    ')}")


def demo_text_few_shot():
    print("\n" + "=" * 60)
    print("2. FEW-SHOT FOR TEXT MODELS (FewShotPromptTemplate)")
    print("=" * 60)

    examples = [
        {"word": "happy", "antonym": "sad"},
        {"word": "hot", "antonym": "cold"},
        {"word": "victory", "antonym": "defeat"},
    ]

    example_prompt = PromptTemplate.from_template("Word: {word}\nAntonym: {antonym}")

    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Provide the exact antonym for each word below:",
        suffix="Word: {input_word}\nAntonym:",
        input_variables=["input_word"],
        example_separator="\n---\n",
    )

    result = prompt.invoke({"input_word": "expand"})
    print("[Formatted String Output]:\n")
    print(result.to_string())


if __name__ == "__main__":
    demo_chat_few_shot()
    demo_text_few_shot()

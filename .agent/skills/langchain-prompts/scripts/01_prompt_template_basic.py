"""
01_prompt_template_basic.py
----------------------------
Demonstrates fundamental PromptTemplate usage in LangChain:
1. Creating a PromptTemplate with from_template
2. Formatting and invoking with variables
3. Using .partial() for pre-filled variables
4. Escaping literal curly braces {{ }} for JSON outputs
"""

from langchain_core.prompts import PromptTemplate


def demo_basic_prompt():
    print("=" * 60)
    print("1. BASIC PROMPTTEMPLATE DEMO")
    print("=" * 60)

    # Simple translation template with 2 variables
    template = PromptTemplate.from_template(
        "You are an expert translator. Translate the following text into {language}:\n\n{text}"
    )

    print("Detected input variables:", template.input_variables)

    # In modern LangChain / LCEL, prefer .invoke(dict) over .format()
    prompt_value = template.invoke({
        "language": "Hindi",
        "text": "Artificial Intelligence is transforming software development."
    })

    print("\n[Formatted Prompt Output]:")
    print(prompt_value.to_string())


def demo_partial_variables():
    print("\n" + "=" * 60)
    print("2. PARTIAL VARIABLES (.partial()) DEMO")
    print("=" * 60)

    # Base prompt with company name and query
    base_prompt = PromptTemplate.from_template(
        "Company: {company}\nSupport Tier: {tier}\nUser Query: {query}\n\nPlease draft a polite response."
    )

    # Freeze company and tier so users only need to provide query
    support_prompt = base_prompt.partial(company="TechNova Solutions", tier="Premium Enterprise")

    print("Remaining required variables after .partial():", support_prompt.input_variables)

    # Call with only query
    prompt_value = support_prompt.invoke({"query": "Server CPU utilization is at 98%."})
    print("\n[Partial Prompt Output]:")
    print(prompt_value.to_string())


def demo_json_escaping():
    print("\n" + "=" * 60)
    print("3. JSON ESCAPING (LITERAL BRACES {{ }}) DEMO")
    print("=" * 60)

    # Notice {{ and }} around the JSON structure, while {topic} is the variable
    json_prompt = PromptTemplate.from_template(
        """Extract information about {topic} and format strictly as valid JSON:
{{
    "entity": "{topic}",
    "category": "Technology",
    "status": "active"
}}"""
    )

    prompt_value = json_prompt.invoke({"topic": "LangChain"})
    print("\n[JSON Escaped Output]:")
    print(prompt_value.to_string())


if __name__ == "__main__":
    demo_basic_prompt()
    demo_partial_variables()
    demo_json_escaping()

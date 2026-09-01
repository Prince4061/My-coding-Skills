import os
from typing import Literal
from dotenv import load_dotenv
from tavily import TavilyClient
from deep_agents import create_deep_agent
from langchain.chat_models import init_chat_model

# 1. Load environment variables
load_dotenv()

# 2. Setup Tavily Search Tool
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance", "sports"] = "general",
    include_raw_content: bool = False
):
    """Real-time internet search tool using Tavily API."""
    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content
    )

def main():
    # 3. Model Initialization (Groq / OpenAI)
    model_provider = os.getenv("MODEL_PROVIDER", "groq")
    model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    
    model = init_chat_model(model_name, model_provider=model_provider)

    # 4. Create Deep Agent with planning and tools
    deep_agent = create_deep_agent(
        model=model,
        tools=[web_search],
        system_prompt="Act as an expert AI researcher. Break down tasks into todo items, search the web, synthesize findings, and write detailed reports."
    )

    # 5. Invoke the Agent
    user_prompt = "What are Deep Agents, their 4 pillars, and how do they differ from shallow ReAct agents?"
    print(f"\n[User Query]: {user_prompt}\n")

    result = deep_agent.invoke({
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    })

    # 6. Display Output & Virtual File System Files
    print("\n--- [Agent Response] ---")
    print(result["messages"][-1].content)

    files = result.get("files")
    if files:
        print("\n--- [Created Files in Virtual FS] ---")
        for filename, content in files.items():
            print(f"\n>> {filename}:\n{content}")

if __name__ == "__main__":
    main()

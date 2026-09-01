import os
from pydantic import BaseModel, Field
from typing import List, Literal
from dotenv import load_dotenv
from tavily import TavilyClient
from deep_agents import create_deep_agent
from deep_agents.backends import FileSystemBackend
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

load_dotenv()

# Setup Tavily
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance", "sports"] = "general",
    include_raw_content: bool = False
):
    """Real-time internet search tool."""
    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content
    )

# Pydantic Schema for Structured Output
class ResearchReport(BaseModel):
    title: str = Field(description="Title of the research")
    summary: str = Field(description="Brief executive summary")
    pillars: List[str] = Field(description="Key pillars or core concepts identified")
    citations: List[str] = Field(description="References or sources")

def main():
    model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

    # 1. Specialized Sub-Agent with Structured Output
    structured_worker = model.with_structured_output(ResearchReport)

    @tool
    def research_specialist(topic: str) -> str:
        """Deep research worker that returns structured JSON reports."""
        raw_data = web_search(query=topic)
        result = structured_worker.invoke(f"Analyze and structure this raw research info: {raw_data}")
        return result.model_dump_json(indent=2)

    # 2. Main Deep Agent Orchestrator with FileSystem Backend
    backend = FileSystemBackend(root_dir="./agent_workspace")

    orchestrator = create_deep_agent(
        model=model,
        tools=[research_specialist],
        backend=backend,
        system_prompt="""You are an Orchestrator Deep Agent.
1. Always create a todo plan first.
2. Delegate research to the `research_specialist` sub-agent.
3. Save your synthesized report directly to a file named 'final_report.md' in your virtual file system.
"""
    )

    query = "Analyze the architecture and core pillars of Deep Autonomous Agents."
    print(f"\n[Starting Orchestrator for Query]: {query}\n")

    res = orchestrator.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    print("\n--- [Final Orchestrator Response] ---")
    print(res["messages"][-1].content)

if __name__ == "__main__":
    main()
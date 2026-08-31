# Sub-Agents & Structured Output Delegation

Sub-agents allow a primary Deep Agent to delegate heavy, specialized sub-tasks (e.g. web search synthesis, code auditing, writing long reports) to clean sub-graphs, keeping the parent agent context window lean.

---

## 1. Defining a Sub-Agent

A sub-agent is created using `create_deep_agent` and wrapped inside a LangChain tool.

```python
from pydantic import BaseModel, Field
from deep_agents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# 1. Research Sub-Agent
research_agent = create_deep_agent(
    model=model,
    tools=[web_search],
    system_prompt="You are a deep research sub-agent. Gather facts, filter noise, and return a clean summary."
)

# 2. Wrap Sub-Agent as a Tool for the Main Agent
@tool
def delegate_research(topic: str) -> str:
    """Delegate thorough web research to a specialized sub-agent."""
    response = research_agent.invoke({
        "messages": [{"role": "user", "content": f"Research in detail: {topic}"}]
    })
    return response["messages"][-1].content
```

---

## 2. Structured Output with Pydantic

When the main agent needs strict JSON/Schema data back from a sub-agent:

```python
from pydantic import BaseModel, Field
from typing import List

class ResearchFindings(BaseModel):
    summary: str = Field(description="Executive summary of the research")
    key_points: List[str] = Field(description="Top takeaways")
    sources: List[str] = Field(description="URLs or source references")
    confidence_score: float = Field(description="0.0 to 1.0 confidence score")

structured_subagent = model.with_structured_output(ResearchFindings)

@tool
def structured_research_worker(topic: str) -> str:
    """Performs structured research and returns validated schema data."""
    raw_info = web_search(query=topic)
    structured_result = structured_subagent.invoke(
        f"Extract key findings from this raw research data: {raw_info}"
    )
    return structured_result.model_dump_json(indent=2)
```

---

## 3. Wiring Main Deep Agent with Sub-Agents

```python
main_agent = create_deep_agent(
    model=model,
    tools=[delegate_research, structured_research_worker],
    system_prompt="""You are the Orchestrator Deep Agent. 
Plan tasks using your todo tool. Delegate deep search and extraction to your specialized sub-agent tools. 
Assemble the final output cleanly."""
)
```
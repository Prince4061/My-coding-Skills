---
name: deep-agents-builder
description: Use this skill whenever the user asks to build, create, code, or scaffold a "Deep Agent" (as opposed to a basic/shallow tool-calling agent or a plain ReAct agent) using the `deep-agents` Python library on top of LangChain/LangGraph. Trigger this for phrases like "deep agent banao", "create a deep agent", "deep agents library", "create_deep_agent", "sub-agents with LangGraph", "agent.md memory", "State/FileSystem/Store backend for agents", "progressive disclosure skills for an agent", or any request to set up an agent with planning (to-do list), sub-agents, memory (agent.md), on-demand skills, or virtual file system backends. Always follow the EXACT code structure, import paths, function names, and file layout documented here rather than improvising a different agent framework or a different API shape — the user has an established project convention and expects generated code to match it exactly.
---

# Deep Agents Builder

This skill encodes the exact, canonical code structure for building "Deep Agents" — long-running,
multi-step agents (planning + sub-agents + system prompt/context engineering + virtual file system)
built with the `deep-agents` library on top of LangChain/LangGraph. Use it any time the user wants
code for this stack, and reproduce the patterns below **verbatim in structure** (imports, function
names, argument names), only changing business-specific details (model name, tool logic, prompt text).

## When to use which reference

| Task | File |
|---|---|
| Env setup, Tavily search tool, basic `create_deep_agent` call | this file (below) |
| Choosing/wiring State vs FileSystem vs Store backend | `references/backends.md` |
| Loading `agent.md` memory + on-demand `skills/` (progressive disclosure) | `references/context-engineering.md` |
| Sub-agents + Pydantic structured output delegation | `references/subagents.md` |

Read the relevant reference file(s) before writing code for that part of the task. Several may apply
to one request (e.g. "deep agent with memory, skills, and a research sub-agent" needs all three).

## Core concept map (explain briefly if the user seems new to this)

Evolution: Standalone LLM → Shallow/basic tool-calling agent → ReAct agent (reason+act loop, no
planning/state) → **Deep Agent** (planning tool, sub-agents, system prompt/context engineering,
virtual file system + backends). Reference implementations: Claude Code, Manus AI, ChatGPT Deep
Research.

The four pillars of a Deep Agent:
1. **Planning Tool (To-Do List)** — `write_todos`; breaks a task into tracked sub-tasks instead of executing immediately.
2. **Sub-Agents** — delegate specialized chunks of work (research, coding, report-writing) to keep the main agent's context clean.
3. **System Prompt & Context Engineering** — global rules via `agent.md` (always loaded) + on-demand `skills/` (progressive disclosure, loaded only when needed).
4. **Virtual File System & Backends** — abstracted read/write layer shared between agent and sub-agents; backed by State (RAM), FileSystem (disk), or Store (cross-thread KV).

## 1. Environment setup

Always use `uv`, and this exact package set unless the user says otherwise:

```bash
uv init
uv venv
# Windows: .venv\Scripts\activate | Mac/Linux: source .venv/bin/activate
uv add -r requirements.txt
```

`requirements.txt`:
```text
deep-agents
langchain
langchain-openai
langgraph
groq
tavily-python
python-dotenv
ipykernel
langchain-quickjs
```

## 2. Web search tool (Tavily)

This is the default/canonical tool used across examples. Reuse this exact shape when the agent needs
internet search:

```python
import os
from typing import Literal
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance", "sports"] = "general",
    include_raw_content: bool = False
):
    """Real-time internet search tool using Tavily API"""
    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content
    )
```

## 3. Basic Deep Agent

`create_deep_agent` automatically wires in the planning (to-do) middleware and summarization behind
the scenes — don't build these manually.

```python
import os
from deep_agents import create_deep_agent
from langchain.chat_models import init_chat_model

# Model init — use Groq's llama-3.3-70b-versatile or OpenAI's gpt-4o depending on what the user has keys for
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

deep_agent = create_deep_agent(
    model=model,
    tools=[web_search],
    system_prompt="Act as a researcher"
)

result = deep_agent.invoke({
    "messages": [
        {"role": "user", "content": "What is deep agents?"}
    ]
})

print(result["messages"][-1].content)
# Files the agent created/touched in its virtual file system
print(result.get("files"))
```

Notes:
- `system_prompt` is a plain string for the quick/basic case. When the user also wants persistent
  memory (`agent.md`) see `references/context-engineering.md` — don't hand-roll prompt concatenation.
- Always show `result["messages"][-1].content` for the final answer and `result.get("files")` when
  the task involves file creation, since that's how the virtual file system's output is inspected.

## 4. Putting it together — decide what the request needs

Before writing code, identify which of these the user's request actually needs, and only pull in
that reference material (don't over-engineer a simple ask):

- Just a quick research/tool agent → sections 1–3 above are enough.
- "Remember data across sessions / after restart" → FileSystem backend (`references/backends.md`).
- "Share data between two chats/threads without files on disk" → Store backend (`references/backends.md`).
- "Give it a memory of project rules" → `agent.md` memory (`references/context-engineering.md`).
- "It should know AWS/Python/LangGraph/etc. only when relevant" → Skills / progressive disclosure (`references/context-engineering.md`).
- "Break the task into a research agent + writer agent" or "structured output" → `references/subagents.md`.

## Key takeaways to keep in mind while generating code

- Shallow agents just call a tool and return; Deep Agents decompose the task into a tracked plan first.
- `agent.md` is always-loaded global memory; `skills/*/skill.md` are on-demand, loaded only per-task (progressive disclosure).
- Sub-agents keep the main agent's context window clean by isolating specialized work (and can return Pydantic-typed structured output).
- Backend choice (State vs FileSystem vs Store) is purely about *where* the virtual file system's bytes live — the agent-facing API (`create`, `read`, files dict) doesn't change.
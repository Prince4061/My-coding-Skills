# Backends for Deep Agents

Deep Agents abstract file read/write operations through a **Virtual File System**. The backend determines where these bytes actually reside.

---

## 1. Overview of Backends

| Backend | Storage Location | Persistence | Best For |
|---|---|---|---|
| **StateBackend** | RAM (In-Memory State) | Ephemeral (Lost after run) | Quick runs, temporary evaluations, isolated tests |
| **FileSystemBackend** | Local Disk Directory | Persistent across runs/restarts | Agents working on real codebases, saving outputs to disk |
| **StoreBackend** | LangGraph Store (Key-Value) | Persistent across threads | Multi-user apps, shared memory across different sessions |

---

## 2. State Backend (Default / In-Memory)

Keeps all virtual files inside the agent's LangGraph state graph.

```python
from deep_agents import create_deep_agent
from deep_agents.backends import StateBackend
from langchain.chat_models import init_chat_model

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

backend = StateBackend()

agent = create_deep_agent(
    model=model,
    tools=[web_search],
    backend=backend
)
```

---

## 3. FileSystem Backend (Disk Storage)

Maps the agent's virtual files directly to a directory on disk.

```python
from deep_agents import create_deep_agent
from deep_agents.backends import FileSystemBackend
from langchain.chat_models import init_chat_model

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# Point to a workspace directory
backend = FileSystemBackend(root_dir="./workspace")

agent = create_deep_agent(
    model=model,
    tools=[web_search],
    backend=backend,
    system_prompt="Save all generated research reports directly to disk."
)
```

---

## 4. Store Backend (Cross-Thread Key-Value)

Uses LangGraph's `BaseStore` to persist files across different threads/conversations without touching the local disk.

```python
from langgraph.store.memory import InMemoryStore
from deep_agents import create_deep_agent
from deep_agents.backends import StoreBackend
from langchain.chat_models import init_chat_model

store = InMemoryStore()
backend = StoreBackend(store=store, namespace=("users", "user_123"))

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

agent = create_deep_agent(
    model=model,
    tools=[web_search],
    backend=backend
)
```
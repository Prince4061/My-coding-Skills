# Context Engineering: Memory (agent.md) & Progressive Skills

Deep Agents structure their prompts dynamically to avoid context window bloat while maintaining rules and capabilities.

---

## 1. Two-Tier Context Hierarchy

1. **Global Memory (`agent.md`)**:
   - Always loaded into the system prompt at startup.
   - Contains persona, permanent project constraints, coding standards, and high-level workflow rules.

2. **On-Demand Skills (`skills/`) (Progressive Disclosure)**:
   - Contains specialized task instructions.
   - Only the skill descriptions/metadata are exposed to the agent initially.
   - When the agent realizes a task needs a skill (e.g. `docker-deploy` or `opencv-shape-detection`), it loads that specific `SKILL.md` into context.

---

## 2. Global Memory Setup (`agent.md`)

Create an `agent.md` file in the root:
```markdown
# Agent Identity & Rules
- You are a Senior Research and Software Engineer.
- Always create a todo list using `write_todos` before starting execution.
- Maintain rigorous fact-checking and cite sources.
- Save structured artifacts into the virtual file system.
```

### Loading `agent.md` into Deep Agent

```python
import os
from deep_agents import create_deep_agent
from langchain.chat_models import init_chat_model

def load_system_memory(memory_path: str = "agent.md") -> str:
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are an autonomous Deep Agent."

system_prompt = load_system_memory("agent.md")

model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

agent = create_deep_agent(
    model=model,
    tools=[web_search],
    system_prompt=system_prompt
)
```

---

## 3. Progressive Disclosure Skills Pattern

Instead of dumping 50KB of instructions for all tools at once, expose a tool `load_skill`:

```python
from pathlib import Path

def get_skill_instructions(skill_name: str) -> str:
    """Load detailed instructions for a specific skill on demand."""
    skill_file = Path(f"skills/{skill_name}/SKILL.md")
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    return f"Skill {skill_name} not found."

agent = create_deep_agent(
    model=model,
    tools=[web_search, get_skill_instructions],
    system_prompt=system_prompt + "\nAvailable on-demand skills: [opencv-shape-detection, data-analysis]. Use get_skill_instructions when needed."
)
```
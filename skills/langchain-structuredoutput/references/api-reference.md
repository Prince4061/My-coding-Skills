# LangChain Structured Output — Technical API Reference 🛠️

A comprehensive technical reference for `with_structured_output()` in modern LangChain (1.x / 2.0+).

---

## 1. Overview & Method Signature

```python
structured_llm = llm.with_structured_output(
    schema,
    *,
    method="function_calling",  # Or "json_mode" / "json_schema"
    include_raw=False,          # Returns {"raw": ..., "parsed": ..., "parsing_error": ...}
    **kwargs
)
```

`with_structured_output()` wraps an existing Chat Model (e.g., `ChatGoogleGenerativeAI`, `ChatOpenAI`, `ChatGroq`) and converts its output from an unstructured `AIMessage` into a validated object matching `schema`.

---

## 2. Supported Schema Types

### A. Pydantic `BaseModel` (Recommended)
Provides schema generation, runtime data validation, constraint enforcement, and serialization methods.

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal

class UserProfile(BaseModel):
    """User profile data extracted from conversation."""

    name: str = Field(description="Full legal name")
    age: int = Field(ge=0, le=120, description="Age in completed years")
    role: Literal["admin", "editor", "viewer"] = Field(default="viewer", description="Access level")
    skills: List[str] = Field(default_factory=list, description="Technical skills list")
    bio: Optional[str] = Field(default=None, description="Short biography")

    @field_validator("name")
    def clean_name(cls, v: str) -> str:
        return v.strip().title()
```

**Key Pydantic v2 Methods:**
- `result.model_dump()` ➔ Converts to a native Python `dict`.
- `result.model_dump_json()` ➔ Converts to a formatted JSON string.
- `result.model_json_schema()` ➔ Generates the underlying JSON schema.

---

### B. `TypedDict` (Lightweight Python Dict)
Ideal when you want typed dictionary access without Pydantic's dependency or validation overhead.

```python
from typing import TypedDict, Annotated, List

class ReviewSummary(TypedDict):
    """Extracted sentiment and rating from customer review."""
    sentiment: Annotated[str, ..., "Sentiment classification: POSITIVE, NEGATIVE, or NEUTRAL"]
    score: Annotated[int, ..., "Numerical rating out of 10"]
    highlights: Annotated[List[str], ..., "Key phrases from the review"]
```

---

### C. Pure JSON Schema (Raw Dict)
Language-agnostic standard. Useful when loading schemas dynamically from config files or external APIs.

```python
json_schema = {
    "title": "DeliveryOrder",
    "description": "Order extraction from chat inquiry",
    "type": "object",
    "properties": {
        "item_name": {"type": "string", "description": "Name of food/item"},
        "quantity": {"type": "integer", "description": "Number of units ordered"},
        "delivery_address": {"type": "string", "description": "Full street delivery address"},
    },
    "required": ["item_name", "quantity"]
}
```

---

## 3. Configuration Parameters

### Parameter: `method`
- `"function_calling"` (Default): Uses the model's native tool calling protocol (e.g. Gemini Function Calling, OpenAI Tools). Highest reliability.
- `"json_mode"`: Instructs the model to return valid JSON in its text content, then parses it. (Used by older models or providers without tool calling).
- `"json_schema"`: Uses strict Structured Outputs feature (where supported, e.g., OpenAI `response_format={"type": "json_object"}`).

```python
# Force function calling
structured_llm = llm.with_structured_output(UserProfile, method="function_calling")
```

---

### Parameter: `include_raw`
When `include_raw=True`, `invoke()` returns a dictionary with three keys:
1. `"raw"`: The original `AIMessage` from the model (including token usage, tool calls, and response metadata).
2. `"parsed"`: The parsed schema object (e.g., `UserProfile` or `None` if parsing failed).
3. `"parsing_error"`: The exception instance if parsing/validation failed, or `None`.

```python
structured_llm = llm.with_structured_output(UserProfile, include_raw=True)
result = structured_llm.invoke("Rahul is 24 years old and is an admin.")

raw_message = result["raw"]           # AIMessage
parsed_object = result["parsed"]       # UserProfile(name='Rahul', age=24, role='admin')
error = result["parsing_error"]        # None (or Exception if failed)
```

---

## 4. Complex & Nested Schemas

Pydantic models can be nested infinitely to represent complex hierarchical data.

```python
class JobExperience(BaseModel):
    company: str = Field(description="Company name")
    years: float = Field(description="Total years worked")
    title: str = Field(description="Job title")

class CandidateResume(BaseModel):
    candidate_name: str = Field(description="Full name")
    experience_list: List[JobExperience] = Field(description="List of past jobs")
    current_salary: Optional[int] = Field(default=None, description="Current salary if mentioned")
```

---

## 5. Error Handling & Validation Failures

When input is malformed or violates constraints (e.g. `age=-5`), Pydantic raises a `ValidationError`.

```python
from pydantic import ValidationError
from langchain_core.exceptions import OutputParserException

try:
    result = structured_llm.invoke("Invalid data: age is negative 5.")
except (ValidationError, OutputParserException) as err:
    print(f"Data extraction failed validation: {err}")
    # Fallback to human review or retry chain
```

---

## 6. Comparison Matrix

| Feature | Pydantic (`BaseModel`) | `TypedDict` | JSON Schema (`dict`) |
|---|---|---|---|
| **Runtime Validation** | ✅ Yes (`ge`, `le`, custom) | ❌ No (typing only) | ❌ No (unless external validator) |
| **Field Descriptions** | `Field(description=...)` | `Annotated[..., "desc"]` | `"description": "..."` |
| **Output Type** | Pydantic Model Object | Python `dict` | Python `dict` |
| **Conversion Methods** | `.model_dump()`, `.model_dump_json()` | Native dict | Native dict |
| **Use Case** | Production APIs, DB models, Agents | Quick scripts, lightweight apps | Universal cross-language systems |

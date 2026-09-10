# Devesh's Teaching Code Style Guide 🎓

## Core Philosophy

Every piece of code must follow the **"Why → What → How → Code"** teaching flow.
Code is never just code — it is a lesson. The reader should understand *why*
something exists before seeing *how* it works.

---

## Output Structure (Always follow this order)

### 1. WHY — Problem Statement
Start with a relatable, simple scenario. Show what goes wrong **without** the
concept. Use a plain-English / Hinglish sentence or a tiny broken example.

```text
# ❌ Problem: AI plain text deta hai, machine samajh nahi sakti
response = "Rahul is 18 years old and lives in Delhi."
# Computer ko kaise pata chalega ki name kya hai? age kya hai?
```

### 2. WHAT — One-Line Definition
Give a single memorable "yaad rakhne wali line" that captures the concept.

```text
# ✅ Structured Output = AI ka response ek fixed format/schema mein lena
```

### 3. HOW — Concept Explanation (with analogy if needed)
Use a short analogy or diagram comment to explain the idea before writing the
real code.

```python
# Socho ghar ka blueprint:
#   House
#    ├── Bedroom
#    ├── Kitchen
#    └── Bathroom
# Waise hi data ka blueprint (schema):
#   Student
#    ├── name  → str
#    ├── age   → int
#    └── marks → int
```

### 4. CODE — The Actual Implementation
Write clean, working code. Follow all rules in the **Code Style Rules** section
below.

### 5. YAAD RAKHO — Summary Block
End every lesson snippet with a `# 🔥 Yaad Rakho` comment block that gives the
one-line takeaway per concept introduced.

```python
# 🔥 Yaad Rakho:
# TypedDict  → Dictionary ka structure
# Pydantic   → Structure + Validation
# JSON Schema → Universal JSON blueprint
```

---

## Code Style Rules

### Comments
- **Hinglish only** — mix Hindi explanation with English technical terms.
- Every class and function gets a one-line docstring/comment explaining *kya karta hai* (what it does).
- Inline comments explain *kyun* (why), not *kya* (what the code already shows).
- No filler comments. No `# this is a list` type noise.
- Use `# ❌` for wrong/before examples, `# ✅` for correct/after examples.

```python
# ❌ Bad comment (useless)
age = 18  # age ko 18 set kar rahe hain

# ✅ Good comment (explains why)
age = 18  # Default age — database mein NULL nahi aana chahiye
```

### Variables & Naming
- Use simple, relatable names: `student`, `review`, `resume`, `rahul`.
- Avoid `x`, `y`, `temp`, `foo` — students ko real-world feel deni chahiye.
- Class names: PascalCase English (`Student`, `ProductReview`).
- Variables/functions: snake_case (`get_structured_output`, `parse_review`).

### Structure
- Each concept gets its own clearly separated code block.
- Use section dividers with comments:

```python
# ─────────────────────────────────────────────
# METHOD 1: TypedDict
# ─────────────────────────────────────────────
```

- Show the **before** (broken/unstructured) and **after** (structured) when
  introducing a concept for the first time.

### Flow Diagrams in Comments
Whenever a pipeline or data-flow is involved, draw it as an ASCII comment:

```python
# Flow:
#   Resume (raw text)
#        ↓
#      LLM
#        ↓
#   Structured Output (JSON/Pydantic)
#        ↓
#    Database
```

### Error / Edge Cases
After the happy-path code, briefly show or comment what happens on bad input:

```python
# Agar age = "abc" diya to Pydantic ValidationError raise karega
# Iska matlab data clean karke pass karo
```

---

## Quick Checklist Before Delivering Code

- [ ] **WHY** section hai? (problem statement / before example)
- [ ] **WHAT** section hai? (one-line definition)
- [ ] **HOW** section hai? (analogy / flow diagram)
- [ ] Code mein **Hinglish comments** hain jo *kyun* batate hain?
- [ ] Variables ke naam relatable hain (`student`, `rahul`, `review`)?
- [ ] `# 🔥 Yaad Rakho` block at the end?
- [ ] Koi filler comment toh nahi?

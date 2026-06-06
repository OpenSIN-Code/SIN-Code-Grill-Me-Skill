# Docs: ./grill.py

## What this file does
Core logic for the Grill-Me skill. Defines `GrillSession` (a single
adversarial design-review session) and `QuestionCategory` (the 10
question categories used to interrogate plans).

## Dependency map
- Imports from: stdlib only (`enum`, `json`, `uuid`, `pathlib`, `typing`)
- Imported by: `sin_grill_me.mcp_server`, `sin_grill_me.__init__`, `tests/test_grill.py`

## Important constants
- `total_questions = 10` — the 10 question categories (one per category).
  Adjusting this requires re-deriving the question tree in
  `_generate_question_tree()`.
- `QuestionCategory` — enum with 10 values: ASSUMPTION, EDGE_CASE, SCOPE,
  SUCCESS, ROLLBACK, CONFLICT, SCALE, SECURITY, COST, MIGRATION, DEPENDENCY.

## Why these decisions
- **No async I/O** — all state is in-memory. No database, no network.
- **UUID session IDs** — gives stable, globally-unique IDs without a counter.
- **Fixed 10-question tree** — keeps each grilling session focused. Going
  deeper happens by re-asking the same question with sharper framing,
  not by adding more questions.

## Usage example
```python
session = GrillSession("API design for user auth")
q = session.next_question()  # {"question": "...", "category": "...", "recommended_answer": "..."}
session.record_answer(q["question"], "Users can only edit their own", "Only own profile")
synthesis = session.synthesize()
```

## Known caveats
- In-memory only — sessions vanish on process restart. That's intentional
  (grilling is a transient, conversational activity). If you need
  persistence, store `session.decisions` to disk between calls.
- No LLM integration in this module — it's a state machine. The MCP
  server is a thin wrapper; the actual question *generation* is done
  by the agent invoking the skill.

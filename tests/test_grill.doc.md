# Docs: ./test_grill.py

## What this file does
Pytest suite for `sin_grill_me.grill.GrillSession`. Covers the 6
observable behaviors of a session: init, question issuance, answer
recording, completion detection, synthesis, and category coverage.

## Dependency map
- Imports from: `sin_grill_me.grill` (GrillSession, QuestionCategory), pytest
- Imported by: `pytest` (run via `python -m pytest tests/`)

## Test inventory
| Test | Scenario | Expected |
|---|---|---|
| `test_init` | Fresh session | status=active, 10 questions queued |
| `test_next_question` | First ask | returns unresolved question, counter ++ |
| `test_record_answer` | User answers | decision stored, marked resolved |
| `test_all_questions_resolved` | All 10 answered | status=complete |
| `test_synthesize` | End of session | 5 structured fields returned |
| `test_question_categories` | Question tree | exactly the 10 expected categories |

## Why these decisions
- **No async fixtures** — `GrillSession` is sync, so the test suite is
  sync too. No `pytest-asyncio` needed.
- **No mocking** — `GrillSession` has no I/O, so tests exercise the
  real class. Faster than mocks, no maintenance burden.
- **Tests as documentation** — each test name is a one-line description
  of the scenario. Future maintainers can read the test names and
  understand the contract without reading the implementation.

## Usage example
```bash
cd ~/.config/opencode/skills/sin-grill-me
python3 -m pytest tests/ -v
# Expected: 6 passed in < 1s
```

## Known caveats
- **No coverage threshold configured** — `pyproject.toml` enables
  `pytest-cov` but doesn't enforce a minimum. 100% line coverage is
  achieved today; any drop will be visible in `htmlcov/`.

# Docs: ./__init__.py

## What this file does
Re-exports the two public symbols (`GrillSession`, `QuestionCategory`) so
`from sin_grill_me import GrillSession` works without the `.grill` subpath.

## Dependency map
- Imports from: `sin_grill_me.grill` (GrillSession, QuestionCategory)
- Imported by: downstream skill consumers (MCP server, tests, future scripts)

## Why this is a separate file
- Keeps the package import surface stable — internal refactors of
  `grill.py` don't break callers.
- Centralizes `__all__` so `from sin_grill_me import *` is well-defined.

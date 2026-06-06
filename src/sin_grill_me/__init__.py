# Purpose: SIN Grill-Me Skill package — exposes the public API.
# Docs: __init__.doc.md
"""SIN Grill-Me Skill package.

Exposes the two public symbols: `GrillSession` (the session state) and
`QuestionCategory` (the 10 question categories).
"""

from .grill import GrillSession, QuestionCategory

__all__ = ["GrillSession", "QuestionCategory"]

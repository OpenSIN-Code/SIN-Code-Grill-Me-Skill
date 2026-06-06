# Purpose: Core logic for adversarial design-review grilling sessions.
# Docs: grill.doc.md
"""
Core logic for the Grill-Me skill.

Manages question generation, decision tracking, and synthesis for
adversarial design-review sessions.
"""

import json
import uuid
from enum import Enum
from pathlib import Path
from typing import Any


class QuestionCategory(str, Enum):
    """Categories of grilling questions.

    The 10 categories form a complete review checklist for any
    architecture/design decision. Each one probes a different risk
    surface (assumptions, edge cases, scope, success criteria, etc.).
    """
    ASSUMPTION = "assumption"
    EDGE_CASE = "edge_case"
    SCOPE = "scope"
    SUCCESS = "success"
    ROLLBACK = "rollback"
    CONFLICT = "conflict"
    SCALE = "scale"
    SECURITY = "security"
    COST = "cost"
    MIGRATION = "migration"
    DEPENDENCY = "dependency"


class GrillSession:
    """A single grilling session.

    Holds the state for one adversarial design-review conversation: the
    question tree, recorded decisions, and the synthesis output.

    Lifecycle: init → next_question → record_answer (loop) → synthesize.
    """

    def __init__(self, topic: str, context: str = ""):
        """Initialize a grilling session for the given topic.

        Args:
            topic: What to grill (e.g. "API design for user auth").
            context: Free-form context (codebase files, requirements,
                prior decisions). Stored on `self.context` for the
                agent's reference; not used to generate questions
                (the question tree is fixed at 10 generic categories).
        """
        self.session_id = str(uuid.uuid4())  # UUIDv4 — globally unique without coordination
        self.topic = topic
        self.context = context
        self.status = "active"  # transitions: active → complete → synthesized
        self.questions_asked = 0
        self.questions_remaining = 10  # 10 fixed questions; see _generate_question_tree
        self.total_questions = 10
        self.decisions: list[dict[str, Any]] = []
        self.assumptions: list[dict[str, Any]] = []
        self.out_of_scope: list[str] = []
        self.questions: list[dict[str, Any]] = []
        self._generate_question_tree()

    def _generate_question_tree(self) -> None:
        """Generate the default question tree for a session.

        Fixed 10-question tree — one per `QuestionCategory` value. If you
        add a new category to the enum, append its question here or
        `test_question_categories` will fail.
        """
        self.questions = [
            {
                "question": f"What problem does '{self.topic}' solve? Who has this problem?",
                "category": QuestionCategory.ASSUMPTION.value,
                "recommended_answer": "Clearly define the target user and the specific pain point.",
                "resolved": False,
            },
            {
                "question": "What are the success criteria? How will we know this works in production?",
                "category": QuestionCategory.SUCCESS.value,
                "recommended_answer": "Define measurable metrics (latency, error rate, user satisfaction).",
                "resolved": False,
            },
            {
                "question": "What happens at 10x / 100x / 1000x the current load?",
                "category": QuestionCategory.SCALE.value,
                "recommended_answer": "Design for the expected peak load, with clear scaling bottlenecks identified.",
                "resolved": False,
            },
            {
                "question": "What edge cases and failure modes are not handled?",
                "category": QuestionCategory.EDGE_CASE.value,
                "recommended_answer": "List all known failure modes and the fallback behavior for each.",
                "resolved": False,
            },
            {
                "question": "What external dependencies exist? What if they fail?",
                "category": QuestionCategory.DEPENDENCY.value,
                "recommended_answer": "Map all dependencies and define fallback strategies for each.",
                "resolved": False,
            },
            {
                "question": "What trust boundary does this cross? Who can call it?",
                "category": QuestionCategory.SECURITY.value,
                "recommended_answer": "Define authentication/authorization requirements and threat model.",
                "resolved": False,
            },
            {
                "question": "Is [adjacent feature] in or out of scope? If out, why?",
                "category": QuestionCategory.SCOPE.value,
                "recommended_answer": "Explicitly list in-scope and out-of-scope items with rationale.",
                "resolved": False,
            },
            {
                "question": "What happens if we need to revert this?",
                "category": QuestionCategory.ROLLBACK.value,
                "recommended_answer": "Define rollback strategy and data migration plan.",
                "resolved": False,
            },
            {
                "question": "How do we get from current state to new state without downtime?",
                "category": QuestionCategory.MIGRATION.value,
                "recommended_answer": "Plan phased rollout with feature flags and backfill strategy.",
                "resolved": False,
            },
            {
                "question": "What's the per-request / per-month / per-year cost at expected scale?",
                "category": QuestionCategory.COST.value,
                "recommended_answer": "Calculate infrastructure, API, and operational costs at expected scale.",
                "resolved": False,
            },
        ]

    def next_question(self) -> dict[str, Any]:
        """Get the next unresolved question and mark it as asked.

        Returns:
            Dict with keys: `question`, `category`, `recommended_answer`.
            When all questions are resolved, returns a sentinel dict
            with category="complete" and the synthesis handoff message.

        Side effects:
            Increments `questions_asked`, decrements `questions_remaining`.
            Sets `status = "complete"` when all questions are resolved.
        """
        for q in self.questions:
            if not q["resolved"]:
                self.questions_asked += 1
                self.questions_remaining -= 1
                return q
        self.status = "complete"
        return {
            "question": "All questions resolved. Ready to synthesize.",
            "category": "complete",
            "recommended_answer": "Use grill_synthesize to generate the summary.",
        }

    def record_answer(self, question: str, answer: str, resolution: str = "") -> None:
        """Record a user's answer to a question and mark it resolved.

        Args:
            question: The exact question text (must match an unresolved
                question in the tree).
            answer: The user's free-form answer (stored for context).
            resolution: The concrete, decided outcome — e.g. "Users can
                only edit their own profile". Empty string means "user
                answered but the decision is still open".

        Side effects:
            Marks the matching question resolved. If `resolution` is
            non-empty, appends to `self.decisions`. When all questions
            are resolved, sets `status = "complete"`.
        """
        for q in self.questions:
            if q["question"] == question:
                q["resolved"] = True
                q["answer"] = answer
                q["resolution"] = resolution
                break
        if resolution:
            self.decisions.append({
                "question": question,
                "answer": answer,
                "resolution": resolution,
            })
        if not self._has_unresolved():
            self.status = "complete"

    def _has_unresolved(self) -> bool:
        """Check if any questions are unresolved."""
        return any(not q["resolved"] for q in self.questions)

    def synthesize(self) -> dict[str, Any]:
        """Synthesize the session into decisions and recommendations.

        Returns:
            Dict with 5 keys:
              - `decisions`: list of resolved decision strings
              - `assumptions`: list of resolved questions (what we know)
              - `out_of_scope`: list of unresolved questions (what was skipped)
              - `open_questions`: list of unresolved questions (what's still open)
              - `recommendations`: list of next-step handoff actions

        Side effects:
            Sets `status = "synthesized"`. Idempotent — calling twice
            is safe and returns the same data.
        """
        self.status = "synthesized"
        decisions = [d["resolution"] for d in self.decisions if d["resolution"]]
        assumptions = [q["question"] for q in self.questions if q.get("resolved")]
        out_of_scope = [q["question"] for q in self.questions if not q.get("resolved")]
        open_questions = [q["question"] for q in self.questions if not q.get("resolved")]
        recommendations = [
            "Create PRD with sin-doc-coauthoring",
            "Plan implementation with sin-goal-mode",
            "Run ceo-audit after implementation",
        ]
        return {
            "decisions": decisions,
            "assumptions": assumptions,
            "out_of_scope": out_of_scope,
            "open_questions": open_questions,
            "recommendations": recommendations,
        }

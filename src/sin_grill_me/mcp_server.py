# Purpose: MCP server exposing grill-me tools for adversarial design-review.
# Docs: mcp_server.doc.md
"""
FastMCP server for the SIN Grill-Me skill.

Exposes 5 tools that manage grilling sessions for design/architecture review.
"""

import json
import logging
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

# ── Local imports ─────────────────────────────────────────────────────────────
from .grill import GrillSession, QuestionCategory

# ── Logger ────────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── MCP Server ───────────────────────────────────────────────────────────────
mcp = FastMCP("sin_grill_me")

# ── State ───────────────────────────────────────────────────────────────────
_SESSIONS: dict[str, GrillSession] = {}


def _init_state() -> None:
    """Create storage directory if needed."""
    Path.home().joinpath(".config", "opencode").mkdir(parents=True, exist_ok=True)


def _get_session(session_id: str) -> GrillSession:
    if session_id not in _SESSIONS:
        raise ValueError(f"Session {session_id} not found")
    return _SESSIONS[session_id]


# ── Tools ─────────────────────────────────────────────────────────────────────
@mcp.tool()
async def grill_start(topic: str, context: str = "") -> str:
    """Start a new grilling session.

    Args:
        topic: What to grill (e.g. "API design for user auth")
        context: Additional context (e.g. codebase files, requirements)

    Returns:
        JSON with session_id, topic, and first question.
    """
    session = GrillSession(topic, context)
    _SESSIONS[session.session_id] = session
    question = session.next_question()
    return json.dumps(
        {
            "session_id": session.session_id,
            "topic": topic,
            "status": "active",
            "questions_asked": 1,
            "questions_total": session.total_questions,
            "current_question": question,
        },
        indent=2,
    )


@mcp.tool()
async def grill_status(session_id: str) -> str:
    """Get status of a grilling session.

    Args:
        session_id: The session ID returned by grill_start.

    Returns:
        JSON with session status, questions asked, and resolved decisions.
    """
    session = _get_session(session_id)
    return json.dumps(
        {
            "session_id": session_id,
            "topic": session.topic,
            "status": session.status,
            "questions_asked": session.questions_asked,
            "questions_total": session.total_questions,
            "decisions": session.decisions,
            "assumptions": session.assumptions,
            "out_of_scope": session.out_of_scope,
        },
        indent=2,
    )


@mcp.tool()
async def grill_next_question(session_id: str) -> str:
    """Get the next question for a grilling session.

    Args:
        session_id: The session ID.

    Returns:
        JSON with the next question and recommended answer.
    """
    session = _get_session(session_id)
    question = session.next_question()
    return json.dumps(
        {
            "session_id": session_id,
            "question": question["question"],
            "category": question["category"],
            "recommended_answer": question["recommended_answer"],
            "questions_remaining": session.questions_remaining,
        },
        indent=2,
    )


@mcp.tool()
async def grill_record_answer(session_id: str, question: str, answer: str, resolution: str = "") -> str:
    """Record a user's answer to a grilling question.

    Args:
        session_id: The session ID.
        question: The question text.
        answer: The user's answer.
        resolution: The resolved decision (e.g. "Users can only edit their own profile").

    Returns:
        JSON with updated status and next steps.
    """
    session = _get_session(session_id)
    session.record_answer(question, answer, resolution)
    return json.dumps(
        {
            "session_id": session_id,
            "status": session.status,
            "questions_asked": session.questions_asked,
            "questions_remaining": session.questions_remaining,
            "last_decision": resolution,
        },
        indent=2,
    )


@mcp.tool()
async def grill_synthesize(session_id: str) -> str:
    """Synthesize a grilling session into decisions, assumptions, and next steps.

    Args:
        session_id: The session ID.

    Returns:
        JSON with decisions, assumptions, out-of-scope items, and recommendations.
    """
    session = _get_session(session_id)
    synthesis = session.synthesize()
    return json.dumps(
        {
            "session_id": session_id,
            "topic": session.topic,
            "status": "synthesized",
            "decisions": synthesis["decisions"],
            "assumptions_confirmed": synthesis["assumptions"],
            "out_of_scope": synthesis["out_of_scope"],
            "open_questions": synthesis["open_questions"],
            "recommendations": synthesis["recommendations"],
        },
        indent=2,
    )


def main() -> None:
    """Run the MCP server."""
    _init_state()
    mcp.run()


if __name__ == "__main__":
    main()

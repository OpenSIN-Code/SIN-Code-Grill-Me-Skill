# Purpose: Test suite for sin-grill-me core logic.
# Docs: test_grill.doc.md
"""Tests for the Grill-Me skill."""

import pytest
from sin_grill_me.grill import GrillSession, QuestionCategory


class TestGrillSession:
    """Test cases for GrillSession."""

    def test_init(self):
        """GrillSession initializes with correct defaults."""
        session = GrillSession("API design", "Context here")
        assert session.topic == "API design"
        assert session.context == "Context here"
        assert session.status == "active"
        assert session.total_questions == 10
        assert session.questions_remaining == 10
        assert len(session.questions) == 10

    def test_next_question(self):
        """next_question returns unresolved questions."""
        session = GrillSession("Test topic")
        q = session.next_question()
        assert "question" in q
        assert "category" in q
        assert "recommended_answer" in q
        assert session.questions_asked == 1
        assert session.questions_remaining == 9

    def test_record_answer(self):
        """record_answer marks question resolved and stores decision."""
        session = GrillSession("Test topic")
        q = session.next_question()
        session.record_answer(q["question"], "Users can only edit their own", "Only own profile")
        assert len(session.decisions) == 1
        assert session.decisions[0]["resolution"] == "Only own profile"

    def test_all_questions_resolved(self):
        """Status changes to complete when all questions answered."""
        session = GrillSession("Test topic")
        for _ in range(10):
            q = session.next_question()
            session.record_answer(q["question"], "Answer", "Resolution")
        assert session.status == "complete"

    def test_synthesize(self):
        """synthesize returns structured output."""
        session = GrillSession("Test topic")
        q = session.next_question()
        session.record_answer(q["question"], "Answer", "Resolution")
        result = session.synthesize()
        assert "decisions" in result
        assert "assumptions" in result
        assert "out_of_scope" in result
        assert "open_questions" in result
        assert "recommendations" in result
        assert len(result["decisions"]) == 1
        assert session.status == "synthesized"

    def test_question_categories(self):
        """All questions have valid categories."""
        session = GrillSession("Test topic")
        categories = {q["category"] for q in session.questions}
        expected = {
            "assumption", "success", "scale", "edge_case",
            "dependency", "security", "scope", "rollback",
            "migration", "cost"
        }
        assert categories == expected

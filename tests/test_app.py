"""
Tests for AI Tutor - Smart Learning Assistant
Run with: pytest tests/test_app.py -v
"""

import pytest
import sys
import os

# Allow importing app.py from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import build_prompt


# ── build_prompt: Explain mode ────────────────────────────────────────────────

class TestExplainMode:

    def test_contains_education_level(self):
        result = build_prompt("Explain a Topic", "High School", "Math", "derivatives")
        assert "High School" in result

    def test_contains_subject(self):
        result = build_prompt("Explain a Topic", "High School", "Math", "derivatives")
        assert "Math" in result

    def test_contains_user_input(self):
        result = build_prompt("Explain a Topic", "UG", "Physics", "Newton's laws")
        assert "Newton's laws" in result

    def test_contains_tutor_instruction(self):
        result = build_prompt("Explain a Topic", "School", "Biology", "photosynthesis")
        assert "tutor" in result.lower()

    def test_contains_step_by_step(self):
        result = build_prompt("Explain a Topic", "PG", "Chemistry", "titration")
        assert "step-by-step" in result.lower()

    @pytest.mark.parametrize("level", ["School", "High School", "UG", "PG", "PhD"])
    def test_all_education_levels(self, level):
        result = build_prompt("Explain a Topic", level, "Math", "algebra")
        assert level in result

    @pytest.mark.parametrize("subject", ["Math", "History", "Computer Science", "Physics", "Biology", "Chemistry"])
    def test_all_subjects(self, subject):
        result = build_prompt("Explain a Topic", "High School", subject, "test topic")
        assert subject in result


# ── build_prompt: Quiz mode ───────────────────────────────────────────────────

class TestQuizMode:

    def test_contains_multiple_choice_options(self):
        result = build_prompt("Generate a Quiz", "UG", "Physics", "Newton's laws", num_questions=3)
        assert "A)" in result and "B)" in result and "C)" in result and "D)" in result

    def test_contains_correct_marker(self):
        result = build_prompt("Generate a Quiz", "High School", "History", "World War 2", num_questions=3)
        assert "[CORRECT]" in result

    def test_contains_education_level(self):
        result = build_prompt("Generate a Quiz", "PhD", "Chemistry", "organic reactions", num_questions=2)
        assert "PhD" in result

    def test_contains_subject(self):
        result = build_prompt("Generate a Quiz", "UG", "Biology", "cell division", num_questions=2)
        assert "Biology" in result

    def test_contains_user_topic(self):
        result = build_prompt("Generate a Quiz", "High School", "Math", "quadratic equations", num_questions=3)
        assert "quadratic equations" in result

    def test_contains_explanation_instruction(self):
        result = build_prompt("Generate a Quiz", "School", "Science", "gravity", num_questions=1)
        assert "explanation" in result.lower()

    def test_num_questions_1_reflected_in_prompt(self):
        result = build_prompt("Generate a Quiz", "UG", "Math", "algebra", num_questions=1)
        assert "1" in result

    def test_num_questions_5_reflected_in_prompt(self):
        result = build_prompt("Generate a Quiz", "UG", "Math", "algebra", num_questions=5)
        assert "5" in result

    def test_num_questions_10_reflected_in_prompt(self):
        result = build_prompt("Generate a Quiz", "UG", "Math", "algebra", num_questions=10)
        assert "10" in result

    def test_default_num_questions_is_1(self):
        result = build_prompt("Generate a Quiz", "UG", "Math", "algebra")
        assert "1" in result

    @pytest.mark.parametrize("n", [1, 3, 5, 7, 10])
    def test_various_question_counts(self, n):
        result = build_prompt("Generate a Quiz", "UG", "Math", "calculus", num_questions=n)
        assert str(n) in result

    @pytest.mark.parametrize("level", ["School", "High School", "UG", "PG", "PhD"])
    def test_all_education_levels(self, level):
        result = build_prompt("Generate a Quiz", level, "Math", "algebra", num_questions=2)
        assert level in result


# ── build_prompt: Edge cases ──────────────────────────────────────────────────

class TestEdgeCases:

    def test_returns_string(self):
        result = build_prompt("Explain a Topic", "UG", "Math", "calculus")
        assert isinstance(result, str)

    def test_non_empty_output(self):
        result = build_prompt("Explain a Topic", "School", "History", "ancient Rome")
        assert len(result.strip()) > 0

    def test_explain_and_quiz_prompts_are_different(self):
        explain = build_prompt("Explain a Topic", "UG", "Math", "calculus")
        quiz = build_prompt("Generate a Quiz", "UG", "Math", "calculus", num_questions=3)
        assert explain != quiz

    def test_different_subjects_produce_different_prompts(self):
        math = build_prompt("Explain a Topic", "UG", "Math", "calculus")
        history = build_prompt("Explain a Topic", "UG", "History", "calculus")
        assert math != history

    def test_different_levels_produce_different_prompts(self):
        school = build_prompt("Explain a Topic", "School", "Math", "calculus")
        phd = build_prompt("Explain a Topic", "PhD", "Math", "calculus")
        assert school != phd

    def test_different_question_counts_produce_different_prompts(self):
        q3 = build_prompt("Generate a Quiz", "UG", "Math", "calculus", num_questions=3)
        q7 = build_prompt("Generate a Quiz", "UG", "Math", "calculus", num_questions=7)
        assert q3 != q7

    def test_special_characters_in_input(self):
        result = build_prompt("Explain a Topic", "UG", "Math", "f(x) = x² + 3x − 5")
        assert "f(x)" in result

    def test_long_user_input(self):
        long_input = "explain " + "everything about derivatives " * 20
        result = build_prompt("Explain a Topic", "UG", "Math", long_input)
        assert isinstance(result, str)
        assert len(result) > 0

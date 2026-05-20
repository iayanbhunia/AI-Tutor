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
        result = build_prompt("Explain a Topic", "High School", "subject_a", "some topic")
        assert "High School" in result

    def test_contains_subject(self):
        result = build_prompt("Explain a Topic", "UG", "subject_a", "some topic")
        assert "subject_a" in result

    def test_contains_user_input(self):
        result = build_prompt("Explain a Topic", "UG", "subject_a", "my topic here")
        assert "my topic here" in result

    def test_contains_tutor_instruction(self):
        result = build_prompt("Explain a Topic", "School", "subject_a", "some topic")
        assert "tutor" in result.lower()

    def test_contains_step_by_step(self):
        result = build_prompt("Explain a Topic", "PG", "subject_a", "some topic")
        assert "step-by-step" in result.lower()

    @pytest.mark.parametrize("level", ["School", "High School", "UG", "PG", "PhD"])
    def test_all_education_levels(self, level):
        result = build_prompt("Explain a Topic", level, "subject_a", "some topic")
        assert level in result

    @pytest.mark.parametrize("subject", ["subject_a", "subject_b", "subject_c", "subject_d"])
    def test_any_subject_name_is_included(self, subject):
        result = build_prompt("Explain a Topic", "UG", subject, "some topic")
        assert subject in result

    def test_empty_subject_uses_general(self):
        result = build_prompt("Explain a Topic", "UG", "General", "some topic")
        assert "General" in result

    def test_subject_with_spaces(self):
        result = build_prompt("Explain a Topic", "UG", "my custom subject", "some topic")
        assert "my custom subject" in result


# ── build_prompt: Quiz mode ───────────────────────────────────────────────────

class TestQuizMode:

    def test_contains_multiple_choice_options(self):
        result = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=3)
        assert "A)" in result and "B)" in result and "C)" in result and "D)" in result

    def test_contains_correct_marker(self):
        result = build_prompt("Generate a Quiz", "High School", "subject_a", "some topic", num_questions=3)
        assert "[CORRECT]" in result

    def test_contains_education_level(self):
        result = build_prompt("Generate a Quiz", "PhD", "subject_a", "some topic", num_questions=2)
        assert "PhD" in result

    def test_contains_subject(self):
        result = build_prompt("Generate a Quiz", "UG", "subject_b", "some topic", num_questions=2)
        assert "subject_b" in result

    def test_contains_user_topic(self):
        result = build_prompt("Generate a Quiz", "High School", "subject_a", "my custom topic", num_questions=3)
        assert "my custom topic" in result

    def test_contains_explanation_instruction(self):
        result = build_prompt("Generate a Quiz", "School", "subject_a", "some topic", num_questions=1)
        assert "explanation" in result.lower()

    def test_num_questions_1(self):
        result = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=1)
        assert "1" in result

    def test_num_questions_5(self):
        result = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=5)
        assert "5" in result

    def test_num_questions_10(self):
        result = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=10)
        assert "10" in result

    def test_default_num_questions_is_1(self):
        result = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic")
        assert "1" in result

    @pytest.mark.parametrize("n", [1, 3, 5, 7, 10])
    def test_various_question_counts(self, n):
        result = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=n)
        assert str(n) in result

    @pytest.mark.parametrize("level", ["School", "High School", "UG", "PG", "PhD"])
    def test_all_education_levels(self, level):
        result = build_prompt("Generate a Quiz", level, "subject_a", "some topic", num_questions=2)
        assert level in result

    def test_empty_subject_uses_general(self):
        result = build_prompt("Generate a Quiz", "UG", "General", "some topic", num_questions=3)
        assert "General" in result


# ── build_prompt: Edge cases ──────────────────────────────────────────────────

class TestEdgeCases:

    def test_returns_string(self):
        result = build_prompt("Explain a Topic", "UG", "subject_a", "some topic")
        assert isinstance(result, str)

    def test_non_empty_output(self):
        result = build_prompt("Explain a Topic", "School", "subject_a", "some topic")
        assert len(result.strip()) > 0

    def test_explain_and_quiz_prompts_are_different(self):
        explain = build_prompt("Explain a Topic", "UG", "subject_a", "some topic")
        quiz = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=3)
        assert explain != quiz

    def test_different_subjects_produce_different_prompts(self):
        result_a = build_prompt("Explain a Topic", "UG", "subject_a", "some topic")
        result_b = build_prompt("Explain a Topic", "UG", "subject_b", "some topic")
        assert result_a != result_b

    def test_different_levels_produce_different_prompts(self):
        school = build_prompt("Explain a Topic", "School", "subject_a", "some topic")
        phd = build_prompt("Explain a Topic", "PhD", "subject_a", "some topic")
        assert school != phd

    def test_different_question_counts_produce_different_prompts(self):
        q3 = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=3)
        q7 = build_prompt("Generate a Quiz", "UG", "subject_a", "some topic", num_questions=7)
        assert q3 != q7

    def test_special_characters_in_input(self):
        result = build_prompt("Explain a Topic", "UG", "subject_a", "f(x) = x² + 3")
        assert "f(x)" in result

    def test_long_user_input(self):
        long_input = "explain this " * 30
        result = build_prompt("Explain a Topic", "UG", "subject_a", long_input)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_subject_with_spaces(self):
        result = build_prompt("Explain a Topic", "UG", "my custom subject", "some topic")
        assert "my custom subject" in result

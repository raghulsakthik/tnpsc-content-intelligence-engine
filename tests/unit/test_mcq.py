from engine.mcq.builder import build_mcq
from engine.mcq.models import Difficulty, MCQOption, MCQStatus
from engine.mcq.validator import validate_mcq


def valid_mcq():
    return build_mcq(
        lesson_id="lesson-1",
        curriculum_node_id="node-1",
        question="What is the capital of Tamil Nadu?",
        options=(
            MCQOption("a", "Chennai", True),
            MCQOption("b", "Madurai"),
            MCQOption("c", "Coimbatore"),
            MCQOption("d", "Salem"),
        ),
        explanation="Chennai is the capital of Tamil Nadu.",
        difficulty=Difficulty.EASY,
        source_evidence_ids=("evidence-1",),
    )


def test_builder_creates_draft_with_deterministic_id():
    first = valid_mcq()
    second = valid_mcq()
    assert first.status == MCQStatus.DRAFT
    assert first.mcq_id == second.mcq_id


def test_valid_mcq_passes():
    result = validate_mcq(valid_mcq())
    assert result.valid
    assert result.errors == ()
    assert result.fingerprint


def test_no_correct_answer_fails():
    mcq = valid_mcq()
    options = tuple(MCQOption(o.option_id, o.text, False) for o in mcq.options)
    broken = mcq.__class__(**{**mcq.__dict__, "options": options}) if hasattr(mcq, "__dict__") else None
    # frozen/slots model: rebuild through the builder for a realistic invalid input.
    broken = build_mcq(
        lesson_id=mcq.lesson_id,
        curriculum_node_id=mcq.curriculum_node_id,
        question=mcq.question,
        options=options,
        explanation=mcq.explanation,
        difficulty=mcq.difficulty,
        source_evidence_ids=mcq.source_evidence_ids,
    )
    assert "no-correct-answer" in validate_mcq(broken).errors


def test_multiple_correct_answers_fail():
    mcq = build_mcq(
        lesson_id="lesson-1",
        curriculum_node_id="node-1",
        question="Select the answer.",
        options=(MCQOption("a", "A", True), MCQOption("b", "B", True)),
        explanation="Both are marked correct for this invalid fixture.",
        difficulty=Difficulty.MEDIUM,
        source_evidence_ids=("evidence-1",),
    )
    assert "multiple-correct-answers" in validate_mcq(mcq).errors


def test_duplicate_options_fail():
    mcq = build_mcq(
        lesson_id="lesson-1",
        curriculum_node_id="node-1",
        question="Which option is correct?",
        options=(MCQOption("a", "Chennai", True), MCQOption("b", "Chennai")),
        explanation="Fixture for duplicate option detection.",
        difficulty=Difficulty.EASY,
        source_evidence_ids=("evidence-1",),
    )
    assert "duplicate-option-text" in validate_mcq(mcq).errors


def test_pyq_is_hard_blocked():
    mcq = build_mcq(
        lesson_id="lesson-1",
        curriculum_node_id="node-1",
        question="A previous-year question",
        options=(MCQOption("a", "A", True), MCQOption("b", "B")),
        explanation="Excluded fixture.",
        difficulty=Difficulty.EASY,
        source_evidence_ids=("evidence-1",),
        is_pyq=True,
    )
    result = validate_mcq(mcq)
    assert mcq.status == MCQStatus.EXCLUDED_PYQ
    assert not result.valid
    assert "pyq-mcq-is-not-eligible-for-publication" in result.errors


def test_missing_source_fails():
    mcq = valid_mcq()
    no_source = build_mcq(
        lesson_id=mcq.lesson_id,
        curriculum_node_id=mcq.curriculum_node_id,
        question=mcq.question,
        options=mcq.options,
        explanation=mcq.explanation,
        difficulty=mcq.difficulty,
    )
    assert "source-evidence-required" in validate_mcq(no_source).errors

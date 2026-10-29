from engine.lessons import LessonStatus, build_lesson, lesson_id


def test_lesson_id_is_deterministic():
    assert lesson_id("science", "Cell Structure") == lesson_id("science", "  cell structure ")


def test_builder_preserves_multiple_sources_and_deduplicates():
    lesson = build_lesson(
        curriculum_node_id="science-cell",
        title="Cell Structure",
        concept="Cells are basic structural units.",
        definition="A cell is the basic unit of life.",
        examples=["Plant cell", "Animal cell"],
        revision_notes=["Remember nucleus", "Remember nucleus"],
        source_ids=["ev-1", "ev-1", "ev-2"],
    )
    assert lesson.source_ids == ("ev-1", "ev-2")
    assert lesson.revision_notes == ("Remember nucleus", "Remember nucleus")
    assert lesson.status == LessonStatus.DRAFT
    assert not lesson.is_publishable()


def test_approved_lesson_requires_sources():
    lesson = build_lesson(
        curriculum_node_id="science",
        title="Matter",
        concept="Matter has mass and occupies space.",
    )
    assert not lesson.is_publishable()

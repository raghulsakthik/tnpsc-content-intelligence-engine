from datetime import date

from engine.curriculum.mapper import candidate_nodes
from engine.curriculum.models import CurriculumNode, CurriculumStatus, CurriculumVersion, NodeType
from engine.curriculum.taxonomy import CURRICULUM, SUBJECTS, general_studies_units


def test_curriculum_version_is_explicitly_versioned():
    assert CURRICULUM.id == "tnpsc-group-2-2a-2022-v1"
    assert CURRICULUM.status is CurriculumStatus.ACTIVE
    assert CURRICULUM.effective_from == date(2022, 1, 27)


def test_subjects_have_stable_canonical_keys():
    keys = {node.canonical_key for node in SUBJECTS}
    assert "general-studies" in keys
    assert "aptitude-mental-ability" in keys
    assert "general-tamil" in keys
    assert len(keys) == len(SUBJECTS)


def test_general_studies_units_have_parent():
    units = general_studies_units()
    subject = next(x for x in SUBJECTS if x.canonical_key == "general-studies")
    assert units
    assert all(x.node_type is NodeType.UNIT for x in units)
    assert all(x.parent_id == subject.id for x in units)


def test_exact_mapping_is_deterministic_and_does_not_fuzzy_publish():
    version = CurriculumVersion("v1", "EXAM", "test", date.today())
    node = CurriculumNode(
        id="v1:subject",
        curriculum_version_id=version.id,
        node_type=NodeType.SUBJECT,
        canonical_key="general-studies",
        title_en="General Studies",
        title_ta="பொது அறிவு",
        aliases=("GS",),
    )
    assert candidate_nodes("general studies", (node,))[0].score == 1.0
    assert candidate_nodes("general science", (node,)) == ()

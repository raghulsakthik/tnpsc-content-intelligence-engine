import pytest

from engine.integration.topic_map import validate_platform_topic_map
from engine.integration.publication import PublicationContractError


def export(*topic_ids: str):
    return {"topics": [{"topic_id": topic_id} for topic_id in topic_ids]}


def test_valid_map_is_normalized():
    result = validate_platform_topic_map(
        mapping={"tnpsc-group-2-2a-2022-v1:aptitude": "aptitude.simplification"},
        platform_export=export("aptitude.simplification"),
    )
    assert result == {"tnpsc-group-2-2a-2022-v1:aptitude": "aptitude.simplification"}


def test_unknown_platform_topic_fails_closed():
    with pytest.raises(PublicationContractError, match="unknown-platform-topic"):
        validate_platform_topic_map(
            mapping={"engine-node": "fake.topic"},
            platform_export=export("aptitude.simplification"),
        )


def test_two_engine_nodes_cannot_collapse_into_one_platform_topic():
    with pytest.raises(PublicationContractError, match="target-collision"):
        validate_platform_topic_map(
            mapping={"engine-a": "topic.one", "engine-b": "topic.one"},
            platform_export=export("topic.one"),
        )

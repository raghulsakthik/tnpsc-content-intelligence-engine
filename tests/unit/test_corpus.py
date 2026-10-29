from engine.corpus.models import BatchItem, ItemStatus
from engine.corpus.processor import CorpusProcessor


def test_manifest_is_deterministic():
    items = [
        BatchItem("b", "resource-b", "hash-b"),
        BatchItem("a", "resource-a", "hash-a"),
    ]
    first = CorpusProcessor.manifest("batch", items, "2026-10-29T00:00:00Z")
    second = CorpusProcessor.manifest("batch", reversed(items), "2026-10-29T00:00:00Z")
    assert first == second
    assert first.item_ids == ("a", "b")


def test_completed_item_is_idempotent():
    calls = []

    def stage(item):
        calls.append(item.item_id)
        return item

    processor = CorpusProcessor([("extract", stage)])
    item = BatchItem("a", "resource-a", "hash-a", status=ItemStatus.COMPLETE, stage="complete")
    assert processor.process_item(item) == item
    assert calls == []


def test_failed_stage_can_resume_from_checkpoint():
    state = {"fail": True, "calls": []}

    def extract(item):
        state["calls"].append("extract")
        if state["fail"]:
            state["fail"] = False
            raise RuntimeError("temporary failure")
        return item

    def clean(item):
        state["calls"].append("clean")
        return item

    processor = CorpusProcessor([("extract", extract), ("clean", clean)])
    failed = processor.process_item(BatchItem("a", "resource-a", "hash-a"))
    assert failed.status == ItemStatus.FAILED
    assert failed.stage == "extract"

    resumed = processor.process_item(failed)
    assert resumed.status == ItemStatus.COMPLETE
    assert state["calls"] == ["extract", "extract", "clean"]


def test_duplicate_stage_names_are_rejected():
    def stage(item):
        return item

    try:
        CorpusProcessor([("x", stage), ("x", stage)])
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("duplicate stages should fail")

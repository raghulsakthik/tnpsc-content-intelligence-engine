from engine.ingestion.inventory import inventory_records


def test_inventory_marks_pyq_as_excluded_without_removing_it():
    rows = inventory_records(
        [
            {"resource_id": "1", "is_pyq": True, "sha256": "abc"},
            {"resource_id": "2", "is_pyq": False, "sha256": "def"},
        ]
    )

    assert len(rows) == 2
    assert rows[0].eligibility == "excluded_pyq"
    assert rows[1].eligibility == "candidate"


def test_inventory_accepts_engine_1_content_reference_alias():
    rows = inventory_records(
        [{"resource_id": "x", "content_reference": "/data/a.pdf"}]
    )

    assert rows[0].local_path == "/data/a.pdf"

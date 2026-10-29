from engine.cleaning import CleaningConfig, clean_document


def test_removes_repeated_header_footer_and_page_numbers() -> None:
    pages = [
        "TNPSC Group II\nScience\n1\nPhotosynthesis\nTNPSC Group II",
        "TNPSC Group II\nScience\n2\nRespiration\nTNPSC Group II",
        "TNPSC Group II\nScience\n3\nCells\nTNPSC Group II",
    ]

    result = clean_document(pages)

    assert result.cleaned_pages == (
        "Science\nPhotosynthesis",
        "Science\nRespiration",
        "Science\nCells",
    )
    assert "page-number" in result.removed_patterns
    assert any(item.startswith("repeated-edge:") for item in result.removed_patterns)
    assert result.changed_page_count == 3


def test_does_not_remove_single_occurrence_content() -> None:
    result = clean_document(["Unique heading\nImportant content\n42"])

    assert "Unique heading" in result.cleaned_pages[0]
    assert "Important content" in result.cleaned_pages[0]
    assert "42" not in result.cleaned_pages[0]


def test_cleaning_can_be_disabled() -> None:
    config = CleaningConfig(
        remove_repeated_page_numbers=False,
        remove_repeated_headers_footers=False,
    )
    result = clean_document(["Header\n1\nBody", "Header\n2\nBody"], config)

    assert result.cleaned_pages[0] == "Header\n1\nBody"
    assert result.cleaned_pages[1] == "Header\n2\nBody"

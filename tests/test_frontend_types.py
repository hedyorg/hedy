from website.frontend_types import Adventure


def test_teacher_adventure_falls_back_to_raw_content_when_formatted_is_empty():
    row = {
        "id": "adv1",
        "name": "Adventure One",
        "content": "<p>This should be visible to students.</p>",
        "formatted_content": "<body><pre><code class=\"language-python\"></code></pre></body>",
    }

    adv = Adventure.from_teacher_adventure_database_row(row)

    assert "This should be visible to students." in adv.text


def test_teacher_adventure_prefers_formatted_content_when_it_has_visible_text():
    row = {
        "id": "adv2",
        "name": "Adventure Two",
        "content": "<p>Raw content</p>",
        "formatted_content": "<p>Formatted content</p>",
    }

    adv = Adventure.from_teacher_adventure_database_row(row)

    assert "Formatted content" in adv.text
    assert "Raw content" not in adv.text

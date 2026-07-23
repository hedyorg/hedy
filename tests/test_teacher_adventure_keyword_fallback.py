from unittest.mock import patch

from app import _html_has_visible_text, _translate_teacher_adventure_code_blocks


def test_html_has_visible_text_detects_empty_code_wrapper_as_empty():
    assert _html_has_visible_text('<body><pre><code class="language-python"></code></pre></body>') is False


def test_translate_teacher_adventure_code_blocks_translates_code_tags():
    content = '<p>Intro</p><pre><code class="language-python">print naam</code></pre>'

    with patch('app.hedy_translation.translate_keywords', return_value='imprimir nombre') as translate:
        translated = _translate_teacher_adventure_code_blocks(content, 'nl', 'es', level=1)

    assert 'imprimir nombre' in translated
    assert 'Intro' in translated
    translate.assert_called_once_with('print naam', 'nl', 'es', level=1)


def test_translate_teacher_adventure_code_blocks_skips_empty_code_tags():
    content = '<pre><code class="language-python"></code></pre><pre><code>print naam</code></pre>'

    with patch('app.hedy_translation.translate_keywords', return_value='print nombre') as translate:
        translated = _translate_teacher_adventure_code_blocks(content, 'nl', 'es', level=2)

    assert 'print nombre' in translated
    assert translated.count('<code') == 2
    translate.assert_called_once_with('print naam', 'nl', 'es', level=2)

import glob
import os
import re

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# `{to}` is the range keyword (`{range} 1 {to} 10`), `{to_list}` is the list keyword (`{add} x {to_list} y`).
# Both render as 'to' in English, so a mix-up only breaks in languages where they differ (e.g. de: 'bis' vs 'zu').
ADD_WITH_RANGE_TO = re.compile(r'\{add\}.*\{to\}')

ENGLISH_CONTENT_FILES = sorted(glob.glob(os.path.join(ROOT_DIR, 'content', '*', 'en.yaml')))


@pytest.mark.parametrize('filename', ENGLISH_CONTENT_FILES, ids=lambda f: os.path.relpath(f, ROOT_DIR))
def test_add_uses_to_list_placeholder(filename):
    with open(filename, encoding='utf-8') as f:
        wrong = [f'line {i}: {line.strip()}' for i, line in enumerate(f, start=1) if ADD_WITH_RANGE_TO.search(line)]

    assert not wrong, 'Use {to_list} instead of {to} after {add}:\n' + '\n'.join(wrong)

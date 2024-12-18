import re
from collections import Counter


def validate_output_html(html):
    validate_no_duplicate_ids(html)


ID_RE = re.compile('id="([^"]+)"')


def validate_no_duplicate_ids(html):
    ids = Counter(ID_RE.findall(html))
    duplicates = [id for id, count in ids.items() if count > 1]
    assert not duplicates, 'There are multiple HTML elements with the same id="..." on this page. IDs should be unique: %s' % ', '.join(
        duplicates)

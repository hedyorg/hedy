# For all pofiles, normalize then to reduce the amounts of things that can go wrong.
#
# Currently, specifically:
# - Strips date/time from headers to reduce changes and chances of conflict
from os import path
import os
import re

from config import ROOT_DIR


def scan_pofiles(root, scanner):
    """Return True if there are any problems."""
    for dir, _, files in os.walk(root):
        for file in files:
            if file.endswith('.po') or file.endswith('.pot'):
                fullpath = path.join(dir, file)
                scanner(fullpath)


def strip_headers(filename):
    with open(filename) as f:
        contents = f.read()

    bogus_date = '2000-01-01 00:00+0000'

    replacements = [
        (
            r'^"POT-Creation-Date: [^"]+"$',
            f'"POT-Creation-Date: {bogus_date}\\\\n"'
        ),
        (
            r'^"PO-Revision-Date: [^"]+"$',
            f'"PO-Revision-Date: {bogus_date}\\\\n"'
        ),
        (
            r'^"Last-Translator: [^"]+"$',
            '"Last-Translator: Someone <someone@example.com>\\\\n"'
        ),
    ]

    for search, replace in replacements:
        contents = re.sub(search, replace, contents, flags=re.MULTILINE)

    with open(filename, 'w') as f:
        f.write(contents)


if __name__ == '__main__':
    strip_headers(path.join(ROOT_DIR, 'messages.pot'))
    scan_pofiles(path.join(ROOT_DIR, 'translations'), strip_headers)

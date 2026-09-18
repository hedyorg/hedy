# /usr/bin/env python3
# Remove untranslated entries from the .po files, the way Weblate does.
#
# Weblate runs a "Remove blank strings" add-on over this project, which strips every
# entry that has no translation yet. 'pybabel update' writes those entries back in,
# every time. Neither side gives up, so Weblate's copy of the files is permanently
# ahead of ours: it raises a "repository has changes" alert that never clears, and any
# pull request touching translations meets a diff of a hundred thousand phantom lines.
#
# Writing the files the way Weblate wants them ends that. Nothing is lost: an entry
# with an empty msgstr is dropped by 'pybabel compile' anyway, so it never reaches the
# running site, and Weblate still knows the string exists because it reads the list of
# strings from the English file, not from the translations.
#
# The English file is the exception, and it matters: it is the template every other
# language is derived from. Stripping "untranslated" entries there would delete the
# source strings themselves.
from os import path
import os
import re
import sys


# Keys in the .po header block; the header is an entry with an empty msgid, which we
# must never drop.
HEADER_MSGID = 'msgid ""'


def is_untranslated(entry):
    """Whether this entry has no translation at all.

    An entry looks like this, with any number of comment lines, and strings that may be
    continued over several lines:

        #: path/to/source.py:12
        msgid "Hello"
        msgstr "Hallo"

    Plural entries have a numbered msgstr per plural form, and only count as
    untranslated when every one of them is empty.
    """
    lines = entry.splitlines()
    if lines and lines[0].strip() == HEADER_MSGID:
        return False

    translations = []
    collecting = False
    for line in lines:
        if re.match(r'^msgstr(\[\d+\])? ', line):
            collecting = True
            translations.append(line.split(' ', 1)[1])
        elif collecting and line.startswith('"'):
            translations.append(line)
        elif collecting and not line.startswith('"'):
            collecting = False

    return bool(translations) and all(t.strip() == '""' for t in translations)


def strip_untranslated(filename):
    with open(filename) as f:
        contents = f.read()

    # Entries are separated by blank lines, and the file ends with one.
    entries = contents.split('\n\n')
    kept = [entry for entry in entries if not is_untranslated(entry)]

    if len(kept) == len(entries):
        return 0

    # End on a single newline, which is how Weblate writes these files. Leaving the
    # blank line that dropping the last entry would produce is a byte of difference,
    # and a byte of difference is a merge conflict waiting to happen.
    with open(filename, 'w') as f:
        f.write('\n\n'.join(kept).rstrip('\n') + '\n')

    return len(entries) - len(kept)


def main():
    root = path.join(path.dirname(__file__), '..', '..')
    translations = path.join(root, 'translations')
    template = path.join(translations, 'en', 'LC_MESSAGES', 'messages.po')

    total = 0
    for dir, _, files in os.walk(translations):
        for file in files:
            if not file.endswith('.po'):
                continue
            fullpath = path.join(dir, file)
            if path.samefile(fullpath, template):
                continue
            total += strip_untranslated(fullpath)

    print(f'Removed {total} untranslated entries')


if __name__ == '__main__':
    sys.exit(main())

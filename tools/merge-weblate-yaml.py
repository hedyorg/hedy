#!/usr/bin/env python3
"""Three-way merge of a content YAML file, aware of what the keys mean.

Hedy's translated YAML files have two writers: the team edits them in git, and
translators edit them in Weblate. Git can only merge them as text, so whenever the two
touch the same region of a file the merge conflicts -- and resolving that textually with
'-X ours' (what tools/merge-weblate-resolving-conflicts.sh does) keeps the translations
but silently reverts whatever the team did in the same hunk, deletions included.

Both sides serialize these files with ruamel.yaml under identical settings, so the files
can be merged as trees instead, where each side's intent is actually visible:

  * a key the team deleted stays deleted, even if Weblate still has a translation for it
  * a key translators added stays added, even though 'main' has never seen it
  * a value only one side changed takes that side's version
  * a value both sides changed is a real conflict: 'main' wins, and it gets reported

'main' wins every conflict, deliberately: an edit the team made in git is the version they
expect to ship, and a merge that quietly preferred Weblate would give them no sign that it
had been replaced. The two kinds of conflict are still reported separately, because what a
translator has to do about them differs -- one is a string the team rewrote, the other is a
string the team wrote from scratch while a translator wrote their own. Either way the
translator's version is listed, not discarded silently, so it can be re-applied in Weblate
if it was the better text.

Translations can still be dropped by this, but only deliberately: when the team removes a
whole adventure or level, a translation that only existed inside it goes with it. Those are
reported too, because "the team deleted the level this was written for" is something a
reviewer should see rather than discover from a line count.

With --template, the English file for the component is used as well, and any key a
translator added that it does not have is dropped (and reported with the other drops).
Every language file has to be a structural subset of the English one -- that is what
tools/check-yaml-structure.py enforces in CI -- and a key that only Weblate's side has
can still be missing from it: Weblate cannot pull 'main' while it is in conflict, so its
copy of the English file goes stale, and translators keep translating levels the team
has meanwhile removed. The language file's own history cannot show that removal, because
the key was never in its base; only the template can.

The merge works by mutating a copy of the 'main' side in place, rather than building a
fresh tree. That keeps two things that matter: ruamel's round-trip metadata, which records
the blank lines between keys and would otherwise shift, and 'main' as the key order, so
the resulting pull request reads as a small diff against it.

Usage:
    merge-weblate-yaml.py [--template EN] BASE OURS THEIRS OUT

where BASE is the merge base, OURS is the 'main' side and THEIRS is the Weblate side.
BASE and OURS may be empty files, for a language file that did not exist before or that
only Weblate has. Pass '-' as OUT to write to stdout. Conflicts and dropped translations are listed on
stderr; the exit code is 0 even then, because a reported conflict is a resolved one, and
2 if a file could not be read or has a shape this cannot merge.
"""

import argparse
import copy
import sys
from io import StringIO

from ruamel import yaml as ruamel_yaml

MISSING = object()


def make_yaml():
    # These have to stay in step with tools/rewrite-content-yaml.py, which notes that they
    # match the Weblate YAML settings for every component. A plain round-trip with these
    # settings is a no-op on files from either side, which is what makes a tree merge
    # safe to serialize back.
    yaml = ruamel_yaml.YAML(typ='rt')
    yaml.indent = 4
    yaml.preserve_quotes = True
    yaml.width = 30000
    return yaml


def load(path):
    with open(path, 'r', encoding='utf-8') as fp:
        data = make_yaml().load(fp)
    # An empty file stands for "this side has no such file yet".
    return ruamel_yaml.comments.CommentedMap() if data is None else data


def dump(data, out):
    buf = StringIO()
    make_yaml().dump(data, buf)
    text = buf.getvalue()
    if out == '-':
        sys.stdout.write(text)
        return
    with open(out, 'w', encoding='utf-8') as fp:
        fp.write(text)


def translator_work_in(base, theirs, path):
    """Leaf paths under 'theirs' holding something the base did not have.

    Used to report what a deletion on our side takes with it, so that a translation
    written for an adventure the team has since removed is accounted for rather than
    silently absent.
    """
    if isinstance(theirs, dict):
        base_dict = base if isinstance(base, dict) else {}
        found = []
        for key, value in theirs.items():
            found += translator_work_in(base_dict.get(key, MISSING), value, path + [str(key)])
        return found
    return [] if theirs == base else ['.'.join(path)]


def decide(base, ours, theirs, path, conflicts, coined):
    """Pick a value for a key both sides still have, as a single indivisible value.

    The object itself is returned, never a rebuilt copy, so that ruamel's scalar style
    survives: a '|' block stays a '|' block and a quoted string stays quoted.
    """
    # Weblate dropped it but we still have it. Keep ours: a string disappearing from the
    # Weblate side is usually its own cleanup of untranslated entries, not a request to
    # delete content from the repository.
    if theirs is MISSING:
        return ours

    if ours != base and theirs != base and ours != theirs:
        (coined if base is MISSING else conflicts).append('.'.join(path))
        # 'main' always wins; see the module docstring. The translator's version is
        # reported rather than dropped silently, so it can be re-applied in Weblate.
        return ours
    if theirs != base:
        return theirs
    return ours


def prune_to_template(value, template, path, discarded):
    """Drop keys from 'value' that the template does not have, recursively.

    'template' is None where there is nothing to compare against -- no template given,
    or a part of the file the template does not describe as a mapping -- and then
    nothing is pruned.
    """
    if not isinstance(value, dict) or not isinstance(template, dict):
        return
    for key in list(value.keys()):
        if key not in template:
            discarded.extend(translator_work_in(MISSING, value[key], path + [str(key)]))
            del value[key]
        else:
            prune_to_template(value[key], template[key], path + [str(key)], discarded)


def template_child(template, key):
    return template.get(key) if isinstance(template, dict) else None


def merge_into(target, base, theirs, template, path, conflicts, coined, discarded):
    """Mutate 'target' (a copy of our node) into the merged node."""
    base_dict = base if isinstance(base, dict) else {}
    theirs_dict = theirs if isinstance(theirs, dict) else {}

    for key in list(target.keys()):
        ours_value = target[key]
        base_value = base_dict.get(key, MISSING)
        theirs_value = theirs_dict.get(key, MISSING)

        # Only recurse where both sides still agree this is a mapping. Anything else --
        # a string, a list, a side that replaced a mapping with a scalar -- is decided as
        # one value, which is the conservative reading for lists like 'mp_choice_options'
        # where merging element by element would invent combinations nobody wrote.
        if isinstance(ours_value, dict) and isinstance(theirs_value, dict):
            merge_into(ours_value, base_value, theirs_value, template_child(template, key),
                       path + [str(key)], conflicts, coined, discarded)
            continue

        result = decide(base_value, ours_value, theirs_value, path + [str(key)],
                        conflicts, coined)
        if result is not ours_value:
            target[key] = result

    # Keys we do not have. Either translators added them, or we deleted them.
    for key, theirs_value in theirs_dict.items():
        if key in target:
            continue
        base_value = base_dict.get(key, MISSING)
        if base_value is MISSING:
            if isinstance(template, dict) and key not in template:
                # The team removed it from the English file; see the module docstring.
                discarded.extend(translator_work_in(MISSING, theirs_value, path + [str(key)]))
                continue
            prune_to_template(theirs_value, template_child(template, key),
                              path + [str(key)], discarded)
            target[key] = theirs_value
        else:
            discarded.extend(translator_work_in(base_value, theirs_value, path + [str(key)]))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--template', help='the English file of the same component')
    parser.add_argument('base')
    parser.add_argument('ours')
    parser.add_argument('theirs')
    parser.add_argument('out')
    args = parser.parse_args()

    try:
        base = load(args.base)
        ours = load(args.ours)
        theirs = load(args.theirs)
        template = load(args.template) if args.template else None
    except Exception as e:  # noqa: BLE001 - any read or parse problem means we must not merge
        sys.stderr.write(f'could not read the files to merge: {e}\n')
        return 2

    if not isinstance(ours, dict) or not isinstance(theirs, dict):
        sys.stderr.write('both sides have to be mappings at the top level\n')
        return 2

    merged = copy.deepcopy(ours)
    conflicts = []
    coined = []
    discarded = []
    merge_into(merged, base, theirs, template, [], conflicts, coined, discarded)

    dump(merged, args.out)

    if conflicts:
        sys.stderr.write(
            f"{len(conflicts)} value(s) edited on both sides; kept main's. The "
            f"translator's version for these is in Weblate:\n")
        for item in conflicts:
            sys.stderr.write(f'  {item}\n')
    if coined:
        sys.stderr.write(
            f'{len(coined)} new string(s) written on both sides; kept main\'s. The '
            f'translator wrote their own for these, re-apply in Weblate if preferred:\n')
        for item in coined:
            sys.stderr.write(f'  {item}\n')
    if discarded:
        sys.stderr.write(
            f'{len(discarded)} translation(s) dropped, because the team removed what they '
            f'were written for:\n')
        for item in discarded:
            sys.stderr.write(f'  {item}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# This script reformats all yaml translation files neatly.
# It exits with 1 if any files have been left.
# It is used in the pre-commit configuration of the project.

# The script handles all files sequentally, which is slow, but as the primary
# use case is via the pre-commit hook, which splits to N processes already
# we just keep this script stupid simple.

# One wart: if the filename contains "adventure" we don't strip any
# whitespace from the beginning or end. We could do this via an explicit flag
# but that would make the setup a bit more complex.

# Another wart: the order of yaml keys is hardcoded here,
# for example we want "title" to appear before "story" as titles typically come first.
# This is a bit nasty to maintain and ideally we parse the order from the
# json schema files but that was a lot of work...

import sys
from ruamel import yaml as ruamel_yaml
from io import StringIO
from multiprocessing import Pool


# NOTE: we prefer the dict keys in this order
# this list contains duplicates but that's OK
# some things are maybe inconsistent or suboptimal
# until we integratie with json schema

PREFERRED_KEY_ORDER = [
    "header",  # slide header to come before its text
    # achievements
    "title",
    "text",
    # adventures
    "name",
    "default_save_name",
    "description",
    # "levels", # comment out, else pages push key&intro down the file for common mistakes
    "intro_text",
    "story_text",
    "example_code",
    "story_text_2",
    "example_code_2",
    "story_text_3",
    "example_code_3",
    "story_text_4",
    "example_code_4",
    "story_text_5",
    "example_code_5",
    "story_text_6",
    "example_code_6",
    # cheatsheets
    "name",
    "explanation",
    "example",
    "demo_code",
    # pages
    "title",
    "text",
    "key",
    "intro",
    "levels",
    "subsections",
    "error_text",
    "error_code",
    "solution_text",
    "solution_code",
    # parsons
    "story",
    # "code", #comment out, else quiz code comes before question text
    # quizzes
    "question_text",
    "code",
    "output",
    "mp_choice_options",
    "hint",
    "correct_answer",
    "question_score",
    "option",
    "feedback"
    # slides
    "header",  # add this to the beginning, else text comes first from achievements
    "text",
    "editor",
]


def main():
    filenames = sys.argv[1:]

    with Pool() as p:
        p.map(rewrite_yaml_file, filenames)


def rewrite_yaml_file(fn):
    with open(fn, "r") as fp:
        old_string = fp.read()

    yaml = ruamel_yaml.YAML(typ='rt')
    # Needs to match the Weblate YAML settings for all components
    yaml.indent = 4
    yaml.preserve_quotes = True
    yaml.width = 30000

    data = yaml.load(old_string)
    # adventures contain meaningful whitespace
    data = custom_rewrite_data(data, False)

    out = StringIO()
    yaml.dump(data, out)
    new_string = out.getvalue()
    made_a_change = old_string.strip() != new_string.strip()
    if made_a_change:
        with open(fn, "w") as fp:
            fp.write(new_string)
        sys.stderr.write('x')
    else:
        sys.stderr.write('.')
    sys.stderr.flush()
    return made_a_change


class StringUsedInDictValueNotInKey(str):
    pass


def custom_rewrite_data(obj, strip_strings):
    if isinstance(obj, dict):
        # use a custom order for the dicts
        # as of python 3.7 the value in strings is based on insertion
        # in our system it's nice if "title" comes first and then "text"
        # NOTE that we can finetune this much more, this is just a start
        copy = {}
        for custom_order_key in PREFERRED_KEY_ORDER:
            if custom_order_key in obj:
                copy[custom_order_key] = custom_rewrite_data(
                    obj[custom_order_key], strip_strings
                )
                del obj[custom_order_key]
        for key in sorted(obj.keys()):
            copy[key] = custom_rewrite_data(obj[key], strip_strings)
        return copy
    if isinstance(obj, list):
        # with lists simply recurse into the directory structure
        for (i, el) in enumerate(obj):
            obj[i] = custom_rewrite_data(el, strip_strings)
        return obj
    if isinstance(obj, str):
        # No string ever needs to have leading whitespace, and it messes
        # with rendering and parsing.
        #
        # We could talk about trailing whitespace, but the lack of a trailing
        # `\n` forces the block indicator to `|-` instead of `|`, and it ultimately
        # doesn't matter that much.
        #
        # We could also force all (multiline) strings to be `|` blocks here if
        # we wanted to. For now, we're just messing with things that cause problems.
        #
        # Only replace the original object if we have a change, to not
        # destroy YAML metadata that may be attached to the string.
        stripped = obj.lstrip()
        clazz = type(obj)

        return clazz(stripped) if obj != stripped else obj
    # everything else we leave alone
    return obj


if __name__ == "__main__":
    main()

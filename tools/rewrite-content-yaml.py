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
import yaml
from ruamel import yaml as ruamel_yaml


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
    "start_code",
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
    # patch the yaml implementation to patch our own values
    # we do this because if we use add_representer(`str`, ...)
    # we also change the representation of the keys and not just the values
    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
    yaml.add_representer(
        StringUsedInDictValueNotInKey, repr_str, Dumper=yaml.SafeDumper
    )

    # collect all filenames
    # we can go for argparse if we decide to do something fancier
    filenames = sys.argv[1:]

    made_a_change = False
    for filename in filenames:
        if rewrite_yaml_file(filename, strip_strings="/adventures/" not in filename):
            made_a_change = True

    if made_a_change:
        sys.exit(1)
    else:
        sys.exit(0)


def rewrite_yaml_file(fn, strip_strings):
    with open(fn, "r") as fp:
        old_string = fp.read()
    data = ruamel_yaml.safe_load(old_string)
    # adventures contain meaningful whitespace
    data = custom_rewrite_data(data, strip_strings)
    new_string = yaml.safe_dump(
        data, indent=4, allow_unicode=True, sort_keys=False, width=300
    )
    with open(fn, "w") as fp:
        fp.write(new_string)
    made_a_change = old_string != new_string
    if made_a_change:
        print(f"made a change to {fn} while reformatting the yaml")
    return made_a_change


class StringUsedInDictValueNotInKey(str):
    pass


def repr_str(dumper, data):
    # some yaml has extra newlines at the end, we should try to clean it up
    # but then tests are failing so we should investigate which ones can be cleaned up
    # and which ones can't
    if data.strip_strings:
        data = data.strip()

    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    # we can consider forcing the quotes around all strings, but then some emojis are not
    # visible in the source code due to escaping
    # return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='"')
    return dumper.org_represent_str(data)


def custom_rewrite_data(obj, strip_strings):
    if isinstance(obj, str):
        # patch our own string implementation so that we can finetune the way we render the string
        copy = StringUsedInDictValueNotInKey(obj)
        # Strip strings should not be done for all keys
        copy.strip_strings = strip_strings
        return copy

    elif isinstance(obj, dict):
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
    elif isinstance(obj, list):
        # with lists simply recurse into the directory structure
        return list([custom_rewrite_data(value, strip_strings) for value in obj])
    # everything else we leave alone
    return obj


if __name__ == "__main__":
    main()

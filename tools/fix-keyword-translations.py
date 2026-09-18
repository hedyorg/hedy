from pathlib import Path
from collections.abc import Collection

COLORS = [
    "black",
    "blue",
    "brown",
    "gray",
    "green",
    "orange",
    "pink",
    "purple",
    "red",
    "white",
    "yellow",
]

KEYWORDS = [
    "'False'",
    "'True'",
    "add",
    "and",
    "answer",
    "ask",
    "at",
    "call",
    "clear",
    "color",
    "comma",
    "d0",
    "d1",
    "d2",
    "d3",
    "d4",
    "d5",
    "d6",
    "d7",
    "d8",
    "d9",
    "def",
    "define",
    "echo",
    "elif",
    "else",
    "'false'",
    "for",
    "forward",
    "from",
    "if",
    "in",
    "input",
    "is",
    "left",
    "length",
    "not_in",
    "or",
    "play",
    "pressed",
    "print",
    "quote",
    "random",
    "range",
    "remove",
    "repeat",
    "return",
    "right",
    "sleep",
    "step",
    "times",
    "to",
    "to_list",
    "'true'",
    "turn",
    "while",
    "with",
] + COLORS

COMMON_PAIR_ERRORS = {
    "at random": "{at} {random}",
    "is ask": "{is} {ask}",
    "print hello": "{print} hello",
} | ({f"color {x}": f"{{color}} {{{x}}}" for x in COLORS})

YAML_TRANSLATIONS_DIR = Path("/workspace/content")

INTENDED_ENGLISH = {Path("/workspace/content/pages"): ["for", "repeat"]}


def find_missed_keywords_in_file(path: Path):
    with path.open() as file:
        file_content = file.read()
        for kw in KEYWORDS:
            if f"`{kw}`" in file_content:
                yield kw


def get_english_files(sourceDir: Path, filter: Collection[Path] | None = None):
    for root, _, files in sourceDir.walk():
        if filter and root not in filter:
            continue
        if "en.yaml" in files:
            yield root / "en.yaml"


def find_all_missed_keywords(sourceDir: Path):
    for enFilePath in get_english_files(sourceDir):
        missingKeywords = [x for x in find_missed_keywords_in_file(enFilePath)]
        if missingKeywords:
            yield enFilePath.parent, missingKeywords


def get_yaml_files(sourceDir: Path, filter: Collection[Path] | None = None):
    for root, _, files in sourceDir.walk():
        if filter and root not in filter:
            continue
        for f in files:
            path = root.joinpath(f)
            if path.suffix == ".yaml":
                yield path


def replace_keywords_in_file(path: Path, keywordsToFix: Collection[str]):
    contents = ""
    with path.open(mode="r") as file:
        contents = file.read()
    changed = False
    for kw in keywordsToFix:
        # Ignore intended English commands on Hedy home page.
        if (
            path.parent in INTENDED_ENGLISH.keys()
            and kw in INTENDED_ENGLISH[path.parent]
        ):
            continue

        if f"`{kw}`" in contents:
            changed = True
            contents = contents.replace(f"`{kw}`", f"`{{{kw}}}`")

    for pair, replacement in COMMON_PAIR_ERRORS.items():
        if f"`{pair}`" in contents:
            changed = True
            contents = contents.replace(f"`{pair}`", f"`{replacement}`")

    if changed:
        with path.open(mode="w") as file:
            file.write(contents)


# missingKeywordsPerDirectory = dict(find_all_missed_keywords(YAML_TRANSLATIONS_DIR))

for path in get_yaml_files(YAML_TRANSLATIONS_DIR):
    replace_keywords_in_file(path, KEYWORDS)

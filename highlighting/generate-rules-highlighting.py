import json
import os
import regex as re
import yaml

from definition import TRANSLATE_WORDS

# destinations of files containing syntax highlighting rules
OUTPUT_PATH_TRANSLATION = "highlighting/highlighting-trad.json"

# Files containing translations of keywords
KEYWORDS_PATH = 'content/keywords/'
KEYWORDS_PATTERN = '(\\w+).yaml$'


def main():
    os.chdir(os.path.dirname(__file__) + "/..")

    print("Generation of translations.....................", end="")
    language_keywords = get_translations(KEYWORDS_PATH, KEYWORDS_PATTERN)
    # Saving the rules in the corresponding file
    with open(OUTPUT_PATH_TRANSLATION, "w", encoding='utf8') as file_lang:
        file_lang.write(json.dumps(language_keywords, indent=4, ensure_ascii=False))
    print(" Done !")


def get_yaml_content(file_name):
    """Recover the content of YAML files

    For each yaml file, the function returns a dictionary
    containing the contents of the file.
    All keys and values are strings

    Arguments :
        - file_name : str, The full path of the file

    Returns a dict.
    """

    try:
        with open(file_name, newline="", encoding='utf-8') as keywords_file:
            yaml_file = yaml.safe_load(keywords_file)
    except Exception as e:
        raise RuntimeError(f'Unable to read file {file_name}') from e
    commandes = {}
    for k in yaml_file:
        commandes[str(k)] = str(yaml_file[k])
    return commandes


def get_commands(language_code, keywords, keywords_ref, translate_words):
    """Create keyword translations

    For each language, this function returns a dictionary
    with the translation of the keyword, usable by the regex

    Arguments :
        - language_code : str, Language code (for execption creation)
        - keywords : str, The yaml content of the language you want to translate
        - keywords_ref : str, The content of the reference language yaml
        - translate_words : str, List of keywords to be translated

    Returns a dict.
    """
    R = {}
    for keyword in sorted(keywords.keys()):
        word = keywords[keyword]

        if keyword in translate_words:

            # special case for arabic 'underscore'
            if language_code == "ar":
                ch = "\u0640*"
                word = ch + ch.join(list(word)) + ch

            # if the keyword is identical to the reference, we keep only one of the 2
            if word == keywords_ref[keyword]:
                R[keyword] = "{}".format(keywords_ref[keyword])
            else:
                R[keyword] = "{}|{}".format(word, keywords_ref[keyword])

    return R


def get_digits(keywords, keywords_ref):
    """Create digits translations

    Assembles the digits of the yaml files into a compact regex,
    including the digits of the reference language

    Arguments :
        - keywords : str, The yaml content of the language you want to translate
        - keywords_ref : str, The content of the reference language yaml

    Returns a dict.
    """
    digits = []

    for d in '0123456789':
        # Each digit is keyed as d0, d1, d2, ...
        key = f'd{d}'
        if keywords_ref[key] not in digits:
            digits.append(keywords_ref[key])
        if keywords[key] not in digits:
            digits.append(keywords[key])

    return "".join(digits)


# Function to get the translations of the keywords
def get_translations(KEYWORDS_PATH, KEYWORDS_PATTERN):
    tmp = {}

    list_language_file = os.listdir(KEYWORDS_PATH)

    # get content
    for language_file in list_language_file:
        # Only check *.yaml files
        if m := re.search(KEYWORDS_PATTERN, language_file):
            language_code = m.group(1)
            tmp[language_code] = get_yaml_content(os.path.join(KEYWORDS_PATH, language_file))

    # english is ref
    reference = tmp["en"]

    result = {}
    for language_code in sorted(tmp.keys()):

        # KEYWORDS
        result[language_code] = get_commands(language_code, tmp[language_code], reference, TRANSLATE_WORDS)

        # DIGITS
        result[language_code]["DIGIT"] = get_digits(tmp[language_code], reference)

    return result


if __name__ == '__main__':
    main()

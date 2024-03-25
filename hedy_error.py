import hedy
import hedy_translation
import re
from flask_babel import gettext


# TODO: we should not maintain a list like this. Translation of exception arguments should happen when the exception
#  is created, because then we know what language was used in every part of the code. For example, if a user creates
#  the program `draai 50 forward 10` and mixes the languages of the keywords, an error regarding the turn command
#  should use `draai` and an error about the forward command - `forward`.
arguments_that_require_translation = [
    'allowed_types',
    'invalid_type',
    'invalid_type_2',
    'offending_keyword',
    'character_found',
    'concept',
    'tip',
    'else',
    'command',
    'incomplete_command',
    'missing_command',
    'print',
    'ask',
    'echo',
    'is',
    'if',
    'repeat',
    'suggestion_color',
    'suggestion_note',
    'suggestion_number',
    'suggestion_numbers_or_strings'
]


def get_error_text(ex, lang):
    """ Return a translated and highlighted text of the provided HedyException """
    # TODO: TB -> We have to find a more delicate way to fix this: returns some gettext() errors
    error_template = gettext('' + str(ex.error_code))
    arguments = ex.arguments

    # Some of the arguments like 'allowed_types' or 'characters' need to be translated in the error message
    for k, v in arguments.items():
        if k in arguments_that_require_translation:
            arguments[k] = _translate_error_arg(v, lang)

    # Some of the already translated arguments like 'tip' and 'allowed_types' are translated to text, which
    # in turn needs to be translated/highlighted. Atm we explicitly allow for 1 level of nested translation.
    for k, v in arguments.items():
        if k in arguments_that_require_translation:
            nested_arguments = _extract_nested_arguments(v, lang)
            if nested_arguments:
                arguments[k] = v.format(**nested_arguments)

    # Errors might contain hardcoded references to commands which are not supplied in the arguments, e.g. {print}, {ask}
    arguments.update(_get_missing_arguments(error_template, arguments, lang))

    # Do not use a safe_format here. Every exception is tested against every language in tests_translation_error
    result = error_template.format(**arguments)
    return _highlight(result)


def _highlight(input_):
    """ Add highlight styling to the parts in the input surrounded by backticks, for example:
    '`print` is incorrect' becomes '<span class="command-highlighted">print</span> is incorrect'
    This is a simple implementation that does not allow escaping backticks. Extend it in the future if needed. """
    quote_positions = [i for i, x in enumerate(input_) if x == "`"]
    quotes_even = len(quote_positions) % 2 == 0
    if not quote_positions or not quotes_even:
        return input_

    quote_positions.insert(0, 0)
    result = []
    for i, position in enumerate(quote_positions):
        start_ = position if i == 0 else position + 1
        end_ = quote_positions[i+1] if i + 1 < len(quote_positions) else len(input_)
        if start_ < end_:
            part = input_[start_:end_]
            is_highlighted = i % 2 == 1
            result.append(hedy.style_command(part) if is_highlighted else part)
    return ''.join(result)


def _get_keys(input_):
    pattern = r'\{([^}]*)\}'
    return re.findall(pattern, input_)


def _get_missing_arguments(input_, args, lang):
    """ Discover and translate keywords used in the template which are missing from the arguments, e.g. {print} """
    matches = _get_keys(input_)
    existing_keywords = hedy_translation.keywords_to_dict_single_choice(lang)
    used_keys = [k for k in matches if k not in args and k in existing_keywords]
    translated_keywords = {k: _translate_error_arg(k, lang) for k in used_keys}
    return translated_keywords


def _extract_nested_arguments(template, lang):
    used_keys = _get_keys(template)
    return {k: _translate_error_arg(k, lang) for k in used_keys}


def _translate_error_arg(arg, lang):
    if isinstance(arg, list):
        return _translate_list(arg, lang)

    return _translate(arg, lang)


def _translate_list(args, lang):
    translated_args = [_translate(a, lang) for a in args]
    # deduplication is needed because diff values could be translated to the same value, e.g. int and float => a number
    translated_args = list(dict.fromkeys(translated_args))

    if len(translated_args) > 1:
        return f"{', '.join(translated_args[0:-1])}" \
            f" {gettext('or')} " \
            f"{translated_args[-1]}"
    return ''.join(translated_args)


def _translate(v, language):
    translation = gettext('' + str(v))
    # if there is no translation available, probably this is a keyword
    if v == translation:
        translation = hedy_translation.translate_keyword_from_en(v, language)
    return translation

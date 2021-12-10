"""
File with quiz logic.

Today, this does not yet contain the Flask routers, although in the future it
should (once we can move the code because we have vanquished the global variables).

For now, it contains helper functions that work on the quiz data.
"""

from website.yaml_file import YamlFile

MAX_ATTEMPTS = 3


def quiz_data_file_for(lang, level):
    quiz_file = YamlFile.for_file(f'coursedata/quizzes/{lang}.yaml')
    if not quiz_file.exists():
        return None
    if level not in quiz_file['levels'].keys():
        return None
    return quiz_file['levels'][level]


def get_question(quiz_data, question_number):
    """Return the question from the data based on a 1-based question_number.

    Return None if no such question.
    """
    return quiz_data.get(question_number)


def is_correct_answer(question, letter):
    return question['correct_answer'] == letter


def get_correct_answer(question):
    """Return the correct answer option from a question."""
    i = index_from_letter(question['correct_answer'])
    return question['mp_choice_options'][i]


def get_hint(question, letter):
    i = index_from_letter(letter)
    return question['mp_choice_options'][i].get('feedback')


def highest_question(quiz_data):
    """Return the highest possible question for the given level."""
    return len(quiz_data)


def correct_answer_score(question):
    return question['question_score']


def max_score(quiz_data):
    index = 1
    max_score = 0
    for question_key, question_value in quiz_data.items():
        index = index + 1
        max_score = max_score + question_value['question_score']
    return max_score


def question_options_for(question):
    """Return a list with a set of answers to the question.

    Returns:
        [
            {
                option_text: '...',
                code: '...',
                feedback: '...',
                char_index: 'A',
            }
        ]
    """
    return [
        dict(**answer, char_index=letter_from_index(i))
        for i, answer in enumerate(question['mp_choice_options'])]


def escape_newlines(x):
    return x.replace("\n", '\\n')


def index_from_letter(letter):
    """Turn A -> 0, B -> 1 etc."""
    return ord(letter) - ord('A')


def letter_from_index(ix):
    """Turn 0 -> A, 1 -> B, etc."""
    return chr(ord('A') + ix)

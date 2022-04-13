import json
import uuid

from config import config
from website import statistics
from website.auth import current_user
import utils
from flask import request, g, session, redirect, url_for
from flask_helpers import render_template
from website.yaml_file import YamlFile

MAX_ATTEMPTS = 3

icons = {
    'check': '<svg class="check-icon" viewBox="0 0 50 50"><polygon class="check" points="34.6 4.51 21.43 29.93 16.17 20.98 5.48 30.77 22.04 45.16 46.33 11.62 34.6 4.51"></polygon></svg>',
    'cross': '<svg class="cross-icon" viewBox="0 0 50 50"><polygon class="cross" points="5.17 38.3 18.43 26.08 8.03 14.12 16.74 6.05 27.14 18.02 39.88 6.32 46.91 14.37 34.16 26.08 44.56 37.91 35.85 46.1 25.45 34.27 12.32 46.36 5.17 38.3"></polygon></svg>',
    'triangle': '<svg class="option-icon" viewBox="0 0 50 50"><polygon class="shape" points="25.04 1.95 0.79 43.95 49.28 43.95 25.04 1.95"></polygon><path class="number" d="M22.4,32.66,23.51,22.12H19.62l.43-4.1h8.6l-.43,4.1L27.11,32.66h3.52l-.43,4.1H18.08l.43-4.1Z"></path></svg>',
    'diamond': '<svg class="option-icon" viewBox="0 0 50 50"><rect class="shape" x="7.68" y="7.67" width="34.64" height="34.64" transform="translate(-10.35 25.00) rotate(-45)"></rect><path class="number" d="M17.07,23.35l1.36-5.50a19.53,19.53,0,0,1,7.23-1.4c5.11,0,6.8,2.34,6.8,5,0,5.07-6.04,7.48-11.05,10.00h6.98l.4-2.62,3.70.36-.79,6.37H15.70l-.03-3.81C21.79,28.07,27.3,25.48,27.3,22.49c0-1.44-1.3-1.94-2.88-1.94a7.35,7.35,0,0,0-2.91.54l-.82,2.66Z"></path></svg>',
    'square': '<svg class="option-icon" viewBox="0 0 50 50"><rect class="shape" x="7.03" y="6.49" width="37" height="37"></rect><path class="number" d="M18.97,21.07l1.22-5.05a18.39,18.39,0,0,1,6.63-1.28c3.6,0,6.23,1.45,6.23,4.85,0,2.17-1.08,4.19-4.15,5.44l-.03.13c2.70.59,3.86,2.24,3.86,4.85,0,4.55-3.53,6.9-8.21,6.9-4.65,0-7.32-2.27-7-5.90l3.63-1.08c-.16,1.51.85,3.23,3.4,3.23a3.26,3.26,0,0,0,3.53-3.43c0-2.08-1.55-2.77-4.62-2.90l.3-2.9c4.48,0,4.55-2.77,4.55-3.2,0-1.41-.72-2.21-2.54-2.21a7.06,7.06,0,0,0-2.73.5l-.76,2.44Z"></path></svg>',
    'circle': '<svg class="option-icon" viewBox="0 0 50 50"><circle class="shape" cx="24.55" cy="25.02" r="20.5"></circle><path class="number" d="M24.06,36.83l.59-5.64H15.35l-.03-3.66,7.62-12.17h7.69L29.34,27.52h3.23l-.72,3.66H28.98l-.59,5.64Zm1.84-17.72H24.4l-5.04,8.41h5.67Z"></path></svg>',
    'pentagram': '<svg class="option-icon" viewBox="0 0 50 50"><polygon class="shape" points="25.24 2.93 3.42 18.78 11.76 44.42 38.72 44.42 47.05 18.78 25.24 2.93"></polygon><path class="number" d="M23.97,36.87c-4.38,0-6.97-2.04-6.65-5.72l3.52-1.05c-.16,1.47.73,3.13,3.2,3.13a3.23,3.23,0,0,0,3.51-3.42c0-2.43-2.07-2.94-4.44-2.94-1.02,0-2.08.09-3.00.16l-1.21-1.31L19.94,15.69H32.48l-.03,5.85-3.58.32-.31-2.52h-5.12l-.41,4.06c.38-.03.8-.03,1.18-.03,4.38,0,7.93,1.18,7.93,6.24C32.13,34.7,28.51,36.87,23.97,36.87Z"></path></svg>',
    'triangle_6': '<svg class="option-icon" viewBox="0 0 50 50"><polygon class="shape" points="25.03 1.95 0.78 43.95 49.28 43.95 25.03 1.95"></polygon><path class="number" d="M24.01,36.97c-4.41,0-6.45-3.05-6.45-8.33,0-5.31,2.07-11.76,8.78-11.76,2.19,0,4.47.69,5.61,2.7l-2.48,2.31a4.00,4.00,0,0,0-3.36-1.59c-2.58,0-3.80,1.98-4.26,6.21a5.46,5.46,0,0,1,4.71-2.43c3.53,0,4.8,2.64,4.8,5.46A7.06,7.06,0,0,1,24.01,36.97Zm.9-9.62a3.03,3.03,0,0,0-3.21,2.7c-.03,2.31.57,3.39,2.49,3.39,2.22,0,3.09-1.5,3.09-3.48C27.28,28.3,26.68,27.34,24.91,27.34Z"></path></svg>',
}


def routes(app, database, achievements):
    global DATABASE
    global ACHIEVEMENTS
    DATABASE = database
    ACHIEVEMENTS = achievements

    @app.route('/quiz/start/<int:level>', methods=['GET'])
    def get_quiz_start(level):
        if not is_quiz_enabled():
            return quiz_disabled_error()

        # A unique identifier to record the answers under
        session['quiz-attempt-id'] = uuid.uuid4().hex

        # Sets the values of total_score and correct on the beginning of the quiz at 0
        session['total_score'] = 0
        session['correct_answer'] = 0

        statistics.add(current_user()['username'], lambda id_: DATABASE.add_quiz_started(id_, level))

        return render_template('quiz/startquiz.html', level=level, next_assignment=1)

    # Quiz mode
    # Fill in the filename as source
    @app.route('/quiz/quiz_questions/<int:level_source>/<int:question_nr>', methods=['GET'], defaults={'attempt': 1})
    @app.route('/quiz/quiz_questions/<int:level_source>/<int:question_nr>/<int:attempt>', methods=['GET'])
    def get_quiz(level_source, question_nr, attempt):

        if not is_quiz_enabled():
            return quiz_disabled_error()

            # If we don't have an attempt ID yet, redirect to the start page
        if not session.get('quiz-attempt-id'):
            return redirect(url_for('get_quiz_start', level=level_source, lang=g.lang))

            # Reading the yaml file
        questions = quiz_data_file_for(g.lang, level_source)
        if not questions:
            return no_quiz_data_error()

        question_status = 'start' if attempt == 1 else 'false'

        if question_nr > highest_question(questions):
            return redirect(url_for('quiz_finished', level=level_source, lang=g.lang))

        question = get_question(questions, question_nr)
        question_obj = question_options_for(question)

        # Read from session. Don't remove yet: If the user refreshes the
        # page here, we want to keep this same information in place (otherwise
        # if we removed from the session here it would be gone on page refresh).
        chosen_option = session.get('chosenOption', None)
        wrong_answer_hint = session.get('wrong_answer_hint', None)

        # Store the answer in the database. If we don't have a username,
        # use the session ID as a username.
        username = current_user()['username'] or f'anonymous:{utils.session_id()}'

        if attempt == 1:
            is_correct = is_correct_answer(question, chosen_option)
            # the answer is not yet answered so is_correct is None
            DATABASE.record_quiz_answer(session['quiz-attempt-id'],
                                        username=username,
                                        level=level_source,
                                        is_correct=is_correct,
                                        question_number=question_nr,
                                        answer=None)

        quiz_answers = DATABASE.get_quiz_answer(username, level_source, session['quiz-attempt-id'])

        return render_template('quiz/quiz_question.html',
                               level_source=level_source,
                               quiz_answers=quiz_answers,
                               questionStatus=question_status,
                               questions=questions,
                               question_options=question_obj,
                               chosen_option=chosen_option,
                               wrong_answer_hint=wrong_answer_hint,
                               question=question,
                               question_nr=question_nr,
                               correct=session.get('correct_answer'),
                               attempt=attempt,
                               is_last_attempt=attempt == MAX_ATTEMPTS,
                               lang=g.lang,
                               cross=icons['cross'],
                               check=icons['check'],
                               triangle=icons['triangle'],
                               diamond=icons['diamond'],
                               square=icons['square'],
                               circle=icons['circle'],
                               pentagram=icons['pentagram'],
                               triangle_6=icons['triangle_6'])

    @app.route('/quiz/finished/<int:level>', methods=['GET'])
    def quiz_finished(level):
        """Results page at the end of the quiz."""
        if not is_quiz_enabled():
            return quiz_disabled_error()

        # Reading the yaml file
        questions = quiz_data_file_for(g.lang, level)
        if not questions:
            return no_quiz_data_error()

        achievement = None
        total_score = round(session.get('total_score', 0) / max_score(questions) * 100)
        username = current_user()['username']
        if username:
            statistics.add(username, lambda id_: DATABASE.add_quiz_finished(id_, level, total_score))

            achievement = ACHIEVEMENTS.add_single_achievement(username, "next_question")
            if total_score == 100:
                if achievement:
                    achievement.append(ACHIEVEMENTS.add_single_achievement(username, "quiz_master")[0])
                else:
                    achievement = ACHIEVEMENTS.add_single_achievement(username, "quiz_master")
            if achievement:
                achievement = json.dumps(achievement)

        # Reading the yaml file
        questions = quiz_data_file_for(g.lang, level)
        if not questions:
            return no_quiz_data_error()

        # use the session ID as a username.
        username = current_user()['username'] or f'anonymous:{utils.session_id()}'

        quiz_answers = DATABASE.get_quiz_answer(username, level, session['quiz-attempt-id'])

        # get a datastructure for the result overview
        result_items = get_result_items(quiz_answers, questions)
        return render_template('quiz/quiz-result-overview.html',
                               correct=session.get('correct_answer', 0),
                               total_score=total_score,
                               level_source=level,
                               achievement=achievement,
                               quiz_answers=quiz_answers,
                               questions=questions,
                               result_items=result_items,
                               level=int(level) + 1,
                               next_assignment=1,
                               cross=icons['cross'],
                               check=icons['check'],
                               triangle=icons['triangle'],
                               diamond=icons['diamond'],
                               square=icons['square'],
                               circle=icons['circle'],
                               pentagram=icons['pentagram'],
                               triangle_6=icons['triangle_6'],
                               lang=g.lang)

    @app.route('/quiz/submit_answer/<int:level_source>/<int:question_nr>/<int:attempt>', methods=["POST"])
    def submit_answer(level_source, question_nr, attempt):
        if not is_quiz_enabled():
            return quiz_disabled_error()

        # If we don't have an attempt ID yet, redirect to the start page
        if not session.get('quiz-attempt-id'):
            return redirect(url_for('get_quiz_start', level=level_source, lang=g.lang))

        # Get the chosen option from the request form with radio buttons
        # This looks like '1-B' or '5-C' or what have you.
        #
        # The number should always be the same as 'question_nr', or otherwise
        # be 'question_nr - 1', so is unnecessary. But we'll leave it here for now.
        if request.method == "POST":
            # The value is a character and not a text
            chosen_option = request.form.get("submit-button")

            # Reading the yaml file
            questions = quiz_data_file_for(g.lang, level_source)
            if not questions:
                return no_quiz_data_error()

            # Convert question_nr to an integer
            q_nr = int(question_nr)

            # Convert the corresponding chosen option to the index of an option
            question = get_question(questions, q_nr)

            is_correct = is_correct_answer(question, chosen_option)

            session['chosenOption'] = chosen_option
            if not is_correct:
                session['wrong_answer_hint'] = get_hint(question, chosen_option)
            else:
                # Correct answer -- make sure there is no hint on the next display page
                session.pop('wrong_answer_hint', None)

            # Store the answer in the database. If we don't have a username,
            # use the session ID as a username.
            username = current_user()['username'] or f'anonymous:{utils.session_id()}'

            DATABASE.record_quiz_answer(session['quiz-attempt-id'],
                                        username=username,
                                        level=level_source,
                                        is_correct=is_correct,
                                        question_number=question_nr,
                                        answer=chosen_option)

            if is_correct:
                score = int(correct_answer_score(question))
                session['total_score'] = session.get('total_score', 0) + score
                session['correct_answer'] = session.get('correct_answer', 0) + 1

                quiz_answers = DATABASE.get_quiz_answer(username, level_source, session['quiz-attempt-id'])
                return redirect(url_for('quiz_feedback', quiz_answers=quiz_answers, level_source=level_source,
                                        question_nr=question_nr, lang=g.lang))

            # Not a correct answer. You can try again if you haven't hit your max attempts yet.
            if attempt >= MAX_ATTEMPTS:
                quiz_answers = DATABASE.get_quiz_answer(username, level_source, session['quiz-attempt-id'])
                return redirect(url_for('quiz_feedback', quiz_answers=quiz_answers, level_source=level_source,
                                        question_nr=question_nr, lang=g.lang, ))

        # Redirect to the display page to try again
        return redirect(
            url_for('get_quiz', chosen_option=chosen_option, level_source=level_source, question_nr=question_nr,
                    attempt=attempt + 1, lang=g.lang))

    @app.route('/quiz/feedback/<int:level_source>/<int:question_nr>', methods=["GET"])
    def quiz_feedback(level_source, question_nr):
        if not is_quiz_enabled():
            return quiz_disabled_error()

        # If we don't have an attempt ID yet, redirect to the start page
        if not session.get('quiz-attempt-id'):
            return redirect(url_for('get_quiz_start', level=level_source, lang=g.lang))

        # Reading the yaml file
        questions = quiz_data_file_for(g.lang, level_source)
        if not questions:
            return no_quiz_data_error()

        question = get_question(questions, question_nr)

        # Read from session and remove the variables from it (this is the
        # feedback page, the previous answers will never apply anymore).
        chosen_option = session.pop('chosenOption', None)
        wrong_answer_hint = session.pop('wrong_answer_hint', None)

        answer_was_correct = is_correct_answer(question, chosen_option)

        index_option = index_from_letter(chosen_option)
        correct_option = get_correct_answer(question)

        question_options = question_options_for(question)

        # use the session ID as a username.
        username = current_user()['username'] or f'anonymous:{utils.session_id()}'

        quiz_answers = DATABASE.get_quiz_answer(username, level_source, session['quiz-attempt-id'])

        return render_template('quiz/feedback.html',
                               quiz_answers=quiz_answers,
                               question=question,
                               questions=questions,
                               question_options=question_options,
                               level_source=level_source,
                               question_nr=question_nr,
                               correct=session.get('correct_answer'),
                               answer_was_correct=answer_was_correct,
                               wrong_answer_hint=wrong_answer_hint,
                               index_option=index_option,
                               correct_option=correct_option,
                               cross=icons['cross'],
                               check=icons['check'],
                               lang=g.lang)


def get_result_items(quiz_answers, questions):
    result_items = []
    for i in range(len(questions)):
        item = {}
        item["question_text"] = questions[i + 1]["question_text"]
        item["question_code"] = questions[i + 1]["code"]
        item["is_correct"] = quiz_answers[i + 1][-1] == questions[i + 1]["correct_answer"]
        item["index_chosen"] = index_from_letter(quiz_answers[i + 1][-1])
        item["index_correct"] = index_from_letter(questions[i + 1]["correct_answer"])
        item["attempts"] = len(quiz_answers[i + 1])
        if "option_text" in question_options_for(questions[i + 1])[
            index_from_letter(questions[i + 1]["correct_answer"])]:
            item["option_text"] = \
            question_options_for(questions[i + 1])[index_from_letter(questions[i + 1]["correct_answer"])]["option_text"]
        elif "code" in question_options_for(questions[i + 1])[index_from_letter(questions[i + 1]["correct_answer"])]:
            item["code"] = \
            question_options_for(questions[i + 1])[index_from_letter(questions[i + 1]["correct_answer"])]["code"]
        result_items.append(item)
    return result_items


def is_quiz_enabled():
    return config.get('quiz-enabled')


def quiz_disabled_error():
    # Todo TB -> Somewhere in the near future we should localize these messages
    return utils.error_page(error=404, page_error='Hedy quiz disabled!', menu=False, iframe=True)


def no_quiz_data_error():
    # Todo TB -> Somewhere in the near future we should localize these messages
    return utils.error_page(error=404, page_error='No quiz data found for this level', menu=False, iframe=True)


def quiz_data_file_for(lang, level):
    # Todo TB -> We should cache this as well!
    quiz_file = YamlFile.for_file(f'content/quizzes/{lang}.yaml')
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
        max_score = max_score + int(question_value['question_score'])
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

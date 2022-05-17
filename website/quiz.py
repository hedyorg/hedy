import json
import uuid

from flask_babel import gettext

from config import config
from website import statistics
from website.auth import current_user
import utils
from flask import request, g, session, redirect, url_for, jsonify
from flask_helpers import render_template

MAX_ATTEMPTS = 3

def routes(app, database, achievements, quizzes):
    global DATABASE
    global ACHIEVEMENTS
    global QUIZZES

    DATABASE = database
    ACHIEVEMENTS = achievements
    QUIZZES = quizzes

    @app.route('/quiz/initialize_user', methods=['POST'])
    def initialize_user():
        body = request.json
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('level'), int):
            return gettext('level_invalid'), 400

        session['quiz-attempt-id'] = uuid.uuid4().hex
        session['total_score'] = 0
        session['correct_answer'] = 0
        session['correctly_answered_questions_numbers'] = []

        statistics.add(current_user()['username'], lambda id_: DATABASE.add_quiz_started(id_, level))

        return jsonify({}), 200

    @app.route('/quiz/get-question/<int:level>/<int:question>', methods=['GET'])
    def get_quiz_question(level, question):
        if question > QUIZZES[g.lang].get_highest_question_level(level) or question < 1:
            return gettext('question_doesnt_exist'), 400

        question = QUIZZES[g.lang].get_quiz_data_for_level_question(level, question, g.keyword_lang)
        return jsonify({question}), 200

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

        if question_nr > QUIZZES[g.lang].get_highest_question_level(level_source):
            return redirect(url_for('quiz_finished', level=level_source, lang=g.lang))

        questions = QUIZZES[g.lang].get_quiz_data_for_level(level_source, g.keyword_lang)
        question = QUIZZES[g.lang].get_quiz_data_for_level_question(level_source, question_nr, g.keyword_lang)

        if not questions:
            return no_quiz_data_error()

        question_status = 'start' if attempt == 1 else 'false'

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

        # Todo TB -> We have to do some magic here to format() the keywords into the quiz

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
                               lang=g.lang)

    @app.route('/quiz/finished/<int:level>', methods=['GET'])
    def quiz_finished(level):
        """Results page at the end of the quiz."""
        if not is_quiz_enabled():
            return quiz_disabled_error()

        questions = QUIZZES[g.lang].get_quiz_data_for_level(level, g.keyword_lang)

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
        questions = QUIZZES[g.lang].get_quiz_data_for_level(level, g.keyword_lang)
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
                               next_assignment=1)

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

            questions = QUIZZES[g.lang] .get_quiz_data_for_level(level_source, g.keyword_lang)
            question = QUIZZES[g.lang] .get_quiz_data_for_level_question(level_source, question_nr, g.keyword_lang)

            if not questions:
                return no_quiz_data_error()

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
                correct_question_nrs = get_correctly_answered_question_nrs()
                if question_nr not in correct_question_nrs:
                    session['total_score'] = session.get('total_score', 0) + score
                    session['correct_answer'] = session.get('correct_answer', 0) + 1
                    session['correctly_answered_questions_numbers'].append(question_nr)

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

        questions = QUIZZES[g.lang].get_quiz_data_for_level(level_source, g.keyword_lang)
        question = QUIZZES[g.lang].get_quiz_data_for_level_question(level_source, question_nr, g.keyword_lang)

        if not questions:
            return no_quiz_data_error()

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
                               lang=g.lang)


def get_result_items(quiz_answers, questions):
    return [{
        'question_text': q.get('question_text'),
        'question_code': q.get('code'),
        'is_correct': quiz_answers[k][-1] == q.get("correct_answer"),
        'index_chosen': index_from_letter(quiz_answers[k][-1]),
        'index_correct': index_from_letter(q.get("correct_answer")),
        'attempts': len([a for a in quiz_answers[k] if a is not None]),
        'option': question_options_for(q)[index_from_letter(q["correct_answer"])]["option"]
    } for k, q in questions.items()]


def is_quiz_enabled():
    return config.get('quiz-enabled')


def quiz_disabled_error():
    # Todo TB -> Somewhere in the near future we should localize these messages
    return utils.error_page(error=404, page_error='Hedy quiz disabled!', menu=False, iframe=True)


def no_quiz_data_error():
    # Todo TB -> Somewhere in the near future we should localize these messages
    return utils.error_page(error=404, page_error='No quiz data found for this level', menu=False, iframe=True)

def is_correct_answer(question, letter):
    return question['correct_answer'] == letter


def get_correct_answer(question):
    """Return the correct answer option from a question."""
    i = index_from_letter(question['correct_answer'])
    return question['mp_choice_options'][i]


def get_hint(question, letter):
    i = index_from_letter(letter)
    return question['mp_choice_options'][i].get('feedback')


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


def get_correctly_answered_question_nrs():
    if 'correctly_answered_questions_numbers' not in session:
        session['correctly_answered_questions_numbers'] = list()
    return session['correctly_answered_questions_numbers']


def escape_newlines(x):
    return x.replace("\n", '\\n')


def index_from_letter(letter):
    """Turn A -> 0, B -> 1 etc."""
    return ord(letter) - ord('A')


def letter_from_index(ix):
    """Turn 0 -> A, 1 -> B, etc."""
    return chr(ord('A') + ix)

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

ANSWER_PARSER = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F'
}


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

        statistics.add(current_user()['username'], lambda id_: DATABASE.add_quiz_started(id_, body.get('level')))

        return jsonify({}), 200

    @app.route('/quiz/get-question/<int:level>/<int:question>', methods=['GET'])
    def get_quiz_question(level, question):
        if question > QUIZZES[g.lang].get_highest_question_level(level) or question < 1:
            return gettext('question_doesnt_exist'), 400

        question = QUIZZES[g.lang].get_quiz_data_for_level_question(level, question, g.keyword_lang)
        return jsonify(question), 200

    @app.route('/quiz/submit_answer/', methods=["POST"])
    def submit_answer():
        body = request.json
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('level'), str):
            return gettext('level_invalid'), 400
        if not isinstance(body.get('question'), str):
            return gettext('question_invalid'), 400
        if not isinstance(body.get('answer'), int):
            return gettext('answer_invalid'), 400

        level = int(body['level'])
        question_number = int(body['question'])

        question = QUIZZES[g.lang].get_quiz_data_for_level_question(level, question_number, g.keyword_lang)
        is_correct = True if question['correct_answer'] == ANSWER_PARSER.get(body.get('answer')) else False

        username = current_user()['username'] or f'anonymous:{utils.session_id()}'
        DATABASE.record_quiz_answer(session['quiz-attempt-id'], username=username, level=level,
                                    is_correct=is_correct, question_number=question_number,
                                    answer=body.get('answer'))

        if is_correct:
            score = int(correct_answer_score(question))
            correct_question_nrs = get_correctly_answered_question_nrs()
            if body.get('question') not in correct_question_nrs:
                session['total_score'] = session.get('total_score', 0) + score
                session['correct_answer'] = session.get('correct_answer', 0) + 1
                session['correctly_answered_questions_numbers'].append(body.get('question'))

            # We have to get the relevant data for the correct answer
            question_text = question.get("question_text")
            correct_answer_text = question.get("mp_choice_options")[body.get('answer') - 1].get('option')
            feedback = question.get("mp_choice_options")[body.get('answer') - 1].get('feedback')
            next_question = True if question_number < QUIZZES[g.lang].get_highest_question_level(level) else False

            return jsonify({'correct': True, 'question_text': question_text, 'level': level,
                            'correct_answer_text': correct_answer_text, 'feedback': feedback,
                            'max_question': question_number < QUIZZES[g.lang].get_highest_question_level(level),
                            'next_question': next_question}), 200

        return jsonify({'correct': False}), 200


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

        answer_was_correct = True if question['correct_answer'] == ANSWER_PARSER.get(chosen_option) else False

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

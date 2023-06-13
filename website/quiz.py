import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from werkzeug.routing import RequestRedirect

from flask import abort, g, render_template, request, session, redirect, url_for

import utils
from hedy import HEDY_MAX_LEVEL
from hedy_content import Quizzes
from website import statistics
from website.auth import current_user

from .achievements import Achievements
from .database import Database
from .website_module import WebsiteModule, route

MAX_ATTEMPTS = 2
NO_SUCH_QUESTION = 'No such question'


class QuizLogic:
    """Business logic for quiz-related things."""

    def __init__(self, db: Database):
        self.db = db

    def quiz_threshold_for_user(self):
        """Return the minimum quiz percentage the given user has to achieve to pass the quiz."""
        customizations = self.db.get_student_class_customizations(current_user()['username'])
        return customizations.get('level_thresholds', {}).get('quiz', 0)


class QuizModule(WebsiteModule):
    def __init__(self, db: Database, achievements: Achievements, quizzes: Dict[str, Quizzes]):
        super().__init__("quiz", __name__, url_prefix="/quiz")
        self.logic = QuizLogic(db)
        self.db = db
        self.achievements = achievements
        self.quizzes = quizzes

    @route("/begin/<int:level>", methods=["GET", "POST"])
    def begin(self, level):
        """Begin the quiz at a particular level.

        Initialize a new attempt, then redirect to the form that presents question 1.
        """
        self.initialize_attempt(level)
        statistics.add(current_user()["username"], lambda id_: self.db.add_quiz_started(id_, level))
        return redirect(url_for('.current_question'))

    @route("/current_question", methods=["GET"])
    def current_question(self):
        """Show the current question.

        The current question is taken from the user session.
        """
        progress, question = self.current_progress_and_question()

        return render_template('quiz/partial-question.html',
                               level=progress.level,
                               question_count=self.question_count(progress.level),
                               correct_answers_so_far=progress.correct_answers_so_far,
                               incorrect_answers_so_far=progress.incorrect_answers_so_far,
                               progress=progress,
                               question=question)

    @route("/preview-question/<int:level>/<int:question>", methods=["GET"])
    def preview_question(self, level, question):
        """Show a specific question, without requiring that the user is currently doing a quiz attempt."""

        # Make sure that we have progress, mark it as developer mode progress
        progress = self.current_progress()
        if not progress:
            progress = self.initialize_attempt(level)
        progress.level = level
        progress.question = question
        progress.is_preview = True
        self.save_progress(progress)

        return self.current_question()

    @route("/submit_answer", methods=["POST"])
    def submit_answer(self):
        """Hit when an answer is submitted."""
        progress, question = self.current_progress_and_question()
        question_count = self.question_count(progress.level)

        answer = int(request.form.get('answer', '0'))
        if not answer:
            return 'No answer given or not an int', 400

        if progress.question_attempt >= MAX_ATTEMPTS:
            return redirect(url_for('.review_question'))

        is_correct = question.correct_answer == answer

        # Record attempt to database for future analysis (but only if this is not a preview session)
        save_to_db = not progress.is_preview
        if save_to_db:
            username = current_user()["username"] or f"anonymous:{utils.session_id()}"
            self.db.record_quiz_answer(
                progress.attempt_id,
                username=username,
                level=progress.level,
                is_correct=is_correct,
                question_number=progress.question,
                answer=letter_from_number(answer),
            )

        if is_correct:
            progress.correctly_answered(question)
        else:
            progress.incorrectly_answered(question.get_choice(answer))
        progress.advance_cypress_page_counter()

        question_finished = is_correct or progress.question_attempt >= MAX_ATTEMPTS
        if question_finished and progress.question == question_count:
            self.on_quiz_finished(progress)

        self.save_progress(progress)
        return redirect(url_for('.review_question' if question_finished else '.current_question'))

    @route("/review_question", methods=["GET"])
    def review_question(self):
        """Review the correct answer of the previous question."""
        progress, question = self.current_progress_and_question()

        is_correct = progress.last_wrong_answer is None
        question_count = self.question_count(progress.level)
        correct_answer = question.get_choice(question.correct_answer)
        incorrect_answer = question.get_choice(progress.last_wrong_answer) if progress.last_wrong_answer else None

        next_question = progress.question + 1 if progress.question + 1 <= question_count else None

        return render_template('quiz/partial-review-question.html',
                               progress=progress,
                               question=question,
                               question_count=question_count,
                               correct_answers_so_far=progress.correct_answers_so_far,
                               incorrect_answers_so_far=progress.incorrect_answers_so_far,
                               correct_answer=correct_answer,
                               incorrect_answer=incorrect_answer,
                               next_question=next_question,
                               is_correct=is_correct)

    @route("/next_question", methods=["POST"])
    def next_question(self):
        """Advance the progress object and redirect to the next question."""
        progress, _ = self.current_progress_and_question()
        progress.advance_cypress_page_counter()
        progress.next_question()
        self.save_progress(progress)

        if progress.question <= self.question_count(progress.level):
            return redirect(url_for('.current_question'))
        else:
            return redirect(url_for('.review_quiz'))

    @route("/review_quiz", methods=["GET"])
    def review_quiz(self):
        """Review the results of the quiz."""
        progress = self.current_progress()
        if not progress:
            return redirect(url_for('.begin', level=1))
        questions = self.get_all_questions(progress.level)
        total_achievable = sum(q.score for q in questions)

        score_percent = round(progress.total_score / total_achievable * 100)

        # Certificates are only for logged-in users
        get_certificate = current_user()['username'] and progress.level == HEDY_MAX_LEVEL
        next_level = progress.level + 1 if progress.level < HEDY_MAX_LEVEL else None
        retake_quiz_level = None

        # If you are in a class and the teacher has set quiz completion requirements, we check
        # them here and hide the "next level" button if you haven't met them.
        if current_user()['username']:
            threshold = self.logic.quiz_threshold_for_user()
            if score_percent < threshold:
                # No next level for you
                next_level = None
                get_certificate = None
                retake_quiz_level = progress.level

        return render_template('quiz/partial-review-quiz.html',
                               next_level=next_level,
                               progress=progress,
                               retake_quiz_level=retake_quiz_level,
                               get_certificate=get_certificate,
                               score_percent=score_percent)

    def on_quiz_finished(self, progress):
        """Called when the student has answered the last question in the quiz.

        Record statistics achievements.
        """
        if progress.is_preview:
            return

        questions = self.get_all_questions(progress.level)
        total_achievable = sum(q.score for q in questions)

        achievement = None
        username = current_user()["username"]
        if username:
            statistics.add(username, lambda id_: self.db.add_quiz_finished(id_, progress.level, progress.total_score))
            # FIXME: I'm pretty sure the types of this code don't work out in case there is more
            # than once achievement at a time, but I don't quite understand well enough how it's
            # supposed to work to fix it.
            achievement = self.achievements.add_single_achievement(username, "next_question")
            if progress.total_score == total_achievable:
                if achievement:
                    achievement.append(self.achievements.add_single_achievement(username, "quiz_master")[0])
                else:
                    achievement = self.achievements.add_single_achievement(username, "quiz_master")
            if progress.level == HEDY_MAX_LEVEL:
                if achievement:
                    achievement.append(self.achievements.add_single_achievement(username, "hedy_certificate")[0])
                else:
                    achievement = self.achievements.add_single_achievement(username, "hedy_certificate")

        # Add any achievements we accumulated to the session. They will be sent to the
        # client at the next possible opportunity.
        if achievement:
            session['pending_achievements'] = session.get('pending_achievements', []) + achievement

    def initialize_attempt(self, level):
        """Record that we're starting a new attempt."""
        return self.save_progress(QuizProgress(
            attempt_id=uuid.uuid4().hex,
            level=level,
            question=1,
            question_attempt=0,
            total_score=0,
        ))

    def save_progress(self, progress):
        session['quiz_progress'] = asdict(progress)
        return progress

    def current_progress(self):
        """Return the current QuizProgress object."""
        p = session.get('quiz_progress')
        try:
            return QuizProgress(**p) if p else None
        except Exception:
            # Deserializing failed for some reason
            return None

    def my_quiz(self):
        """Return the quiz for the current language."""
        return self.quizzes[g.lang]

    def question_count(self, level):
        return self.my_quiz().get_highest_question_level(level)

    def get_all_questions(self, level):
        """Return all questions for the given level."""
        qs = self.my_quiz().get_quiz_data_for_level(level, request.args.get('keyword_lang_override', g.keyword_lang))
        return [Question.from_yaml(int(n), q) for n, q in qs.items()]

    def get_question(self, level, question: int) -> 'Question':
        """Return the indicated question. The question will be returned as ViewModelQuestion object.

        The current session's keyword language is used, and an override is possible if
        requested.
        """
        q = self.my_quiz().get_quiz_data_for_level_question(
            level, question, request.args.get('keyword_lang_override', g.keyword_lang))
        return Question.from_yaml(question, q) if q else None

    def current_progress_and_question(self):
        """Return the current progress and question objects."""
        progress = self.current_progress()
        if not progress:
            raise RequestRedirect(url_for('.begin', level=1))

        question = self.get_question(progress.level, progress.question)
        if not question:
            # We shouldn't have gotten here
            return abort(400, NO_SUCH_QUESTION)
        return progress, question


@dataclass
class Choice:
    number: int
    text: str
    feedback: str
    code: Optional[str] = None


@dataclass
class Question:
    """View Model Question.

    A question as it is seen by the templates (not necessarily as it is stored on disk).
    """
    number: int
    text: str
    choices: List[Choice]
    correct_answer: int
    hint: str
    score: int
    code: Optional[str] = None
    output: Optional[str] = None

    def get_choice(self, number: int):
        """Return the Choice object for a base-1 choice number."""
        return self.choices[number - 1]

    @staticmethod
    def from_yaml(nr, data):
        """Build a ViewModelQuestion from what's written in the YAML."""
        return Question(
            number=nr,
            text=data.get('question_text', ''),
            code=data.get('code'),
            choices=[Choice(number=i + 1, text=opt.get('option', ''), feedback=opt.get('feedback', ''))
                     for i, opt in enumerate(data.get('mp_choice_options', []))],
            # Correct_answer is 'A', 'B', 'C' in the file, but needs to be 1, 2, 3 because that's
            # what the data has.
            correct_answer=number_from_letter(data.get('correct_answer', 'A')),
            hint=data.get('hint', ''),
            score=int(data.get('question_score', 10)),
            output=data.get('output'),
        )


@dataclass
class QuizProgress:
    """Progress through the quiz."""
    level: int
    question: int
    attempt_id: str  # Identifier of the entire quiz
    question_attempt: int  # How often we tried to answer the current question
    total_score: int
    correctly_answered_questions_numbers: List[int] = field(default_factory=list)
    last_wrong_answer: Optional[int] = None
    wrong_answer_feedback: Optional[str] = None
    is_preview: Optional[bool] = None

    # We have this solely so that we can make a cypress click-through test that is reliable
    # without 'cy.wait()'s everywhere.
    cypress_page_counter: List[int] = field(default=0)

    def correctly_answered(self, question: Question):
        """Update the progress' state in response to a correct answer."""
        if question.number not in self.correctly_answered_questions_numbers:
            self.total_score += question.score
            self.correctly_answered_questions_numbers.append(question.number)
        self.last_wrong_answer = None
        self.wrong_answer_feedback = None

    def incorrectly_answered(self, choice: Choice):
        """Update the progress' state in response to an incorrect choice."""
        self.question_attempt += 1
        self.last_wrong_answer = choice.number
        self.wrong_answer_feedback = choice.feedback

    def next_question(self):
        """Move to the next question."""
        self.question += 1
        self.question_attempt = 0
        self.last_wrong_answer = None
        self.wrong_answer_feedback = None

    def advance_cypress_page_counter(self):
        self.cypress_page_counter += 1

    @property
    def correct_answers_so_far(self):
        return set(self.correctly_answered_questions_numbers)

    @property
    def incorrect_answers_so_far(self):
        return set(i + 1 for i in range(self.question) if i + 1 not in self.correctly_answered_questions_numbers)


def number_from_letter(letter):
    """Turn A, B, C into 1, 2, 3."""
    return ord(letter.upper()) - ord('A') + 1


def letter_from_number(num):
    """Turn 1, 2, 3 into A, B, C."""
    return chr(ord('A') + num - 1)

import {modal} from "./modal";

(function() {
    $('.option-block').on("click", function () {
        $('.option-block').removeClass('active');
        $(this).addClass('active');
    });
})();


export function startQuiz(level: number) {
    $('#start_quiz_container').hide();
    $.ajax({
      type: 'POST',
      url: '/quiz/initialize_user',
      data: JSON.stringify({
        level: level
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function() {
        loadQuestQuestion(level, 1);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

export function loadQuestQuestion(level: number, question: number) {
    // If we get the request from the feedback page -> hide just to be sure also remove selected answer
    $('#quiz_feedback_container').hide();
    $('.option-block').removeClass('active');

    $.ajax({
      type: 'GET',
      url: '/quiz/get-question/' + level + '/' + question,
      dataType: 'json'
    }).done(function(response: any) {
        $('#quiz_container').show();
        showQuestion(response.question_text);
        if (response.code) {
            showQuestionCode(response.code);
        }
        showAnswers(response.mp_choice_options, level, question);
        highlightQuestionBar(question);
        loadHint(response.hint);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showQuestion(question: string) {
    $('#quiz_question_title').text(question);
    $('#quiz_question_container').show();
}

function showQuestionCode(code: string) {
    $('#quiz_question_code_container').show();
    let editor = ace.edit("quiz_question_code");
    editor.setValue(code);
}

function showAnswers(options: any, level: number, question: number) {
    for (let i = 1; i < options.length+1; ++i) {
        $('#answer_container_' + i).show();
        $('#answer_text_' + i).text(options[i-1].option);
        $('#answer_text_' + i).attr('level', level);
        $('#answer_text_' + i).attr('question', question);
        $('#answer_text_' + i).show();
        // Todo -> If we have a code answer, show answer_code_i and remove backticks
    }
    $('#quiz_answers_container').show();
}

function highlightQuestionBar(question: number) {
    $('.step').removeClass('current');
    $('.question_header_text_container').hide();
    $('#question_header_text_' + question).show();
    $('#question_header_' + question).addClass('current');
}

function loadHint(hint: string) {
    $('#quiz_question_hint').text(hint);
    $('#quiz_question_hint').hide();
}

export function answerQuestion(answer_number: number) {
    let element = $('#answer_text_' + answer_number);
    let level = element.attr('level');
    let question = element.attr('question');

    $.ajax({
      type: 'POST',
      url: '/quiz/submit_answer/',
      data: JSON.stringify({
        level: level,
        question: question,
        answer: answer_number
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response: any) {
        if (response.correct) {
            showFeedback(response, question || "", true);
            updateHeader(question || "", true);
        } else {
            showFeedback(response, question || "", false);
            updateHeader(question || "", false);
        }
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showFeedback(response: any, question: string, correct: boolean) {
    console.log(response);
    $('#quiz_question_container').hide();
    $('#quiz_answers_container').hide();

    $('#question_number_container').text(question);
    $('#question_length_container').text(response.max_question);

    if (response.next_question) {
        $('#next_question_number_container').text(parseInt(question) + 1);
        $('#next_question_button').attr('onclick', "hedyApp.loadQuestQuestion(" + response.level + "," + (parseInt(question) + 1) + ");");
        $('#next_question_button').show();
    } else {
        $('#results_button').show();
    }

    $('#question_feedback_text_container').text(response.question_text);
    $('#feedback_feedback_text').text(response.feedback);
    $('#feedback_correct_answer_container').text(response.correct_answer_text);

    if (correct) {
        $('#feedback_incorrect_container').hide();
        $('#feedback_correct_container').show();
    } else {
        $('#feedback_correct_container').hide();
        $('#feedback_incorrect_container').show();
    }
    $('#quiz_feedback_container').show();
}

function updateHeader(question: string, correct: boolean) {
    if (correct) {
        $('#question_header_' + question).addClass('check');
    } else {
        $('#question_header_' + question).addClass('incorrect');
    }
}

export function loadQuizResults() {
    console.log("Laad de resultaten...");
}

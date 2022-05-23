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
        loadHint(response.hint);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showQuestion(question: string) {
    $('#quiz_question_title').text(question);
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
}

function loadHint(hint: string) {
    $('#quiz_question_hint').text(hint);
    $('#quiz_question_hint').hide();
}

export function answerQuestion(answer_number: number) {
    let element = $('#answer_text_' + answer_number);
    $.ajax({
      type: 'POST',
      url: '/quiz/submit_answer/',
      data: JSON.stringify({
        level: element.attr('level'),
        question: element.attr('question'),
        answer: answer_number
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response: any) {
        if (response.correct) {
            updateQuestionBar();
            showFeedback(response.question);
        } else if (response.incorrect) {
            // Show feedback as well -> with "fault" marker
        }
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function updateQuestionBar() {
    console.log("Dit moeten we nog fixen...");
}

function showFeedback(question: any) {
    console.log(question)
    console.log("Antwoord is goed....");
}

export function loadQuizResults() {
    console.log("Laad de resultaten...");
}

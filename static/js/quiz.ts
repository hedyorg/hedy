import {modal} from "./modal";

(function() {
    $('.option-block').on("click", function () {
        $('.option-block').removeClass('active');
        $(this).addClass('active');
    });
})();


export function startQuiz(level: number) {
    $('#start_quiz_container').hide();
    loadQuestQuestion(level, 1);
}

export function loadQuestQuestion(level: number, question: number) {
    $.ajax({
      type: 'GET',
      url: '/quiz/get-question/' + level + '/' + question,
      dataType: 'json'
    }).done(function(response: any) {
        $('#quiz_container').show();
        console.log(response);
        showQuestion(response.question.question_text);
        if (response.question.code) {
            showQuestionCode(response.question.code);
        }
        showAnswers(response.question.mp_choice_options);
        loadHint(response.question.hint);
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

function showAnswers(options: any) {
    for (let i = 1; i < options.length+1; ++i) {
        $('#answer_container_' + i).show();
        $('#answer_text_' + i).text(options[i-1].option);
        $('#answer_text_' + i).show();
        // Todo -> If we have a code answer, show answer_code_i and remove backticks
    }
}

function loadHint(hint: string) {
    $('#quiz_question_hint').text(hint);
    $('#quiz_question_hint').hide();
}

export function answerQuestion(answer: number) {
    console.log(answer);
}

import {modal} from "./modal";

(function() {

})();


export function startQuiz(level: number) {
    $('#start_quiz_container').hide();
    loadQuestQuestion(level, 1);
}

export function loadQuestQuestion(level: number, question: number) {
    $.ajax({
      type: 'GET',
      url: '/quiz/get-question/' + level + '/' + 2,
      dataType: 'json'
    }).done(function(response: any) {
        $('#quiz_container').show();
        console.log(response);
        showQuestion(response.question.question_text);
        if (response.question.code) {
            console.log("Er is een code!");
            showQuestionCode(response.question.code);
        }
        showAnswers(response.question.mp_choice_options);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showQuestion(question: string) {
    $('#quiz_question_title').text(question);
}

function showQuestionCode(code: string) {
    $('#quiz_question_container').show();
    let editor = ace.edit("quiz_question_code");
    editor.setValue(code);
}

function showAnswers(options: any) {
    console.log(options);
}

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
      url: '/quiz/get-question/' + level + '/' + question,
      dataType: 'json'
    }).done(function(response: any) {
        console.log(response);
        $('#quiz_container').show();
        showQuestion();
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showQuestion() {
    console.log("todo...");
}

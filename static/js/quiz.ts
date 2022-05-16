import {modal} from "./modal";

(function() {

})();


export function loadQuestQuestion(level: number, question: number) {
    $.ajax({
      type: 'GET',
      url: '/quiz/get-question/' + level + '/' + question,
      dataType: 'json'
    }).done(function(response: any) {
        console.log(response);
        // We get the question info back -> show question
        showQuestion();
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showQuestion() {
    console.log("todo...");
}

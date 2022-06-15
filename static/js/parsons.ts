import {modal} from "./modal";

(function() {
        // We might not need this -> is there something we want to load on page load?
    }
)();

export function startParsons(level: number) {
    $('#start_parsons_container').hide();
    loadParsonsExercise(level, 1);
}

export function loadParsonsExercise(level: number, question: number) {
    $.ajax({
      type: 'GET',
      url: '/parsons/get-question/' + level + '/' + question,
      dataType: 'json'
    }).done(function(response: any) {
        $('#parsons_container').show();
        showExercise(response);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showExercise(response: any) {
    console.log("Let's show the exercise...");
    console.log(response);
}
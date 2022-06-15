import {modal} from "./modal";

(function() {
        // We might not need this -> is there something we want to load on page load?
    }
)();

export function startParsons(level: number) {
    $('#start_parsons_container').hide();
    loadParsonsExercise(level, 1);
}

export function loadParsonsExercise(level: number, exercise: number) {
    $.ajax({
      type: 'GET',
      url: '/parsons/get-exercise/' + level + '/' + exercise,
      dataType: 'json'
    }).done(function(response: any) {
        $('#parsons_container').show();
        showExercise(response);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showExercise(response: any) {
    console.log("We have decided to shuffle items on the front-end...");
    let code_lines = response.code_lines.sort( () => Math.random() - 0.5);
    console.log(response);
    console.log(code_lines);
}
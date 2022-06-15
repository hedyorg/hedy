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
    let code_lines = shuffle_code_lines(response.code_lines);
    let counter = 0;
    // Hide all containers, show the onces relevant dynamically
    $('.parsons_start_line_container').hide();
    $('.parsons_goal_line_container').hide();

    $.each(code_lines, function(key: string, valueObj: string) {
        counter += 1;
        // Temp output to console to make sure TypeScript compiles
        console.log(key);
        ace.edit('start_parsons_' + counter).session.setValue(valueObj.replace(/\n+$/, ''), -1);
        $('#start_parsons_div_' + counter).attr('index', key);
        $('#start_parsons_div_' + counter).attr('code', valueObj);
        ace.edit('goal_parsons_' + counter).session.setValue("");

        $('#parsons_start_line_container_' + counter).show();
        $('#parsons_goal_line_container_' + counter).show();
    });
}

export function loadNextExercise() {
    // Todo...
}

// https://stackoverflow.com/questions/26503595/javascript-shuffling-object-properties-with-their-values
function shuffle_code_lines(code_lines: object) {
    let shuffled = {};
    let keys = Object.keys(code_lines);
    keys.sort(function() {return Math.random() - 0.5;});
    keys.forEach(function(k) {
        // @ts-ignore
        shuffled[k] = code_lines[k];
    });
    return shuffled;
}
import {modal} from "./modal";
import {stopit} from "./app";

interface ParsonsExercise {
    readonly story: number;
    readonly code_lines: Record<string, string>;
    readonly code: string;
}

(function() {
        // We might not need this -> is there something we want to load on page load?
    }
)();

export function loadParsonsExercise(level: number, exercise: number) {
    $('#next_parson_button').hide();

    // If we have a forced keyword language, sent this info to the back-end to get the correct exercise
    let parameters = new URLSearchParams(window.location.search)
    let url = "/parsons/get-exercise/" + level + '/' + exercise;
    if (parameters.has('keyword_language')) {
        url += "/" + parameters.get('keyword_language')
    }

    $.ajax({
      type: 'GET',
      url: url,
      dataType: 'json'
    }).done(function(response: ParsonsExercise) {
        $('#parsons_container').show();
        $('#next_parson_button').attr('current_exercise', exercise);
        resetView();
        updateHeader(exercise);
        showExercise(response);
        updateNextExerciseButton(level, exercise);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function resetView() {
    stopit();
    $('#output').empty();
    $('.parsons_goal_line_container').removeClass('border-green-500 border-red-500');
    $('.compiler-parsons-box').attr('index', '-');
    $('.compiler-parsons-box').attr('code', '');
    $( ".goal_parsons" ).each(function(  ) {
        ace.edit($(this).attr('id')).setValue('');
    });
}

function updateHeader(exercise: number) {
    $('.parsons_header_text_container').hide();
    $('.step').removeClass('current');

    $('#parsons_header_text_' + exercise).show();
    $('#parsons_header_' + exercise).addClass('current');
}

function showExercise(response: ParsonsExercise) {
    const code_lines = shuffle_code_lines(response.code);
    let counter = 0;
    // Hide all containers, show the onces relevant dynamically
    $('.parsons_start_line_container').hide();
    $('.parsons_goal_line_container').hide();

    for (const [key, valueObj] of Object.entries(code_lines)) {
        counter += 1;
        // Temp output to console to make sure TypeScript compiles
        ace.edit('start_parsons_' + counter).session.setValue(valueObj.replace(/\n+$/, ''), -1);
        $('#start_parsons_div_' + counter).attr('index', key);
        $('#start_parsons_div_' + counter).attr('code', valueObj);
        ace.edit('goal_parsons_' + counter).session.setValue("");

        $('#parsons_start_line_container_' + counter).show();
        $('#parsons_goal_line_container_' + counter).show();
    }
    $('#parsons_explanation_story').text(response.story);
}

function updateNextExerciseButton(level: number, exercise: number) {
    const max_exercise = <number>($('#next_parson_button').attr('max_exercise') || 1);
    // If there is another exercise: add the onclick for next exercise
    if (exercise < max_exercise) {
        $('#next_parson_button').attr('onclick', 'hedyApp.loadParsonsExercise(' + level + ", " + (exercise+1) + ");");
    } else {
        $('#next_parson_button').attr('onclick', null);
    }
}

export function loadNextExercise() {
    // Todo...
}

function parse_code_string_into_dict(code: string) {
    // Fixme: For relic code support we still need the alphabetic order
    const splitted_code = code.split(/\r?\n/).filter(e => String(e).trim());
    let code_lines: Record<string, string> = {};
    for (let index = 0; index < splitted_code.length; index++) {
        code_lines[index+1] = splitted_code[index]
    }
    return code_lines;
}

// https://stackoverflow.com/questions/26503595/javascript-shuffling-object-properties-with-their-values
function shuffle_code_lines(code: string) {
    const code_lines = parse_code_string_into_dict(code);
    let shuffled: Record<string, string> = {};
    let keys = Object.keys(code_lines);
    fisherYatesShuffle(keys);
    for (const k of keys) {
        shuffled[k] = code_lines[k];
    }
    return shuffled;
}

/**
 * Shuffle an array in-place
 */
function fisherYatesShuffle<A>(xs: A[]) {
    for (let i = xs.length - 1; i >= 1; i--) {
        const j = Math.floor(Math.random() * i);
        const h = xs[j];
        xs[j] = xs[i];
        xs[i] = h;
    }
}

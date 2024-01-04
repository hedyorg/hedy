import {modal} from "./modal";
import {stopit, store_parsons_attempt} from "./app";
import { HedyEditor } from "./editor";
import { HedyCodeMirrorEditorCreator } from "./cm-editor";
import Sortable from "sortablejs";

interface ParsonsExercise {
    readonly story: number;
    readonly code_lines: Record<string, string>;
    readonly code: string;
}

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
       modal.notifyError(err.responseText);
    });
}

function resetView() {
    stopit();
    // Initialize in case it hasn't been initialized before
    if (Object.keys(editorDict).length === 0) {
        initializeParsons();
    }
    $('#output').empty();
    $('.parsons_goal_line_container').removeClass('border-green-500 border-red-500');
}

function updateHeader(exercise: number) {
    $('.parsons_header_text_container').hide();
    $('.step').removeClass('current');

    $('#parsons_header_text_' + exercise).show();
    $('#parsons_header_' + exercise).addClass('current');
}
let editorDict: Record<number, HedyEditor> = {}
function showExercise(response: ParsonsExercise) {
    const code_lines = parse_code_string_into_dict(response.code);
    let keys = Object.keys(code_lines);

    // Hide all containers, show the onces relevant dynamically
    $('.parsons_start_line_container').hide();
    $('.parsons_goal_line_container').hide();

    fisherYatesShuffle(keys);

    keys.forEach((key, i) => {
        const valueObj = code_lines[key];
        const counter = i + 1;
        // Temp output to console to make sure TypeScript compiles
        const goalEditor = editorDict[i + 1];
        goalEditor.contents = valueObj;

        document.getElementById('parsons_line_data_' + counter)!.dataset['index'] = key;
        document.getElementById('parsons_line_data_' + counter)!.dataset['code'] = valueObj;
        $('#parsons_line_' + counter).show();
    });

    let parsons = document.getElementById('parsons_code_container')!

    Sortable.create(parsons,{
        animation: 150,
        onStart: () => {
            $('.parsons_goal_line_container').removeClass('border-green-500 border-red-500');
        },
    });

    $('#parsons_explanation_story').text(response.story);
}

function updateNextExerciseButton(level: number, exercise: number) {
    const max_exercise = <number>($('#next_parson_button').attr('max_exercise') || 1);
    // If there is another exercise: add the onclick for next exercise
    if (exercise < max_exercise) {
        $('#next_parson_button').on('click', () => loadParsonsExercise(level, exercise+1));
    } else {
        $('#next_parson_button').off('click');
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

export function get_parsons_code() {
    let code = "";
    let order = new Array();
    let mistake = false;
    document.querySelectorAll<HTMLElement>('#parsons_code_container > div > div').forEach((element, key) => {        
     // We are not interested in elements that are hidden
      if (!$(element).is(':visible')) {
        return;
      }
      // the parent is the one that has the borders...
      const parent = element.parentElement!
      let text = element.dataset['code'] || "";
      if (text.length > 1) {
        // Also add a newline as we removed this from the YAML structure
        code += text + "\n";
      }
      parent.classList.remove('border-green-500');
      parent.classList.remove('border-red-500');
      const index = element.dataset['index'] || 999;
      if (index == key + 1) {
        parent.classList.add('border-green-500');
      } else {
        mistake = true;
        parent.classList.add('border-red-500');
      }
      order.push(index);
    });

    // Before returning the code we want to a-sync store the attempt in the database
    // We only have to set the order and level, rest is handled by the back-end
    store_parsons_attempt(order, !mistake);
    if (mistake) {
      return "";
    }
    return code.replace(/ +$/mg, '');
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

export function initializeParsons() {
    // Do not initialize twice
    if (Object.keys(editorDict).length > 0) {
        return;
    }
    const editorCreator = new HedyCodeMirrorEditorCreator();
    const parsonCodeContainers = document.querySelectorAll('#parsons_code_container > div > pre');
    parsonCodeContainers.forEach((container, i) => {
        const editor = editorCreator.initializeReadOnlyEditor(container as HTMLElement, 'ltr');
        editorDict[i + 1] = editor;
    })
}
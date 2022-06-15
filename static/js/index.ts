import {modal} from "./modal";

export * from './modal';
export * from './app';
export * from './auth';
export * from './statistics';
export * from './tutorial';
export * from './quiz';
export * from './parsons';
import './syntaxModesRules';
import './tabs';
import './translating';
import {loadQuestQuestion} from "./quiz";
export * from './teachers';

export function startQuiz(level: number) {
    $('#start_parsons_container').hide();
    $.ajax({
      type: 'POST',
      url: '/quiz/initialize_user',
      data: JSON.stringify({
        level: level
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function() {
        loadParsonsExercise(level, 1);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
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
}
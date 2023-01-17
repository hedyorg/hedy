import {modal} from "./modal";
import {showAchievements} from "./app";

(function() {
    $('.option-block').on("click", function () {
        // Remove active attribute and hide possible answer button
        $('.option-block').removeClass('border-double border-8 active');
        $('.submit-button').hide();

        // Add active attribute and show correct answer button
        $(this).addClass('border-double border-8 active');
        $(this).find(".submit-button").show();
    });
})();


export function startQuiz(level: number) {
    $('#start_quiz_container').hide();
    $.ajax({
      type: 'POST',
      url: '/quiz/initialize_user',
      data: JSON.stringify({
        level: level
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function() {
        loadQuizQuestion(level, 1);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

export function loadQuizQuestion(level: number, question: number) {
    // If we get the request from the feedback page -> always hide the feedback container
    $('#quiz_feedback_container').hide();

    // If we have a forced keyword language, sent this info to the back-end to get the correct question
    let parameters = new URLSearchParams(window.location.search)
    let url = "/quiz/get-question/" + level + '/' + question;
    if (parameters.has('keyword_language')) {
        url += "/" + parameters.get('keyword_language')
    }

    $.ajax({
      type: 'GET',
      url: url,
      dataType: 'json'
    }).done(function(response: any) {
        $('#quiz_container').show();
        showQuestion(response.question_text);
        if (response.code) {
            $('#quiz_question_output_container').hide();
            showQuestionCode(response.code);
        } else {
            $('#quiz_question_code_container').hide();
            if (response.output) {
                showQuestionOutput(response.output);
            } else {
                $('#quiz_question_output_container').hide();
            }
        }
        showAnswers(response.mp_choice_options, level, question);
        highlightQuestionBar(question);
        loadHint(response.hint);
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showQuestion(question: string) {
    $('#quiz_question_title').html(parseCodeBlocks(question));
    $('#quiz_question_container').show();
}

function showQuestionCode(code: string) {
    $('#quiz_question_code_container').show();
    let editor = ace.edit("quiz_question_code");
    editor.setValue(code);
    editor.clearSelection(); // Make sure the ace editor is not selected
    editor.renderer.$cursorLayer.element.style.display = "none"; // Also remove the cursor
}

function showQuestionOutput(output: string) {
    $('#quiz_question_output_container').empty();
    const color = "white";
    $('<span class="whitespace-pre-wrap">').text(output).css({color}).appendTo('#quiz_question_output_container');
    $('#quiz_question_output_container').show();
}

function showAnswers(options: any, level: number, question: number) {
    // This solution is far from beautiful but seems to best approach to parse YAML code down to the editor
    // If we find three backticks -> the answer is a code snippet: remove the backticks and show as snippet
    $('.option-block').hide();
    $('.option-block').removeClass('incorrect-option');
    for (let i = 1; i < options.length+1; ++i) {
        if (options[i-1].option.includes("```")) {
            $('#answer_text_' + i).hide();
            let editor = ace.edit('answer_code_' + i);
            // This does look like magic: It removes all backticks and the resting newlines
            editor.setValue($.trim(options[i-1].option.replace(new RegExp('```', 'g'),"")));
            editor.clearSelection(); // Make sure the ace editor is not selected
            editor.renderer.$cursorLayer.element.style.display = "none"; // Also remove the cursor
            $('#answer_code_' + i).show();
            // We have to "click" the editor as for some reason the code is always selected?
            $('#answer_code_' + i).click();
        } else {
            $('#answer_text_' + i).html(parseCodeBlocks(options[i - 1].option));
            $('#answer_code_' + i).hide();
            $('#answer_text_' + i).show();
        }
        let container = $('#answer_container_' + i);
        // Set relevant info on container so we can catch this on answering
        container.attr('level', level);
        container.attr('question', question);
        container.removeClass('border-double border-8 active');
        container.find(".submit-button").hide(); // Not sure why but $('.submit-button').hide() doesn't work globally!
        container.show();
    }
    $('#quiz_answers_container').show();
}

function parseCodeBlocks(option: string) {
    while(option.indexOf('`') != -1 ) {
        option = option.replace('`', '<code>').replace('`', '</code>');
    }
    return option;
}

function highlightQuestionBar(question: number) {
    $('.question_header_text_container').hide();
    $('.step').removeClass('current');

    $('#question_header_text_' + question).show();
    $('#question_header_' + question).addClass('current');
}

function loadHint(hint: string) {
    $('#quiz_question_hint').html(parseCodeBlocks(hint));
    $('#quiz_question_hint').hide();
}

export function answerQuestion(answer_number: number) {
    let element = $('#answer_container_' + answer_number);
    let level = element.attr('level');
    let question = element.attr('question');

    $.ajax({
      type: 'POST',
      url: '/quiz/submit_answer/',
      data: JSON.stringify({
        level: level,
        question: question,
        answer: answer_number
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response: any) {
        if (response.attempt == 1 && !response.correct) {
            highlightFaultyAnswer(answer_number);
            showFaultyFeedback(response.feedback);
        }
        else if (response.correct) {
            showFeedback(response, question || "", true);
            updateHeader(question || "", true);
        } else {
            showFeedback(response, question || "", false);
            updateHeader(question || "", false);
        }
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function highlightFaultyAnswer(answer_number: number) {
    $('.option-block').removeClass('active');
    $('#answer_container_' + answer_number).addClass('incorrect-option');
}

function showFaultyFeedback(feedback: string) {
    $('#quiz_question_hint').html(parseCodeBlocks(feedback));
    $('#quiz_question_hint').show();
}

function showFeedback(response: any, question: string, correct: boolean) {
    $('#quiz_question_container').hide();
    $('#quiz_answers_container').hide();

    $('#question_number_container').text(question);
    $('#question_length_container').text(response.max_question);

    if (response.next_question) {
        $('#next_question_number_container').text(parseInt(question) + 1);
        $('#next_question_button').attr('onclick', "hedyApp.loadQuizQuestion(" + response.level + "," + (parseInt(question) + 1) + ");");
        $('#next_question_button').show();
    } else {
        $('#next_question_button').hide();
        $('#results_button').show();
    }

    $('#question_feedback_text_container').html(parseCodeBlocks(response.question_text));
    $('#feedback_feedback_text').text(response.feedback);
    if (response.correct_answer_text.includes("```")) {
        let editor = ace.edit("feedback_answer_code");
        editor.setValue($.trim(response.correct_answer_text.replace(new RegExp('`', 'g'),"")));
        editor.clearSelection(); // Make sure the ace editor is not selected
        editor.renderer.$cursorLayer.element.style.display = "none"; // Also remove the cursor
        $('#feedback_correct_answer_container').hide();
        $('#feedback_answer_code').show();
    } else {
        // Replace the first backtick by an opening code block, the second one with a closing tag
        $('#feedback_correct_answer_container').html(parseCodeBlocks(response.correct_answer_text));
        $('#feedback_answer_code').hide();
        $('#feedback_correct_answer_container').show();
    }
    if (correct) {
        $('#feedback_incorrect_container').hide();
        $('#feedback_correct_container').show();
    } else {
        $('#feedback_correct_container').hide();
        $('#feedback_incorrect_container').show();
    }
    $('#quiz_feedback_container').show();
}

function updateHeader(question: string, correct: boolean) {
    if (correct) {
        $('#question_header_' + question).addClass('bg-green-400');
    } else {
        $('#question_header_' + question).addClass('bg-red-400');
    }
}

export function showQuizResults(level: number) {
    $.ajax({
      type: 'GET',
      url: '/quiz/get_results/' + level,
      dataType: 'json'
    }).done(function(response: any) {
        showResults(response);
        if (response.achievement) {
            showAchievements(response.achievements, false, "");
        }
    }).fail(function(err) {
       modal.alert(err.responseText, 3000, true);
    });
}

function showResults(response: any) {
    $('#quiz_container').hide();
    $('#quiz_end_score').text(response.score);
    $('#end_quiz_container').show();
}

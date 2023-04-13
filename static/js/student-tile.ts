function expandStudentTile(student: any) {
    const average_quiz = student.average_quiz;
    const success_rate_highest_level = student.success_rate_highest_level;
    const success_rate_overall = student.success_rate_overall;
    const highest_level_quiz = student.highest_level_quiz;
    const highest_level_quiz_score = student.highest_level_quiz_score;

    let bigTile = document.getElementById('expanded-student-tile')!;
    bigTile.innerHTML =
        '<p class="font-bold text-lg">' + student.username + '</p>' +
        '<p>Success overall:  ' + success_rate_overall + '</p>' +
        '<p>Highest level: ' + highest_level_quiz + '</p>' +
        '<p>Quiz avg: ' + average_quiz + '</p></br>' +
        '<p>Success rate highest level' + '(' + highest_level_quiz + '): ' + success_rate_highest_level + '</p>' +
        '<p>Quiz score highest level' + '(' + highest_level_quiz + '): ' + highest_level_quiz_score + '</p>';
    bigTile.classList.remove('hidden');
}

function hideStudentTile() {
    $('#expanded-student-tile').addClass('hidden');
}

function studentTileClicked(event: any, student: any) {
    const currentlySelected = $(event.target).closest('.student-tile').hasClass('selected');

    // Remove 'selected' attribute from all student tiles
    $('.student-tile').removeClass('selected');

    // Select the currently clicked tile, or unselect if it was already selected
    if (currentlySelected) {
        hideStudentTile();
    } else {
        $(event.target).closest('.student-tile').addClass('selected');
        expandStudentTile(student);
    }
}

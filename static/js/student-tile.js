function expandStudentTile(student) {
    const average_quiz = student.average_quiz;
    const success_rate_highest_level = student.success_rate_highest_level;
    const success_rate_overall = student.success_rate_overall;
    const highest_level_quiz = student.highest_level_quiz;
    const highest_level_quiz_score = student.highest_level_quiz_score;

    let bigTile = document.getElementById('expanded-student-tile');
    bigTile.innerHTML =
        '<p class="font-bold text-lg">' + student.username + '</p>' +
        '<p>Success overall:  ' + success_rate_overall + '</p>' +
        '<p>Highest level: ' + highest_level_quiz + '</p>' +
        '<p>Quiz avg: ' + average_quiz + '</p></br>' +
        '<p>Success rate highest level' + '(' + highest_level_quiz + '): ' + success_rate_highest_level + '</p>' +
        '<p>Quiz score highest level' + '(' + highest_level_quiz + '): ' + highest_level_quiz_score + '</p>';
    bigTile.classList.remove('hidden');
}

function studentTileClicked(event, student) {
    // removing active green color when clicking student-tile
    let tiles = document.querySelectorAll('.student-tile');
    tiles.forEach(function (tile) {
        tile.classList.remove('bg-green-400');
        let studentTileText = tile.querySelectorAll('.student-tile p');
        studentTileText.forEach(function (textElement) {
            textElement.style.color = 'black';
        });
    });

    // adding an active green color to student-tile
    let clickedStudentTile = event.target;
    if (clickedStudentTile.tagName === 'P') {
        clickedStudentTile = clickedStudentTile.parentElement;
    }
    clickedStudentTile.classList.add('bg-green-400');
    let studentTileText = clickedStudentTile.querySelectorAll('.student-tile p');
    studentTileText.forEach(function (textElement) {
        textElement.style.color = 'white';
    });

    expandStudentTile(student);
}

let studentTiles = document.querySelectorAll('.student-tile');
// highlighting when mousing over/out student-tile
studentTiles.forEach(function (tile) {
    tile.addEventListener('mouseover', function () {
        let studentTileText = tile.querySelectorAll('.student-tile p');
        studentTileText.forEach(function (textElement) {
            textElement.style.color = 'white';
        });
    });
    tile.addEventListener('mouseout', function () {
        if (!tile.classList.contains('bg-green-400')) {
            let studentTileText = tile.querySelectorAll('.student-tile > p');
            studentTileText.forEach(function (textElement) {
                textElement.style.color = 'black';
            });
        }
    });
});

function expandStudentTile(student) {
    let bigTile = document.getElementById('expanded-student-tile');
    bigTile.innerHTML =
        '<p class="font-bold text-lg">' + student.username + '</p>' +
        '<p>Success overall: </p>' +
        '<p>Highest level: ' + student.highest_level + '</p>' +
        '<p>Quiz avg: ' + student.average_quiz + '</p></br>' +
        '<p>Success rate highest level(x): </p>' +
        '<p>Quiz score highest level(x): </p>';
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

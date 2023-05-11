import {Chart} from "chart.js";

let studentTileChart: Chart<"bar", number[], string>;

function expandStudentTileChart(student: any){

    let bigTile = document.getElementById('expanded-student-tile')!;
    let studentName = document.getElementById('studentName')!;
    let ctx = document.getElementById('studentProgressionChart') as HTMLCanvasElement;

    if (studentTileChart != null) {
        studentTileChart.destroy();
    }

    studentTileChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: 'Program Progression (%)',
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    studentName.textContent = student.username;
    bigTile.classList.remove('hidden');
}

function hideStudentTileChart() {
    $('#expanded-student-tile').addClass('hidden');
}

export function studentTileChartClicked(event: any, student: any): void {
    const currentlySelected = $(event.target).closest('.student-tile').hasClass('selected');

    // Remove 'selected' attribute from all student tiles
    $('.student-tile').removeClass('selected');

    // Select the currently clicked tile, or unselect if it was already selected
    if (currentlySelected) {
        hideStudentTileChart();
    } else {
        $(event.target).closest('.student-tile').addClass('selected');
        expandStudentTileChart(student);
    }
}


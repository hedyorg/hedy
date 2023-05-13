import {Chart} from "chart.js";

let studentTileChart: Chart<"bar", number[], string>;

function createNewProgressionChart(ctx: HTMLCanvasElement, studentLevels: string[], studentProgression: number[]): Chart<"bar", number[], string> {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: studentLevels,
            datasets: [{
                label: 'Program Progression (%)',
                data: studentProgression,
                borderWidth: 1,
                borderColor: '#36A2EB',
                backgroundColor: '#9BD0F5',
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Adventure Progression of a student',
                    font: {
                        size: 24,
                    }
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                },
                x: {
                    title: {
                        display: true,
                        text: "Levels",
                        font: {
                            size: 15
                        }
                    },
                }
            }
        }
    });
}

function expandStudentTileChart(student: any, levels: string[], programs: number[]){
    let bigTile = document.getElementById('expanded-student-tile')!;
    let studentName = document.getElementById('studentName')!;
    let ctx = document.getElementById('studentProgressionChart') as HTMLCanvasElement;

    // Ensure that the studentTileChart (chart bar) is reset each time a different student tile is clicked
    if (studentTileChart != null) {
        studentTileChart.destroy();
    }

    studentTileChart = createNewProgressionChart(ctx, levels, programs);

    studentName.textContent = student.username;
    bigTile.classList.remove('hidden');
}

function hideStudentTileChart() {
    $('#expanded-student-tile').addClass('hidden');
}

export function studentTileChartClicked(event: any, student: any, levels: string[], programs: number[]): void {
    const currentlySelected = $(event.target).closest('.student-tile').hasClass('selected');

    // Remove 'selected' attribute from all student tiles
    $('.student-tile').removeClass('selected');

    // Select the currently clicked tile, or unselect if it was already selected
    if (currentlySelected) {
        hideStudentTileChart();
    } else {
        $(event.target).closest('.student-tile').addClass('selected');
        expandStudentTileChart(student, levels, programs);
    }
}

export function loadQuizChartClicked() {
    let ctx = document.getElementById('studentQuizChart') as HTMLCanvasElement;

    let studentLevels: string[] = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"];
    let studentProgression: number[] = [12, 19, 3, 5, 2, 3];

    createNewProgressionChart(ctx, studentLevels, studentProgression);
}

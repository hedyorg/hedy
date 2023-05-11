import {Chart} from "chart.js";

let studentTileChart: Chart<"bar", number[], string>;

function expandStudentTileChart(student: any, levels: string[]){

    let bigTile = document.getElementById('expanded-student-tile')!;
    let studentName = document.getElementById('studentName')!;
    let ctx = document.getElementById('studentProgressionChart') as HTMLCanvasElement;

    if (studentTileChart != null) {
        studentTileChart.destroy();
    }

    let studentLevels: string[] = levels
    let studentProgression: number[] = [12, 19, 3, 5, 2, 3]

    studentTileChart = new Chart(ctx, {
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

    studentName.textContent = student.username;
    bigTile.classList.remove('hidden');
}

function hideStudentTileChart() {
    $('#expanded-student-tile').addClass('hidden');
}

export function studentTileChartClicked(event: any, student: any, levels: string[]): void {
    const currentlySelected = $(event.target).closest('.student-tile').hasClass('selected');

    // Remove 'selected' attribute from all student tiles
    $('.student-tile').removeClass('selected');

    // Select the currently clicked tile, or unselect if it was already selected
    if (currentlySelected) {
        hideStudentTileChart();
    } else {
        $(event.target).closest('.student-tile').addClass('selected');
        expandStudentTileChart(student, levels);
    }
}


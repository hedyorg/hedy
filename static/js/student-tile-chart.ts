import {Chart, ChartTypeRegistry} from "chart.js";

let studentTileChart: Chart<"bar", number[], string>;
let dataLoaded = false

function expandStudentTileChart(student: any, levels: string[], programs: number[]){
    let bigTile = document.getElementById('expanded-student-tile')!;
    let studentName = document.getElementById('student-name')!;
    const ctx = document.getElementById('student-progression-chart') as HTMLCanvasElement;

    // Ensure that the studentTileChart (chart bar) is reset each time a different student tile is clicked
    if (studentTileChart != null) {
        studentTileChart.destroy();
    }

    let chartMax: number = 15
    let chartType: keyof ChartTypeRegistry = "bar";
    let chartLabel = 'Program progression per level (%)';
    let chartTitle: string = 'Level Progression';
    studentTileChart = createNewChart(ctx, levels, programs, chartMax, chartLabel, chartTitle, chartType);

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

export function loadQuizChart(levels: string[], students: any) {
    if (!dataLoaded) {
        for (let i = 0; i < students.length; i++) {
            let student = students[i];
            let avg_quizzes_per_level = student['average_quizzes_ran_per_level'];
            let elementString = "static-student-tile-" + student['username'];

            const div = document.getElementById(elementString) as HTMLDivElement;
            let canvas = document.createElement('canvas');
            canvas.width = 350;
            canvas.height = 250;
            canvas.id = "canvas-" + student['username'];
            div.appendChild(canvas);

            let chartMax: number = 100;
            let chartType: keyof ChartTypeRegistry = "line";
            let chartLabel = 'Average quiz per level (%)';
            let chartTitle: string = 'Average Quiz';
            createNewChart(canvas, levels, avg_quizzes_per_level, chartMax, chartLabel, chartTitle, chartType);
        }
        dataLoaded = true;
    }
}

function createNewChart(ctx: HTMLCanvasElement, studentLevels: string[], data: number[],  max: number, chartLabel: string, chartTitle: string, chartType: any): Chart<"bar", number[], string> {
    return new Chart(ctx, {
        type: chartType,
        data: {
            labels: studentLevels,
            datasets: [{
                label: chartLabel,
                data: data,
                borderWidth: 1,
                borderColor: '#36A2EB',
                backgroundColor: '#9BD0F5',
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: chartTitle,
                    font: {
                        size: 24,
                    }
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: max,
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

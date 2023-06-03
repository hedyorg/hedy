import {Chart, ChartType} from "chart.js";

let studentTileChart: Chart<ChartType, number[][], string>;
let dataLoaded = false

function expandStudentTileChart(student: any, levels: string[], successRuns: number[], errorRuns: number[]){
    let bigTile = document.getElementById('expanded-student-tile')!;
    let studentName = document.getElementById('student-name')!;
    const ctx = document.getElementById('student-progression-chart') as HTMLCanvasElement;

    // Ensure that the studentTileChart (chart bar) is reset each time a different student tile is clicked
    if (studentTileChart != null) {
        studentTileChart.destroy();
    }

    const chartMax: number = 15
    const chartTitle: string = 'Level Progression';
    const chartFailColor = "#fd7f6f";
    const chartSuccessColor = "#b2e061";
    const chartSuccessLabel = "Successful runs";
    const chartFailLabel = "Failed runs";

    const data = [successRuns, errorRuns]
    const chartColors = [chartSuccessColor, chartFailColor]
    const chartLabels = [chartSuccessLabel, chartFailLabel]

    const datasets = initChart(levels, data, chartLabels, chartColors)

    studentTileChart = createNewChart(ctx, datasets, chartMax, chartTitle, "bar");

    studentName.textContent = student.username;
    bigTile.classList.remove('hidden');
}

function hideStudentTileChart() {
    $('#expanded-student-tile').addClass('hidden');
}

export function studentTileChartClicked(event: any, student: any, levels: string[], success_runs: number[], error_runs: number[]): void {
    const currentlySelected = $(event.target).closest('.student-tile').hasClass('selected');

    // Remove 'selected' attribute from all student tiles
    $('.student-tile').removeClass('selected');

    // Select the currently clicked tile, or unselect if it was already selected
    if (currentlySelected) {
        hideStudentTileChart();
    } else {
        $(event.target).closest('.student-tile').addClass('selected');
        expandStudentTileChart(student, levels, success_runs, error_runs);
    }
}

export function loadQuizChart(levels: string[], students: any) {
    if (!dataLoaded) {
        for (let i = 0; i < students.length; i++) {
            let student = students[i];
            let avg_quizzes_per_level = student['avg_quizzes_runs_per_level'];
            let elementString = "static-student-tile-" + student['username'];

            const div = document.getElementById(elementString) as HTMLDivElement;
            let canvas = document.createElement('canvas');
            canvas.width = 350;
            canvas.height = 250;
            canvas.id = "canvas-" + student['username'];
            div.appendChild(canvas);

            let chartMax: number = 100;
            let chartLabel = 'Average quiz per level (%)';
            let chartTitle: string = 'Average Quiz';

            const data = {
              labels: levels,
              datasets: [
                {
                  label: chartLabel,
                  data: avg_quizzes_per_level,
                    borderColor: '#36A2EB',
                    backgroundColor: '#9BD0F5',
                },
              ]
            };

            createNewChart(canvas, data, chartMax, chartTitle, "line");
        }
        dataLoaded = true;
    }
}

function createNewChart(ctx: HTMLCanvasElement, data: any, max: number, chartTitle: string, chartType: any): Chart<ChartType, number[][], string> {
    return new Chart(ctx, {
        type: chartType,
        data: data,
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
                    stacked: true,
                },
                x: {
                    title: {
                        display: true,
                        text: "Levels",
                        font: {
                            size: 15
                        }
                    },
                    stacked: true,
                }
            }
        }
    });
}

function initChart(levels: string[], data: any, chartLabels: any, chartColor: any) {
    return {
      labels: levels,
      datasets: [
        {
          label: chartLabels[0],
          data: data[0],
            backgroundColor: chartColor[0],
        },
        {
          label: chartLabels[1],
          data: data[1],
            backgroundColor: chartColor[1],
        },
      ]
    };
}

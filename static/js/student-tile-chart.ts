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
    const chartFailColor: string = "#fd7f6f";
    const chartSuccessColor: string = "#b2e061";
    const chartSuccessLabel: string = "Successful runs";
    const chartFailLabel: string = "Failed runs";

    const data = [successRuns, errorRuns]
    const chartColors = [chartSuccessColor, chartFailColor]
    const chartLabels = [chartSuccessLabel, chartFailLabel]
    const chartData = initChartData(data, chartColors, chartLabels, levels)
    studentTileChart = createNewChart(ctx, chartData, chartMax, chartTitle, "bar");

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
            let avg_quizzes_runs_per_level = student['avg_quizzes_runs_per_level'];
            let elementString = "static-student-tile-" + student['username'];

            const div = document.getElementById(elementString) as HTMLDivElement;
            let canvas = document.createElement('canvas');
            canvas.width = 350;
            canvas.height = 250;
            canvas.id = "canvas-" + student['username'];
            div.appendChild(canvas);

            const chartMax: number = 100;
            const chartLabel: string = 'Average quiz per level (%)';
            const chartTitle: string = 'Average Quiz';
            const chartColor: string = '#9BD0F5';

            const data = [avg_quizzes_runs_per_level]
            const chartColors = [chartColor]
            const chartLabels = [chartLabel]
            const chartData = initChartData(data, chartColors, chartLabels, levels)
            createNewChart(canvas, chartData, chartMax, chartTitle, "line");
        }
        dataLoaded = true;
    }
}

function initChartData(data: any[], chartColor: string[], chartLabel: string[], levels: any) {
    let datasets: {label: string, data: any, backgroundColor: any}[] = [];

    for (let i  = 0; i < data.length; i++) {
        datasets.push({
            backgroundColor: chartColor[i],
            data: data[i],
            label: chartLabel[i]
        })
    }

    return {
        labels: levels,
        datasets: datasets
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

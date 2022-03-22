import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);


const chart_fail_color = "#fd7f6f";
const chart_success_color = "#b2e061";
const chart_neutral_color = "#7eb0d5";
const chart_colors = ["#fd7f6f", "#b2e061", "#7eb0d5", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]
const chart_level_colors = ['#fbcb8d', '#f9ac48', '#f18c07', '#ac6405', '#673c03', '#fce28c', '#fad146', '#f3bd05', '#ae8704', '#685102', '#b3d5b5', '#85bc89', '#58a15d', '#3f7342', '#254528', '#fab28e', '#f78449', '#ef5709', '#ab3e07', '#662504', '#dbadb8', '#c57b8d', '#ad4c63', '#7c3647', '#4a202a']


export const stats = {
  getProgramStats: function (weeksBack: number, element: any) {
    if (element.classList.contains('active')) {
      return false
    }

    startLoadingCharts();
    setActive(element);
    const data = getRequestData(weeksBack);

    $.get('/program-stats', data).done (function (response) {

      // update program runs per level charts
      const failedRunsPerLevelDataset = generatePerLevelDataset('Failed runs', response['per_level'], 'data.failed_runs', chart_fail_color, false);
      const successfulRunsPerLevelDataset = generatePerLevelDataset('Successful runs', response['per_level'], 'data.successful_runs', chart_success_color, false);
      const errorRatePerLevelDataset = generatePerLevelDataset('Error rate', response['per_level'], 'data.error_rate', chart_fail_color, true);

      updateChart('programRunsPerLevelChart', [successfulRunsPerLevelDataset, failedRunsPerLevelDataset]);
      updateChart('errorRatePerLevelChart', [errorRatePerLevelDataset]);


      // update program runs per week charts
      const levels = flattenWeekProps(response['per_week'], ['successful_runs', 'failed_runs'], (el: string) => el.toLowerCase().startsWith('l'));
      const successfulRunsPerWeekDatasets = generateDatasets(levels, response['per_week'], 'week', 'data.successful_runs.', chart_level_colors, false);
      const failedRunsPerWeekDatasets = generateDatasets(levels, response['per_week'], 'week', 'data.failed_runs.', chart_level_colors, false);

      updateChart('successfulRunsPerWeekChart', successfulRunsPerWeekDatasets);
      updateChart('failedRunsPerWeekChart', failedRunsPerWeekDatasets);
      updateSharedLegend('#admin-program-runs-legend', successfulRunsPerWeekDatasets, '.admin-runs-chart');

      // update exceptions per level and per week charts
      const exceptions = flattenExProps(response['per_level'], (el: string) => el.toLowerCase().endsWith('exception'));
      const exLabelMapper = (e: string) => e.substr(0, e.length - 9);
      const exceptionsPerLevelDatasets = generateDatasets(exceptions, response['per_level'], 'level', 'data.', chart_colors, true, exLabelMapper);
      const exceptionsPerWeekDatasets = generateDatasets(exceptions, response['per_week'], 'week', 'data.', chart_colors, true, exLabelMapper);

      updateChart('exceptionsPerLevelChart', exceptionsPerLevelDatasets);
      updateChart('exceptionsPerWeekChart', exceptionsPerWeekDatasets);
      updateSharedLegend('#admin-exceptions-legend', exceptionsPerLevelDatasets, '.admin-exceptions-chart');

      // update user types per level and week charts
      const anonymousRunsPerLevelDataset = generatePerLevelDataset('Anonymous users', response['per_level'], 'data.anonymous_runs', chart_colors[0], false);
      const loggedRunsPerLevelDataset = generatePerLevelDataset('Logged users', response['per_level'], 'data.logged_runs', chart_colors[1], false);
      const studentRunsPerLevelDataset = generatePerLevelDataset('Student users', response['per_level'], 'data.student_runs', chart_colors[2], false);
      const unknownRunsPerLevelDataset = generatePerLevelDataset('Unknown type users', response['per_level'], 'data.user_type_unknown_runs', chart_colors[3], false);
      updateChart('usersPerLevelChart', [anonymousRunsPerLevelDataset, loggedRunsPerLevelDataset, studentRunsPerLevelDataset, unknownRunsPerLevelDataset]);

      const userTypes = ['anonymous_runs', 'logged_runs', 'student_runs', 'user_type_unknown_runs'];
      const userTypeLabelMapper = (e: string) => {
        if (e === 'anonymous_runs') return 'Anonymous users';
        if (e === 'logged_runs') return 'Logged users';
        if (e === 'student_runs') return 'Student users';
        return 'Unknown type users'
      };
      const userTypesPerWeekDatasets = generateDatasets(userTypes, response['per_week'], 'week', 'data.', chart_colors, true, userTypeLabelMapper);
      updateChart('usersPerWeekChart', userTypesPerWeekDatasets);

      // update quiz scores per level charts
      const completedQuizPerLevelDatasets = generatePerLevelDataset('Completed quizzes', response['per_level'], 'data.completed_quizzes', chart_success_color, true);
      const abandonedQuizPerLevelDatasets = generatePerLevelDataset('Abandoned quizzes', response['per_level'], 'data.abandoned_quizzes', chart_fail_color, true);
      const maxScorePerLevelDatasets = generatePerLevelDataset('Max score', response['per_level'], 'data.quiz_score_max.', chart_success_color, false);
      const minScorePerLevelDatasets = generatePerLevelDataset('Min score', response['per_level'], 'data.quiz_score_min.', chart_fail_color, false);
      const avgScorePerLevelDatasets = generatePerLevelDataset('Avg score', response['per_level'], 'data.quiz_score_avg.', chart_neutral_color, false);

      updateChart('completedQuizPerLevelChart', [completedQuizPerLevelDatasets]);
      updateChart('abandonedQuizPerLevelChart', [abandonedQuizPerLevelDatasets]);
      updateChart('maxScorePerLevelChart', [maxScorePerLevelDatasets]);
      updateChart('minScorePerLevelChart', [minScorePerLevelDatasets]);
      updateChart('avgScorePerLevelChart', [avgScorePerLevelDatasets]);

      // update quiz scores per week charts
      const levels_quizzes = flattenWeekProps(response['per_week'], ['completed_quizzes', 'abandoned_quizzes'], (el: string) => el.toLowerCase().startsWith('l'));

      const completedQuizPerWeekDatasets = generateDatasets(levels_quizzes, response['per_week'], 'week', 'data.completed_quizzes.', chart_colors, false);
      const abandonedQuizPerWeekDatasets = generateDatasets(levels_quizzes, response['per_week'], 'week', 'data.abandoned_quizzes.', chart_colors, false);
      const maxScorePerWeekDatasets = generateDatasets(levels_quizzes, response['per_week'], 'week', 'data.quiz_score_max.', chart_colors, false);
      const minScorePerWeekDatasets = generateDatasets(levels_quizzes, response['per_week'], 'week', 'data.quiz_score_min.', chart_colors, false);
      const avgScorePerWeekDatasets = generateDatasets(levels_quizzes, response['per_week'], 'week', 'data.quiz_score_avg.', chart_colors, false);

      updateChart('completedQuizPerWeekChart', completedQuizPerWeekDatasets);
      updateChart('abandonedQuizPerWeekChart', abandonedQuizPerWeekDatasets);
      updateChart('maxScorePerWeekChart', maxScorePerWeekDatasets);
      updateChart('minScorePerWeekChart', minScorePerWeekDatasets);
      updateChart('avgScorePerWeekChart', avgScorePerWeekDatasets);

      updateSharedLegend('#admin-quiz-legend', completedQuizPerWeekDatasets, '.admin-quiz-chart');

    }).fail (function (error) {
      console.log(error);
    }).always(function() {
      stopLoadingCharts();
    });

    return false;
  },

  getClassStats: function (classId: string, weeksBack: number, element: any) {
    if (element.classList.contains('active')) {
      return false
    }

    startLoadingCharts();
    setActive(element);
    const data = getRequestData(weeksBack);

    $.get('/class-stats/' + classId, data).done (function (response) {
      const class_per_level = response['class']['per_level'];
      const class_per_week = response['class']['per_week']

      // update program runs per level charts
      const failedRunsPerLevelDataset = generatePerLevelDataset('Failed runs', class_per_level, 'data.failed_runs', chart_fail_color, false);
      const successfulRunsPerLevelDataset = generatePerLevelDataset('Successful runs', class_per_level, 'data.successful_runs', chart_success_color, false);
      const errorRatePerLevelDataset = generatePerLevelDataset('Error rate', class_per_level, 'data.error_rate', chart_fail_color, true);

      updateChart('classProgramRunsPerLevelChart', [successfulRunsPerLevelDataset, failedRunsPerLevelDataset]);
      updateChart('classErrorRatePerLevelChart', [errorRatePerLevelDataset]);


      // update program runs per week charts
      const levels = flattenWeekProps(class_per_week, ['successful_runs', 'failed_runs'], (el: string) => el.toLowerCase().startsWith('l'));
      const successfulRunsPerWeekDatasets = generateDatasets(levels, class_per_week, 'week', 'data.successful_runs.', chart_level_colors, false);
      const failedRunsPerWeekDatasets = generateDatasets(levels, class_per_week, 'week', 'data.failed_runs.', chart_level_colors, false);

      updateChart('classSuccessfulRunsPerWeekChart', successfulRunsPerWeekDatasets);
      updateChart('classFailedRunsPerWeekChart', failedRunsPerWeekDatasets);
      updateSharedLegend('#class-program-runs-legend', successfulRunsPerWeekDatasets, '.class-runs-chart');

      // update exceptions per level and per week charts
      const exceptions = flattenExProps(class_per_level, (el: string) => el.toLowerCase().endsWith('exception'));
      const exLabelMapper = (e: string) => e.substr(0, e.length - 9);
      const exceptionsPerLevelDatasets = generateDatasets(exceptions, class_per_level, 'level', 'data.', chart_colors, true, exLabelMapper);
      const exceptionsPerWeekDatasets = generateDatasets(exceptions, class_per_week, 'week', 'data.', chart_colors, true, exLabelMapper);

      updateChart('classExceptionsPerLevelChart', exceptionsPerLevelDatasets);
      updateChart('classExceptionsPerWeekChart', exceptionsPerWeekDatasets);
      updateSharedLegend('#class-exceptions-legend', exceptionsPerLevelDatasets, '.class-exceptions-chart');

      const students_per_level = response['students']['per_level'];
      const students_per_week = response['students']['per_week'];

      // update program runs per week per level charts
      const students_level = flattenWeekProps(students_per_level, ['successful_runs', 'failed_runs'], () => true);
      const studentSuccessfulRunsPerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.successful_runs.', chart_colors, false);
      const studentFailedRunsPerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.failed_runs.', chart_colors, false);
      const studentErrorRatePerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.error_rate.', chart_colors, true);
      const studentCompletedQuizzesPerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.completed_quizzes.', chart_colors, false);
      const studentAbandonedQuizzesPerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.abandoned_quizzes.', chart_colors, false);
      const studentMaxScorePerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.quiz_score_max.', chart_colors, false);
      const studentMinScorePerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.quiz_score_min.', chart_colors, false);
      const studentAvgScorePerLevelDatasets = generateDatasets(students_level, students_per_level, 'level', 'data.quiz_score_avg.', chart_colors, false);

      updateChart('studentSuccessfulRunsPerLevelChart', studentSuccessfulRunsPerLevelDatasets);
      updateChart('studentFailedRunsPerLevelChart', studentFailedRunsPerLevelDatasets);
      updateChart('studentErrorRatePerLevelChart', studentErrorRatePerLevelDatasets);
      updateChart('studentCompletedQuizPerLevelChart', studentCompletedQuizzesPerLevelDatasets);
      updateChart('studentAbandonedQuizPerLevelChart', studentAbandonedQuizzesPerLevelDatasets);
      updateChart('studentMaxScorePerLevelChart', studentMaxScorePerLevelDatasets);
      updateChart('studentMinScorePerLevelChart', studentMinScorePerLevelDatasets);
      updateChart('studentAvgScorePerLevelChart', studentAvgScorePerLevelDatasets);

      // update program runs per week per level charts
      const students_week = flattenWeekProps(students_per_week, ['successful_runs', 'failed_runs'], () => true);
      const students_week_quizzes = flattenWeekProps(students_per_level, ['completed_quizzes', 'abandoned_quizzes'], () => true);
      const studentSuccessfulRunsPerWeekDatasets = generateDatasets(students_week, students_per_week, 'week', 'data.successful_runs.', chart_colors, false);
      const studentFailedRunsPerWeekDatasets = generateDatasets(students_week, students_per_week, 'week', 'data.failed_runs.', chart_colors, false);
      const studentErrorRatePerWeekDatasets = generateDatasets(students_week, students_per_week, 'week', 'data.error_rate.', chart_colors, true);
      const studentCompletedQuizPerWeekDatasets = generateDatasets(students_week_quizzes, students_per_week, 'week', 'data.completed_quizzes.', chart_colors, false);
      const studentAbandonedQuizPerWeekDatasets = generateDatasets(students_week_quizzes, students_per_week, 'week', 'data.abandoned_quizzes.', chart_colors, false);
      const studentMaxScorePerWeekDatasets = generateDatasets(students_week_quizzes, students_per_week, 'week', 'data.quiz_score_max.', chart_colors, false);
      const studentMinScorePerWeekDatasets = generateDatasets(students_week_quizzes, students_per_week, 'week', 'data.quiz_score_min.', chart_colors, false);
      const studentAvgScorePerWeekDatasets = generateDatasets(students_week_quizzes, students_per_week, 'week', 'data.quiz_score_avg.', chart_colors, false);

      updateChart('studentSuccessfulRunsPerWeekChart', studentSuccessfulRunsPerWeekDatasets);
      updateChart('studentFailedRunsPerWeekChart', studentFailedRunsPerWeekDatasets);
      updateChart('studentErrorRatePerWeekChart', studentErrorRatePerWeekDatasets);
      updateChart('studentCompletedQuizPerWeekChart', studentCompletedQuizPerWeekDatasets);
      updateChart('studentAbandonedQuizPerWeekChart', studentAbandonedQuizPerWeekDatasets);
      updateChart('studentMaxScorePerWeekChart', studentMaxScorePerWeekDatasets);
      updateChart('studentMinScorePerWeekChart', studentMinScorePerWeekDatasets);
      updateChart('studentAvgScorePerWeekChart', studentAvgScorePerWeekDatasets);

      // update common student chart legend
      updateSharedLegend('#student-legend', studentErrorRatePerLevelDatasets, '.student-chart');

    }).fail (function (error) {
      console.log(error);
    }).always(function() {
      stopLoadingCharts();
    });

    return false;
  },

  searchProgramLogs: function (classId: string) {
    var raw_data = $('#logs-search-form').serializeArray();
    var payload: any = {}
    $.map(raw_data, function(n){
        payload[n['name']] = n['value'];
    });
    payload['class_id'] = classId;

    $('#search-logs-empty-msg').hide();
    $('#search-logs-failed-msg').hide();
    $('#logs-spinner').show();
    $('#logs-load-more').hide();
    $('#search-logs-button').prop('disabled', true);
    $('#search-logs-table tbody').html('');

    const self = this;
    $.ajax ({type: 'POST', url: '/logs/query', data: JSON.stringify (payload), contentType: 'application/json; charset=utf-8'}).done (function (response) {
        if (response['query_status'] === 'SUCCEEDED') {
          self.logsExecutionQueryId = response['query_execution_id'];
          self.logsNextToken = '';
          self.fetchProgramLogsResults();
        } else {
          $('#search-logs-failed-msg').show();
        }
      }).fail (function (error) {
        $('#search-logs-failed-msg').show();
        console.log(error);
      }).always(function() {
        $('#logs-spinner').hide();
        $('#search-logs-button').prop('disabled', false);
      });

    return false;
  },

  logsExecutionQueryId: '',
  logsNextToken: '',

  fetchProgramLogsResults: function() {
    $('#logs-spinner').show();
    $('#search-logs-empty-msg').hide();
    $('#logs-load-more').hide();

    const data = {
      query_execution_id: this.logsExecutionQueryId,
      next_token: this.logsNextToken ? this.logsNextToken : undefined
    };

    const self = this;
    $.get('/logs/results', data).done (function (response) {
      const $logsTable = $('#search-logs-table tbody');

      response.data.forEach ((e: any) => {
        $logsTable.append(`<tr> \
          <td class="border px-4 py-2">${e.date}</td> \
          <td class="border px-4 py-2">${e.level}</td> \
          <td class="border px-4 py-2">${e.lang || ''}</td> \
          <td class="border px-4 py-2">${e.username || ''}</td> \
          <td class="border px-4 py-2">${e.exception || ''}</td> \
          <td class="border px-4 py-2"> \
            <button class="green-btn float-right top-2 right-2" onclick=hedyApp.stats.copyCode(this)>⇥</button> \
            <pre>${e.code}</pre> \
          </td></tr>`)
      });

      if (response.data.length == 0) {
        $('#search-logs-empty-msg').show();
      }

      self.logsNextToken = response.next_token;

    }).fail (function (error) {
      console.log(error);
    }).always(function() {
      $('#logs-spinner').hide();
      if (self.logsNextToken) {
        $('#logs-load-more').show();
      }
    });

    return false;
  },

  copyCode: function(el: any) {
    const copyButton = $(el);
    if (navigator.clipboard === undefined) {
      updateCopyButtonText(copyButton, 'Failed!');
    } else {
      navigator.clipboard.writeText(copyButton.next().text()).then(function() {
        updateCopyButtonText(copyButton, 'Copied!');
      }, function() {
        updateCopyButtonText(copyButton, 'Failed!');
      });
    }
    return false;
  },

  initializeAdminStats: function() {
    initChart('programRunsPerLevelChart', 'bar', 'Program runs per level', 'Level #', 'top', false, true);
    initChart('errorRatePerLevelChart', 'line', 'Error rate per level', 'Level #', 'top', true, false);

    initChart('successfulRunsPerWeekChart', 'bar', 'Successful runs per week', 'Week #', null, false, false);
    initChart('failedRunsPerWeekChart', 'bar', 'Failed runs per week', 'Week #', null, false, false);

    initChart('exceptionsPerLevelChart', 'line', 'Exceptions per level', 'Level #', null, false, false);
    initChart('exceptionsPerWeekChart', 'line', 'Exceptions per week', 'Week #', null, false, false);

    initChart('usersPerLevelChart', 'bar', 'User types per level', 'Level #', 'top', false, true);
    initChart('usersPerWeekChart', 'bar', 'User types per week', 'Week #', 'top', false, true);

    initChart('completedQuizPerLevelChart', 'bar', 'Completed quizzes per level', 'Level #', null, false, false);
    initChart('completedQuizPerWeekChart', 'bar', 'Completed quizzes per week', 'Week #', null, false, false);

    initChart('abandonedQuizPerLevelChart', 'bar', 'Abandoned quizzes per level', 'Level #', null, false, false);
    initChart('abandonedQuizPerWeekChart', 'bar', 'Abandoned quizzes per week', 'Week #', null, false, false);

    initChart('maxScorePerLevelChart', 'line', 'Max quiz score per level', 'Level #', null, false, false);
    initChart('maxScorePerWeekChart', 'line', 'Max quiz score per week', 'Week #', null, false, false);

    initChart('minScorePerLevelChart', 'line', 'Min quiz score per level', 'Level #', null, false, false);
    initChart('minScorePerWeekChart', 'line', 'Min quiz score per week', 'Week #', null, false, false);

    initChart('avgScorePerLevelChart', 'line', 'Avg quiz score per level', 'Level #', null, false, false);
    initChart('avgScorePerWeekChart', 'line', 'Avg quiz score per week', 'Week #', null, false, false);

    initializeElements();
  },

  initializeClassStats: function() {
    initChart('classProgramRunsPerLevelChart', 'bar', 'Program runs per level', 'Level #', 'top', false, true);
    initChart('classErrorRatePerLevelChart', 'line', 'Error rate per level', 'Level #', 'top', true, false);

    initChart('classSuccessfulRunsPerWeekChart', 'bar', 'Successful runs per week', 'Week #', null, false, false);
    initChart('classFailedRunsPerWeekChart', 'bar', 'Failed runs per week', 'Week #', null, false, false);

    initChart('classExceptionsPerLevelChart', 'line', 'Exceptions per level', 'Level #', null, false, false);
    initChart('classExceptionsPerWeekChart', 'line', 'Exceptions per week', 'Week #', null, false, false);

    initChart('studentSuccessfulRunsPerLevelChart', 'bar', 'Successful runs per level', 'Level #', null, false, false);
    initChart('studentFailedRunsPerLevelChart', 'bar', 'Failed runs per level', 'Level #', null, false, false);

    initChart('studentErrorRatePerLevelChart', 'line', 'Error rate per level', 'Level #', null, true, false);
    initChart('studentErrorRatePerWeekChart', 'line', 'Error rate per week', 'Week #', null, true, false);

    initChart('studentSuccessfulRunsPerWeekChart', 'bar', 'Successful runs per week', 'Week #', null, false, false);
    initChart('studentFailedRunsPerWeekChart', 'bar', 'Failed runs per week', 'Week #', null, false, false);

    initChart('studentCompletedQuizPerLevelChart', 'bar', 'Completed quizzes per level', 'Level #', null, false, false);
    initChart('studentCompletedQuizPerWeekChart', 'bar', 'Completed quizzes per week', 'Week #', null, false, false);

    initChart('studentAbandonedQuizPerLevelChart', 'bar', 'Abandoned quizzes per level', 'Level #', null, false, false);
    initChart('studentAbandonedQuizPerWeekChart', 'bar', 'Abandoned quizzes per week', 'Week #', null, false, false);

    initChart('studentMaxScorePerLevelChart', 'line', 'Max quiz score per level', 'Level #', null, false, false);
    initChart('studentMaxScorePerWeekChart', 'line', 'Max quiz score per week', 'Week #', null, false, false);

    initChart('studentMinScorePerLevelChart', 'line', 'Min quiz score per level', 'Level #', null, false, false);
    initChart('studentMinScorePerWeekChart', 'line', 'Min quiz score per week', 'Week #', null, false, false);

    initChart('studentAvgScorePerLevelChart', 'line', 'Avg quiz score per level', 'Level #', null, false, false);
    initChart('studentAvgScorePerWeekChart', 'line', 'Avg quiz score per week', 'Week #', null, false, false);

    initializeElements();
  },
}

/**
 Charts setup
 */
function initChart(elementId: string, chartType: any, title: string, xTitle: string, legendPosition: any,
                   is_percent: boolean, stacked: boolean) {
  const chart = document.getElementById(elementId) as HTMLCanvasElement;
  new Chart(chart, {
    type: chartType,
    data: {
      datasets: []
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: title
        },
        legend: {
          display: legendPosition !== null,
          position: legendPosition
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          stacked: stacked,
          scaleLabel: {
            display: is_percent,
            labelString: is_percent ? "Percentage" : ""
          },
          ticks: is_percent ? {
            min: 0,
            max: 100,
            callback: function(value: any) {
              return value + "%"
            }
          } : {}
        },
        x: {
          title: {
            display: true,
            text: xTitle
          },
          offset: true,
          stacked: stacked
        }
      }
    }
  });
}

/*
Chart functions
*/
function initializeElements() {
  // Show the first stats by default when the page loads
  $('.stats-period-toggle').first().click()

  // Hide irrelevant messages
  $('#logs-spinner').hide();
  $('#search-logs-failed-msg').hide();
  $('#search-logs-empty-msg').hide();

  const today = new Date().toISOString().split('T')[0];
  $('#logs-start-date').val(today + ' 00:00:00');
  $('#logs-end-date').val(today + ' 23:59:59');
}

function setActive(element: any) {
  $('.stats-period-toggle').removeClass('active');
  element.classList.add('active');
}

function startLoadingCharts() {
  $('.stats-data').hide();
  $('.stats-spinner').show();
}

function stopLoadingCharts() {
  $('.stats-spinner').hide();
  $('.stats-data').show();
}

function getRequestData(weeksBack: number) {
  let date = new Date();
  date.setDate(date.getDate() - (weeksBack - 1) * 7);
  let start = date.toISOString().split('T')[0];

  return { start: start };
}

function updateSharedLegend(id: string, datasets: any[], chartsClass: string) {
  var legend = $(id);
  // Clear legend contents
  legend.html('');

  // Add legend items based on the provided datasets
  datasets.map(el => el)
    .forEach ((e: any) => {
      legend.append(`<li data-chart-class="${chartsClass}" class="stats-legend-item">
        <div class="stats-legend-color-box" style="background-color:${e.backgroundColor};"></div>
      ${e.label}</li>`)
    });

  // Subscribe to the new item's click event
  var legendItems = $('.stats-legend-item');
  for (var i = 0; i < legendItems.length; i++) {
    legendItems[i].addEventListener("click", legendItemClickCallback, false);
  }
}

function legendItemClickCallback(event: any) {
  event = event || window.event;
  var target = event.target || event.srcElement;

  updateLegendItem(target);

  const chartsClass = $(target).data('chart-class');
  $(chartsClass).each(function() {
    const chart = Chart.getChart(this.id)!;
    updateChartSeries(chart, target.innerText);
  });
}

function updateLegendItem(target: any) {
  if (target.style.textDecoration !== '') {
    target.style.textDecoration = '';
  } else {
    target.style.textDecoration = 'line-through';
  }
}

function updateChartSeries(chart: any, seriesName: string) {
  for (var d = 0; d < chart.data.datasets.length; d++) {
    if (chart.data.datasets[d].label.trim() === seriesName.trim()) {
      chart.data.datasets[d].hidden = !chart.data.datasets[d].hidden;
    }
  }
  chart.update();
}

function flattenWeekProps(input: any[], properties: string[], filter: any) {
  if (input === undefined) {
    return [];
  }
  var result = new Set<string>();
  for (var i=0; i<input.length; i++) {
    const data = input[i]['data'];
    for (var p=0; p<properties.length; p++) {
      addProperties(result, data, properties[p], filter)
    }
  }

  return Array.from(result);
}

function addProperties(result: Set<string>, input: any[], propertyName: any, filter: any) {
   getPropertyNames(input[propertyName], filter).forEach(result.add, result);
}

function flattenExProps(input: any[], filter: any) {
  var result = new Set<string>();
  for (var i=0; i<input.length; i++) {
    getPropertyNames(input[i]['data'], filter).forEach(result.add, result);
  }
  return Array.from(result);
}

function getPropertyNames(data: any[], filter: any) {
  var result = new Set<string>();
  if (data !== undefined) {
    var keys = Object.keys(data)
    for (var i=0; i<keys.length; i++) {
      if (filter(keys[i])) {
        result.add(keys[i]);
      }
    }
  }
  return result;
}

function generatePerLevelDataset(label: string, data: any[], yAxisKey: string, color: string, showBorder: boolean) {
  return {
    label: label,
    data: data,
    parsing: {
      xAxisKey: 'level',
      yAxisKey: yAxisKey,
    },
    backgroundColor: [color],
    borderColor: [color],
    borderWidth: showBorder ? 2 : 0,
  }
}

function generateDatasets(data: any[], source: any[], xAxisKey: string, yAxisKey: string, colors: string[],
                          showBorder: any, label: any = (x: string) => x) {
  const result = new Array();
  var color_index = 0;
  var sorted_data = Array.from(data).sort((e1, e2) => parseInt(e1.substr(1)) - parseInt(e2.substr(1)));
  for (let dataset of sorted_data) {
    result.push({
      label: label(dataset),
      data: source,
      parsing: {
        xAxisKey: xAxisKey,
        yAxisKey: yAxisKey + dataset,
      },
      backgroundColor: colors[color_index % colors.length],
      borderColor: colors[color_index % colors.length],
      borderWidth: showBorder ? 2 : 0,
      })
    color_index += 1;
  }
  return result;
}

function updateChart(elementId: string, datasets: any[] ) {
  const ch = Chart.getChart(elementId)!;
  ch.data.datasets = datasets;
  ch.update();
}

function updateCopyButtonText(copyBtn: any, text: string) {
  copyBtn.text(text);
  setTimeout(function() {copyBtn.html("⇥")}, 2000);
}

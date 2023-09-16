import { Chart, registerables } from 'chart.js';
import {modal} from "./modal";
import {showAchievements} from "./app";
Chart.register(...registerables);


export function resolve_student(class_id: string, error_id: string, prompt: string) {
  modal.confirm(prompt, function(){
    $.ajax({
      type: 'DELETE',
      url: '/live_stats/class/' + class_id + '/error/' + error_id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      if (response.achievement) {
          showAchievements(response.achievement, true, "");
      } else {
          location.reload();
      }
    }).fail(function(err) {
        modal.notifyError(err.responseText);
    });
  });
}

export function InitLineChart(data: any[], labels: any[]){
  const ctx = document.getElementById("runsOverTime") as HTMLCanvasElement;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels.map(String),
      datasets: [{
        data: data,
        fill: false,
        pointBackgroundColor: function(context) {
                    var index = context.dataIndex;
                    var value = context.dataset.data[index];
                    if (value === 0) {
                    return 'red'
                    }
                    else if (value === 1){
                      return 'green'
                    }
                    return 'blue'
                },
        // backgroundColor: 'rgba(0, 0, 255, 1)',
        borderColor: 'rgba(0, 0, 255, 0.6)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
            y: {
              ticks: {
                callback: function(index) {
                  // Hide every 2nd tick label
                  if (index === 0) {
                    return 'Fail'
                  }
                  else if (index === 1){
                    return 'Success'
                  }
                  return ''
                },
              }
            },
        },
      plugins: {
        legend: {
            display: false
        }
      }
    }
  });
}

export function enable_level_class_overview(level: string) {
  if ($('#level_button_' + level).hasClass('gray-btn')) {
      $('#level_button_' + level).removeClass('gray-btn');
      $('#level_button_' + level).addClass('green-btn');
  } else {
      $('#level_button_' + level).removeClass('green-btn');
      $('#level_button_' + level).addClass('gray-btn');
  }
}

export function select_levels_class_overview(class_id: string) {
  let levels: (string | undefined)[] = [];
  $('.level-select-button').each(function() {
      if ($(this).hasClass("green-btn")) {
          levels.push(<string>$(this).val());
      }
  });

  $.ajax({
    type: 'POST',
    url: '/live_stats/class/' + class_id,
    data: JSON.stringify({
        levels: levels
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function () {
    location.reload();
  }).fail(function (err) {
    modal.notifyError(err.responseText);
  });
}

export function toggle_show_students_class_overview(adventure: string) {
  var adventure_panel = "div[id='adventure_panel_" + adventure + "']";
  if ($(adventure_panel).hasClass('hidden')) {
    $(adventure_panel).removeClass('hidden');
    $(adventure_panel).addClass('block');
  } else {
    $(adventure_panel).removeClass('block');
    $(adventure_panel).addClass('hidden');
  }
}

export function getRunsOverTime(data: any[], labels: any[]) {
  const chart = Chart.getChart("runsOverTime")!;
  chart.data.labels = labels.map(String);

  var datasets = [{
    data: data,
    fill: false,
    pointBackgroundColor: function(context:any) {
                var index = context.dataIndex;
                var value = context.dataset.data[index];
                if (value === 0) {
                return 'red'
                }
                else if (value === 1){
                  return 'green'
                }
                return 'blue'
            },
    // backgroundColor: 'rgba(0, 0, 255, 1)',
    borderColor: 'rgba(0, 0, 255, 0.6)',
    borderWidth: 1
  }]

  chart.data.datasets = datasets;
  chart.update();
}

export const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

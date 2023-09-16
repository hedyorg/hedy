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

export const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

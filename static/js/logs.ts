export const logs = {
  initialize: function () {
    // Hide irrelevant messages
    $("#logs-spinner").hide();
    $("#search-logs-failed-msg").hide();
    $("#search-logs-empty-msg").hide();

    const today = new Date().toISOString().split("T")[0];
    $("#logs-start-date").val(today + " 00:00:00");
    $("#logs-end-date").val(today + " 23:59:59");
  },

  searchProgramLogs: function (classId: string) {
    var raw_data = $("#logs-search-form").serializeArray();
    var payload: any = {};
    $.map(raw_data, function (n) {
      payload[n["name"]] = n["value"];
    });
    payload["class_id"] = classId;

    $("#search-logs-empty-msg").hide();
    $("#search-logs-failed-msg").hide();
    $("#logs-spinner").show();
    $("#logs-load-more").hide();
    $("#search-logs-button").prop("disabled", true);
    $("#search-logs-table tbody").html("");

    const self = this;
    $.ajax({
      type: "POST",
      url: "/logs/query",
      data: JSON.stringify(payload),
      contentType: "application/json; charset=utf-8",
    })
      .done(function (response) {
        if (response["query_status"] === "SUCCEEDED") {
          self.logsExecutionQueryId = response["query_execution_id"];
          self.logsNextToken = "";
          self.fetchProgramLogsResults();
        } else {
          $("#search-logs-failed-msg").show();
        }
      })
      .fail(function (error) {
        $("#search-logs-failed-msg").show();
        console.log(error);
      })
      .always(function () {
        $("#logs-spinner").hide();
        $("#search-logs-button").prop("disabled", false);
      });

    return false;
  },

  logsExecutionQueryId: "",
  logsNextToken: "",

  fetchProgramLogsResults: function () {
    $("#logs-spinner").show();
    $("#search-logs-empty-msg").hide();
    $("#logs-load-more").hide();

    const data = {
      query_execution_id: this.logsExecutionQueryId,
      next_token: this.logsNextToken ? this.logsNextToken : undefined,
    };

    const self = this;
    $.get("/logs/results", data)
      .done(function (response) {
        const $logsTable = $("#search-logs-table tbody");

        response.data.forEach((e: any) => {
          $logsTable.append(`<tr> \
          <td class="border px-2">${e.date}</td> \
          <td class="border px-2">${e.level}</td> \
          <td class="border px-2">${e.lang || ""}</td> \
          <td class="border px-2 break-words">${e.username || ""}</td> \
          <td class="border px-2 break-words">${e.exception || ""}</td> \
          <td class="border px-2 max-w-md"> \
            <button class="green-btn float-right top-2 right-2" onclick=hedyApp.logs.copyCode(this)>⇥</button> \
            <pre class="break-words">${e.code}</pre> \
          </td></tr>`);
        });

        if (response.data.length == 0) {
          $("#search-logs-empty-msg").show();
        }

        self.logsNextToken = response.next_token;
      })
      .fail(function (error) {
        console.log(error);
      })
      .always(function () {
        $("#logs-spinner").hide();
        if (self.logsNextToken) {
          $("#logs-load-more").show();
        }
      });

    return false;
  },

  copyCode: function (el: any) {
    const copyButton = $(el);
    if (navigator.clipboard === undefined) {
      updateCopyButtonText(copyButton, "Failed!");
    } else {
      navigator.clipboard.writeText(copyButton.next().text()).then(
        function () {
          updateCopyButtonText(copyButton, "Copied!");
        },
        function () {
          updateCopyButtonText(copyButton, "Failed!");
        },
      );
    }
    return false;
  },
};

function updateCopyButtonText(copyBtn: any, text: string) {
  copyBtn.text(text);
  setTimeout(function () {
    copyBtn.html("⇥");
  }, 2000);
}

$(function() {
  /**
   * Count newlines and also estimate how the text will be line wrapped
   */
  function estimateLineCount(s) {
    var ESTIMATED_LINE_LENGTH = 80;

    var lines = s.split('\n');
    var wrappedLines = lines.map(x => Math.floor(x.length / ESTIMATED_LINE_LENGTH));

    return sum(wrappedLines) + lines.length;
  }

  function sum(xs) {
    let ret = 0;
    for (const x of xs) {
      ret += x;
    }
    return ret;
  }


  function resizeArea(el) {
    var lines = Math.max(1, estimateLineCount($(el).val()));
    var targetHeight = lines * 25 + 4;

    // Allow for the case where the user made it bigger themselves
    if ($(el).height() < targetHeight) {
      $(el).css({ height: `${targetHeight}px` });
    }
  }

  $('textarea').each((i, el) => resizeArea(el)).keypress(e => {
    const target = $(e.target);
    if (!target.hasClass('touched')) {
      target.addClass('touched');
      recordChangeToForm(target.closest('form'));
    }
    resizeArea(target);
  });


  var FORM_MAP = new Map();

  function recordChangeToForm(form) {
    $('#download-bar').removeClass('hidden');
    var fileName = form.find('*[name=file]').val();

    var formData = FORM_MAP.get(fileName);
    console.log(formData);

    if (!formData) {
      var button = $('<button>').addClass('yellow-btn').addClass('mx-4').text(fileName).click(() => {
        form.submit();
      });

      $('#download-bar').append(button);

      formData = {
        button: button,
        changes: 0,
      }
      FORM_MAP.set(fileName, formData);
    }

    formData.changes += 1;
    formData.button.text(`${fileName} (${formData.changes})`);
  }
});

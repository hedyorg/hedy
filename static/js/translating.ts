/**
 * Count newlines and also estimate how the text will be line wrapped
 */
function estimateLineCount(s: string) {
  var ESTIMATED_LINE_LENGTH = 80;

  var lines = s.split('\n');
  var wrappedLines = lines.map(x => Math.floor(x.length / ESTIMATED_LINE_LENGTH));

  return sum(wrappedLines) + lines.length;
}

function sum(xs: number[]) {
  let ret = 0;
  for (const x of xs) {
    ret += x;
  }
  return ret;
}


function resizeArea(el: JQuery | HTMLElement) {
  var lines = Math.max(1, estimateLineCount($(el).val() as string));
  var targetHeight = lines * 25 + 4;

  // Allow for the case where the user made it bigger themselves
  if ($(el).height() as number < targetHeight) {
    $(el).css({ height: `${targetHeight}px` });
  }
}

var VISIBLE_TRANSLATIONS = true;
const TRANSLATIONS = $('.translated-input').filter(function(_, el) {
  return el.textContent !== null &&
         el.textContent.length > 0 &&
         $(el).parent().parent().find('.original-text')[0].textContent !== el.textContent
});

$('#show-hide-missing-translations').click(function() {
    if (VISIBLE_TRANSLATIONS) {
      TRANSLATIONS.each(function(_, el) {
        $(el).parent().parent().hide();
      });
      $('tr.bg-purple-200').hide();
      VISIBLE_TRANSLATIONS = false;
      $(this)[0].innerText = 'Show all translations';
    } else {
      TRANSLATIONS.each(function(_, el) {
        $(el).parent().parent().show();
      });
      $('tr.bg-purple-200').show();
      VISIBLE_TRANSLATIONS = true;
      $(this)[0].innerText = 'Show only missing translations';
    }
})


$('textarea').each((_i, el) => resizeArea(el)).on('input', e => {
  const target = $(e.target);
  if (!target.hasClass('touched')) {
    target.addClass('');
    // Todo: TB -> Temporary remove the 'touched' class as it changed ANY textarea on the website
    //  We have to make this a bit nicer that it only concerns the translating onces

    // Change the 'data-name="xxx"' attribute into an actual 'name="xxx"' attribute
    // so that the value is actually submitted via the form.
    target.attr('name', target.data('name'));

    recordChangeToForm(target.closest('form'));
  }

  resizeArea(target);
});


var FORM_MAP = new Map();

function recordChangeToForm(form: JQuery) {
  var fileName = form.data('file');
  var formData = FORM_MAP.get(fileName);

  if (!formData) {
    var button = $('button[data-file="' + fileName + '"]');
    formData = {
      button: button,
      changes: 0,
    }

    FORM_MAP.set(fileName, formData);
  }

  formData.changes += 1;
  formData.button.text(`${fileName} (${formData.changes})`);
}

$('button[data-file]').click(e => {
  var fileName = $(e.target).data('file');
  var form = $('form[data-file="' + fileName + '"]');
  form.submit();
});

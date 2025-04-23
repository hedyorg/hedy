import { modal } from './modal';
import { theKeywordLanguage } from "./app";
import { ClientMessages } from './client-messages';
import DOMPurify from 'dompurify'
import { HedyCodeMirrorEditorCreator } from './cm-editor';
import { CustomWindow } from './custom-window';
import { addCurlyBracesToCode, addCurlyBracesToKeyword } from './adventure';
import { autoSave } from './autosave';
import { HedySelect } from './custom-elements';
import { Chart } from 'chart.js';
import { setLoadingVisibility } from './loading';

declare const htmx: typeof import('./htmx');
declare let window: CustomWindow;
const editorCreator = new HedyCodeMirrorEditorCreator();

export function create_class(class_name_prompt: string) {
  modal.prompt (class_name_prompt, '', function (class_name) {
    $.ajax({
      type: 'POST',
      url: '/class',
      data: JSON.stringify({
        name: class_name
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      window.location.pathname = '/for-teachers/customize-class/' + response.id ;
    }).fail(function(err) {
      return modal.notifyError(err.responseText);
    });
  });
}

export function rename_class(id: string, class_name_prompt: string) {
    modal.prompt (class_name_prompt, '', function (class_name) {
        $.ajax({
          type: 'PUT',
          url: '/class/' + id,
          data: JSON.stringify({
            name: class_name
          }),
          contentType: 'application/json',
          dataType: 'json'
        }).done(function() {
          location.reload();
        }).fail(function(err) {
          return modal.notifyError(err.responseText);
        });
    });
}

export function duplicate_class(id: string, teacher_classes: string[], second_teacher_prompt: string, prompt: string, defaultValue: string = '') {
  if (teacher_classes && !defaultValue){
    modal.confirm(second_teacher_prompt, function () {
      apiDuplicateClass(id, prompt, true, defaultValue);
    }, function () {
      apiDuplicateClass(id, prompt, false, defaultValue);
    });
  } else {
    apiDuplicateClass(id, prompt, false, defaultValue);
  }
}

function apiDuplicateClass(id: string, prompt: string, second_teacher: boolean, defaultValue: string = '') {
    modal.prompt (prompt, defaultValue, function (class_name) {
    $.ajax({
      type: 'POST',
      url: '/duplicate_class',
      data: JSON.stringify({
        id: id,
        name: class_name,
        second_teacher: second_teacher,
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      if (response.second_teachers && second_teacher == true){
        for (const secondTeacher of response.second_teachers) {
          $.ajax({
            type: 'POST',
            url: '/invite-second-teacher',
            data: JSON.stringify({
              username: secondTeacher.username,
              class_id: response.id
            }),
            contentType: 'application/json',
            dataType: 'json'
            }).fail(function(err) {
                modal.notifyError(err.responseText);
            });
        }
      }
      location.reload();
    }).fail(function(err) {
      return modal.notifyError(err.responseText);
    });
  });
}

export function delete_class(id: string, prompt: string) {
  modal.confirm(prompt, function () {
    $.ajax({
      type: 'DELETE',
      url: '/class/' + id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function () {
      location.reload();
    }).fail(function (err) {
      modal.notifyError(err.responseText);
    });
  });
}

export function join_class(id: string, name: string) {
  $.ajax({
      type: 'POST',
      url: '/class/join',
      contentType: 'application/json',
      data: JSON.stringify({
        id: id,
        name: name
      }),
      dataType: 'json'
    }).done(function() {
      window.location.pathname = '/programs';
    }).fail(function(err) {
      if (err.status == 403) { //The user is not logged in -> ask if they want to
         return modal.confirm (err.responseText, function () {
            localStorage.setItem ('hedy-join', JSON.stringify ({id: id, name: name}));
            window.location.pathname = '/login';
         });
      } else {
          modal.notifyError(err.responseText || ClientMessages['Connection_error']);
      }
    });
}

export function remove_student_invite(username: string, class_id: string, prompt: string) {
  return modal.confirm (prompt, function () {
      $.ajax({
          type: 'POST',
          url: '/remove_student_invite',
          data: JSON.stringify({
              username: username,
              class_id: class_id
          }),
          contentType: 'application/json',
          dataType: 'json'
      }).done(function () {
          location.reload();
      }).fail(function (err) {
          return modal.notifyError(err.responseText);
      });
  });
}

export function remove_student(class_id: string, student_id: string, prompt: string) {
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'DELETE',
      url: '/class/' + class_id + '/student/' + student_id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function() {
      location.reload();
    }).fail(function(err) {
        modal.notifyError(err.responseText);
    });
  });
}

function get_formatted_content(content: string, levels: string[], language: string) {
  const parser = new DOMParser();
  const html = parser.parseFromString(content, 'text/html');
  let minLevel = 1;
  if (levels.length) {
    minLevel = Math.min(...levels.map((el) => Number(el)));
  }
  let snippets: string[] = [] ;
  let snippetsFormatted: string[] = [];
  let keywords: string[] = []
  let keywordsFormatted: string[] = []

  for (const tag of html.getElementsByTagName('code')) {
    if (tag.className === "language-python") {
      snippets.push(tag.innerText);
    } else {
      keywords.push(tag.innerText);
    }
  }

  for (const snippet of snippets) {
    snippetsFormatted.push(addCurlyBracesToCode(snippet, minLevel, language || 'en'));
  }

  for (const keyword of keywords) {
    keywordsFormatted.push(addCurlyBracesToKeyword(keyword))
  }

  let i = 0;
  let j = 0;
  for (const tag of html.getElementsByTagName('code')) {
    if (tag.className === "language-python") {
      tag.innerText = snippetsFormatted[i++]
    } else {
      tag.innerText = keywordsFormatted[j++]
    }
  }
  // We have to replace <br> for newlines, because the serializer swithces them around
  const formatted_content = html.getElementsByTagName('body')[0].outerHTML.replace(/<br>/g, '\n');
  return formatted_content
}

function update_db_adventure(adventure_id: string) {
  // Todo TB: It would be nice if we improve this with the formToJSON() function once #3077 is merged
  const adventure_name = $('#custom_adventure_name').val();
  const levels = (document.querySelector('#levels_dropdown') as HedySelect).selected
  const classes = (document.querySelector('#classes_dropdown') as HedySelect).selected
  const language = (document.querySelector('#languages_dropdown') as HedySelect).selected[0]
  if(levels.length === 0) {
    modal.notifyError(ClientMessages['one_level_error']);
    return;
  }
  const content = DOMPurify.sanitize(window.ckEditor.getData());
  const solutionExampleCode = DOMPurify.sanitize(window.ckSolutionEditor.getData());

  const formatted_content = get_formatted_content(content, levels, language);
  const formatted_solution_code = get_formatted_content(solutionExampleCode, levels, language);
  const agree_public = $('#agree_public').prop('checked');

  $.ajax({
    type: 'POST',
    url: '/for-teachers/customize-adventure',
    data: JSON.stringify({
      id: adventure_id,
      name: adventure_name,
      content: content,
      formatted_content: formatted_content,
      formatted_solution_code: formatted_solution_code,
      public: agree_public,
      language,
      classes,
      levels,
    }),
    contentType: 'application/json',
    dataType: 'json'
  }).done(function (response) {
    modal.notifySuccess(response.success);
  }).fail(function (err) {
    modal.notifyError(err.responseText);
  });
}

export function update_adventure(adventure_id: string, first_edit: boolean, prompt: string) {
  if (!first_edit) {
    modal.confirm (prompt, function () {
        update_db_adventure(adventure_id);
    });
   } else {
       update_db_adventure(adventure_id);
   }
}

function show_preview(content: string) {
    const name = $('#custom_adventure_name').val();
    if (typeof name !== 'string') { throw new Error(`Expected name to be string, got '${name}'`); }
    let levels: string[] = []
    document.querySelectorAll('#levels_dropdown > .option.selected').forEach((el) => {
      levels.push(el.getAttribute("data-value") as string)
    })
    if (typeof levels !== 'object') { throw new Error(`Expected level to be a list, got '${levels}'`); }

    let container = $('<div>');
    container.addClass('preview border border-black px-8 py-4 text-left rounded-lg bg-gray-200 text-black');
    container.css('white-space', 'pre-wrap');
    container.css('width', '40em');
    container.html(content);

    // We have to show the modal first before we can "find" the <pre> attributes and convert them to ace editors
    modal.preview(container, name);
    for (const preview of $('.preview pre').get()) {
        $(preview).addClass('text-lg rounded');
        const dir = $("body").attr("dir");
        const codeNode = preview.querySelector('code')
        let code: string;
        // In case it has a child <code> node
        if(codeNode) {
          codeNode.hidden = true
          code = codeNode.innerText
        } else {
          code = preview.textContent || "";
          preview.textContent = "";
        }
        const exampleEditor = editorCreator.initializeReadOnlyEditor(preview, dir);
        exampleEditor.contents = code.trimEnd();
        for (const level of levels) {
          exampleEditor.setHighlighterForLevel(parseInt(level, 10), theKeywordLanguage);
          // We only need to set a highlighter for a single level.
          break;
        }
    }
}

export function preview_adventure() {
    let content = DOMPurify.sanitize(<string>$('#custom_adventure_content').val());
    if (!content) {
      content = window.ckEditor.getData();
    }
    // We get the content, send it to the server to parse the keywords and then show dynamically
    $.ajax({
      type: 'POST',
      url: '/for-teachers/preview-adventure',
      data: JSON.stringify({
          code: content
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function (response) {
        show_preview(response.code);
    }).fail(function (err) {
      modal.notifyError(err.responseText);
    });
}

export function delete_adventure(adventure_id: string, prompt: string) {
  modal.confirm(prompt, function () {
    $.ajax({
      type: 'DELETE',
      url: '/for-teachers/customize-adventure/' + adventure_id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function () {
      window.location.href = '/for-teachers';
    }).fail(function (err) {
      modal.notifyError(err.responseText);
    });
  });
}

export function change_password_student(username: string, enter_password: string, password_prompt: string) {
    modal.prompt ( enter_password + " " + username + ":", '', function (password) {
        modal.confirm (password_prompt, function () {
            $.ajax({
              type: 'POST',
              url: '/auth/change_student_password',
              data: JSON.stringify({
                  username: username,
                  password: password
              }),
              contentType: 'application/json',
              dataType: 'json'
            }).done(function (response) {
              modal.notifySuccess(response.success);
            }).fail(function (err) {
              modal.notifyError(err.responseText);
            });
        });
    });
}

export function show_doc_section(section_key: string) {
  // Todo TB: We can improve this code as it is quite cumbersome (08-22)
  $(".section-button").each(function(){
       if ($(this).hasClass('blue-btn')) {
           $(this).removeClass("blue-btn");
           $(this).addClass("green-btn");
       }
   });
   if ($ ('#section-' + section_key).is (':visible')) {
       $("#button-" + section_key).removeClass("blue-btn");
       $("#button-" + section_key).addClass("green-btn");
       $ ('.section').hide ();
   } else {
     $("#button-" + section_key).removeClass("green-btn");
     $("#button-" + section_key).addClass("blue-btn");
     $('.section').hide();
     $ ('.common_mistakes_section').hide ();
     $('#section-' + section_key).toggle();
   }
}

//https://stackoverflow.com/questions/7196212/how-to-create-dictionary-and-add-key-value-pairs-dynamically?rq=1
export function save_customizations(class_id: string) {
    let levels: (string | undefined)[] = [];
    $('[id^=enable_level_]').each(function() {
        if ($(this).is(":checked")) {
            levels.push(<string>$(this).attr('level'));
        }
    });
    let other_settings: string[] = [];
    $('.other_settings_checkbox').each(function() {
        if ($(this).prop("checked")) {
            other_settings.push(<string>$(this).attr('id'));
        }
    });
    let level_thresholds: Record<string, string> = {};
    $('.threshold_settings_value').each(function() {
        if ($(this).val() != '') {
            level_thresholds[$(this).attr('id') as string] = $(this).val() as string;
        }
    });
    let opening_dates: Record<string, string> = {};
    $('[id^=opening_date_level_]').each(function() {
      opening_dates[$(this).attr('level') as string] = $(this).val() as string;
    });
    // Not sending the adventures because the adventures are automatically saved in the database
    $.ajax({
      type: 'POST',
      url: '/for-teachers/customize-class/' + class_id,
      data: JSON.stringify({
          levels: levels,
          opening_dates: opening_dates,
          other_settings: other_settings,
          level_thresholds: level_thresholds
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function (response) {
      modal.notifySuccess(response.success);
      $('#remove_customizations_button').removeClass('hidden');
      // Since the `sorted_adventures` section contains `quiz` and `parsons`
      // It needs to be synched with the updates that aren't done through HTMX
      // Therefore we trigger an input trigger, which in turn will call the
      // get-customization-level endpoint and remove or add those two adventures
      // if needed.
      const dropdown = document.getElementById("levels_dropdown");
      const input_trigger = new Event("input");
      dropdown?.dispatchEvent(input_trigger);  
    }).fail(function (err) {
      modal.notifyError(err.responseText);
    });
}

export function restore_customization_to_default(prompt: string) {
    modal.confirm (prompt, async function () {
      // We need to know the current level that is selected by the user
      // so we can know which level to draw in the template
      let active_level_id : string = $('[id^=level_]')[0].id;
      let active_level = active_level_id.split('_')[1]
      try {
        await htmx.ajax(
          'POST',
          `/for-teachers/restore-customizations?level=${active_level}`,
          '#adventure_dragger'
        )
        $('.other_settings_checkbox').prop('checked', false);
        // Remove the value from all input fields -> reset to text to show placeholder
        $('.opening_date_input').prop("type", "text")
                                .blur()
                                .val('')
                                .prop('disabled', false)
                                .attr('placeholder', ClientMessages.directly_available)
                                .each(function() {
                                      if($(this).hasClass('bg-green-300')) {
                                        $(this).removeClass('bg-green-300')
                                              .addClass('bg-gray-200')
                                      }
                                });

        $('[id^=enable_level_]').prop('checked', true);
        setLevelStateIndicator(active_level);
        modal.notifySuccess(ClientMessages.customization_deleted);
      } catch (error) {
        console.error(error);
      }
    });
}

export function enable_level(level: string) {
    if ($('#enable_level_' + level).is(':checked')) {
      $('#opening_date_level_' + level).prop('disabled', false)
                                      .attr('type', 'text')
                                      .attr("placeholder", ClientMessages.directly_available)
                                      .removeClass('bg-green-300')
                                      .addClass('bg-gray-200')
    } else {
      $('#opening_date_level_' + level).prop('disabled', true)
                                       .attr('type', 'text')
                                       .attr("placeholder", ClientMessages.disabled)
                                       .val('');
    }

    if ($('#level_' + level).is(':visible')) {
      setLevelStateIndicator(level);
    }
}

export function setDateLevelInputColor(level: string) {
  var date_string : string = $('#opening_date_level_' + level).val() as string;
  var input_date = new Date(date_string);
  var today_date = new Date();
  if (input_date > today_date) {
    $('#opening_date_level_' + level).removeClass('bg-gray-200')
                                     .addClass('bg-green-300')

  } else {
    $('#opening_date_level_' + level).removeClass('bg-green-300')
                                     .addClass('bg-gray-200')
  }

  if ($('#level_' +  level).is(':visible')) {
    setLevelStateIndicator(level);
  }
}

export function add_account_placeholder() {
  // Get the hidden row template
  const rowTemplate = $('#account_row_unique').clone();
  rowTemplate.removeClass('hidden');
  rowTemplate.attr('id', "");

  // Function to update data-cy attributes
  function updateDataCyAttributes(row: JQuery<HTMLElement>, index: number) {
      row.find('[data-cy]').each(function() {
          const currentCy = $(this).attr('data-cy');
          if (currentCy) {
              const newCy = currentCy.replace(/_\d+$/, `_${index}`);
              $(this).attr('data-cy', newCy);
          }
      });
  }

  // Get the current number of rows
  const existingRowsCount = $('.account_row').length;

  // Append 5 rows at once
  for (let x = 0; x < 5; x++) {
      const newRow = rowTemplate.clone();
      updateDataCyAttributes(newRow, existingRowsCount + x + 1);
      newRow.appendTo("#account_rows_container");
  }
}

export function toggleAutoGeneratePasswords() {
    if ($('#passwords_toggle').is(':checked')) {
        $('#passwords_toggle_checked_text').show();
        $('#passwords_toggle_unchecked_text').hide();
        $('#usernames_title').show();
        $('#passwords_title').hide();
        $('#usernames_desc').show();
        $('#passwords_desc').hide();
    } else {
        $('#passwords_toggle_checked_text').hide();
        $('#passwords_toggle_unchecked_text').show();
        $('#usernames_title').hide();
        $('#passwords_title').show();
        $('#usernames_desc').hide();
        $('#passwords_desc').show();
    }
}

export function printAccounts(title: string) {
    var table = document.getElementById("accounts_table");
    let newWindow = window.open("")!;
    const css = `
    <style>
      h1 {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", "Courier New", monospace;
        margin-left: 20px;
        color: rgb(44 82 130);
      }

      #accounts_table {
        border-collapse: collapse;
      }

      #accounts_table td, th {
        padding-left: 1.25rem;
        padding-right: 1.25rem;
        padding-top: 1.25rem;
        padding-bottom: 1.25rem;
        font-size: 1.5rem;
        border: 1px solid gray;
        color: rgb(44 82 130);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", "Courier New", monospace;
        text-align: center;
      }
    </style>`;
    newWindow.document.write(`
        <div style="display: flex; margin-bottom: 20px;">
          <img src="/images/hero-graphic/hero-graphic-empty.png" height="100">
          <h1>${title}</h1>
        </div>
    `);
    newWindow.document.write(table?.outerHTML + css);
    newWindow.print();
    newWindow.close();
}

export function copyAccountsToClipboard(prompt: string) {
    const selection = window.getSelection();
    const table = document.getElementById("accounts_table");
    if (selection && table) {
        var range = document.createRange();
        selection.empty();
        range.selectNode(table);
        selection.addRange(range)
        document.execCommand('copy')
        selection.empty();

        modal.notifySuccess(prompt);
    }
}

export function createAccounts(prompt: string) {
    const accounts = $('#accounts_input').val() as string;
    const numberOfAccounts = accounts.split('\n').filter(l => l.trim()).length;
    const updatedPrompt = prompt.replace('{number_of_accounts}', numberOfAccounts.toString());

    modal.confirm (updatedPrompt, function () {
        const className = $('#classes').val() as string;
        const generatePasswords = $('#passwords_toggle').is(":checked") as boolean;

        setLoadingVisibility(true);

        $.ajax({
            type: 'POST',
            url: '/for-teachers/create-accounts',
            data: JSON.stringify({
                class: className,
                generate_passwords: generatePasswords,
                accounts: accounts,
            }),
            contentType: 'application/json'
        }).done(function (response) {

            setLoadingVisibility(false);
            $('#accounts_form').hide();
            $('#create_accounts_title').hide();

            $('#accounts_results').show();
            $('#accounts_results_title').show();
            $("tr:has(td)").remove();
            const accountsHtml = createHtmlForAccountsTable(response['accounts']);
            $("#accounts_table").append(accountsHtml);

        }).fail(function (err) {
            setLoadingVisibility(false);

            try {
                // This endpoint has to return error info to direct the user how to fix it
                const parsed = JSON.parse(err.responseText);
                if (parsed.error) {
                    // Note the notification should not be closed automatically
                    // because it contains feedback about broken records
                    modal.notifyError(parsed.error, 0);
                    return;
                }
            } catch { }
            // If the error is simple text (e.g. 'request invalid'), display it to the user
            modal.notifyError(err.responseText);
        });
    });
}

function createHtmlForAccountsTable(accounts: Array<any>) {
    let result = ""
    for (let [index, account] of accounts.entries()) {
        result += `
          <tr class="${ index%2 ? 'bg-white' : 'bg-gray-200'} font-mono">
            <td class="text-center px-4 py-2">hedy.org</td>
            <td class="text-center px-4 py-2">${account['username']}</td>
            <td class="text-center px-4 py-2">${account['password']}</td>
          </tr>`;
    }
    return result;
}

function onCreateAccountsPaste() {
    // When copying data from Excel, the default column separator is a tab (\t).
    // So, when text is pasted in the textarea for creating accounts, so we replace tabs with semicolons
    const accountsInput = $('#accounts_input').val() as string;
    const newAccounts = accountsInput.replace(/\t/g, ';');
    $('#accounts_input').val(newAccounts);
}

export function copy_join_link(link: string, success: string) {
    // https://qawithexperts.com/article/javascript/creating-copy-to-clipboard-using-javascript-or-jquery/364
    var sampleTextarea = document.createElement("textarea");
    document.body.appendChild(sampleTextarea);
    sampleTextarea.value = link;
    sampleTextarea.select();
    document.execCommand("copy");
    document.body.removeChild(sampleTextarea);
    modal.notifySuccess(success);
}

export interface InitializeTeacherPageOptions {
  readonly page: 'for-teachers';

  /**
   * Whether to show the dialog box on page load
   */
  readonly welcome_teacher?: boolean;
}

export function initializeTeacherPage(options: InitializeTeacherPageOptions) {
  if (options.welcome_teacher) {
    modal.notifySuccess(ClientMessages.teacher_welcome, 30_000);
  }
}

function setLevelStateIndicator(level: string) {
  $('[id^=state_]').addClass('hidden');

  if ($('#opening_date_level_' + level).is(':disabled')) {
    $('#state_disabled').removeClass('hidden');
  } else if($('#opening_date_level_' + level).val() === ''){
    $('#state_accessible').removeClass('hidden');
  } else {
    var date_string : string = $('#opening_date_level_' + level).val() as string;
    var input_date = new Date(date_string);
    var today_date = new Date();
    if (input_date > today_date) {
      $('#opening_date').text(date_string);
      $('#state_future').removeClass('hidden');
    } else {
      $('#state_accessible').removeClass('hidden');
    }
  }
}

export interface InitializeCreateAccountsPageOptions {
  readonly page: 'create-accounts';
}

export function initializeCreateAccountsPage(_options: InitializeCreateAccountsPageOptions) {
  const accountsInput = document.getElementById("accounts_input") as HTMLFormElement;
  // Apparently we need the setTimeout to get the whole text of the textarea because the event provides only
  // the text that was in the clipboard which does not work in if the user is appending text and not replacing it.
  accountsInput?.addEventListener('paste', function() {
      window.setTimeout(onCreateAccountsPaste, 100);
  });
}

export interface InitializeCustomizeClassPageOptions {
  readonly page: 'customize-class';
  readonly class_id: string;
}

export function initializeCustomizeClassPage(options: InitializeCustomizeClassPageOptions) {
  $(document).ready(function(){
      $('#back_to_class').on('click', () => {
        window.location.href = `/for-teachers/class/${options.class_id}`;
      });

      $('[id^=opening_date_level_]').each(function() {
        setDateLevelInputColor($(this).attr('level')!);
      })

      $('#levels_dropdown').on('change', function(){
          var level = $(this).val() as string;
          setLevelStateIndicator(level);
      });

      // Autosave customize class page
      // the third argument is used to trigger a GET request on the specified element
      // if the trigger (input in this case) is changed.
      autoSave("customize_class");
  });
}

/**
 * These will be copied into global variables, because that's how this file works...
 */
export interface InitializeClassOverviewPageOptions {
  readonly page: 'class-overview';
  readonly graph_students: student[];
  readonly level: number;
}

export function initializeClassOverviewPage(_options: InitializeClassOverviewPageOptions) {
  $('.attribute').change(function () {
    const attribute = $(this).attr('id');
    if (!(this as HTMLInputElement).checked) {
      $('#' + attribute + '_header').hide();
      $('.' + attribute + '_cell').hide();
    } else {
      $('#' + attribute + '_header').show();
      $('.' + attribute + '_cell').show();
    }
  });

  initializeGraph()
  // An ugly hack, but if someone goes back trhough the page, the cache
  // causes the old version of the page to be shown
  // So we hard reload it
  window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted ||
                           ( typeof window.performance != "undefined" &&
                                window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      window.location.href = window.location.href
    }
  });
}

interface InitializeGraphOptions {
  readonly graph_students: student[];
  readonly level: number
}

interface student {
  adventures_tried: number,
  number_of_errors: number,
  successful_runs: number,
  username: string,
}

interface dataPoint {
  x: number,
  y: number,
  r: number,
  successful_runs: number,
  name: string
}
const MAX_BUBBLE_SIZE = 62;
const MIN_BUBBLE_SIZE = 12;

export function initializeGraph() {
  const graphElement = document.getElementById('adventure_bubble') as HTMLCanvasElement
  if (graphElement === undefined || graphElement === null) return;
  const graphData: InitializeGraphOptions = JSON.parse(graphElement.dataset['graph'] || '') ;
  let min = Infinity;
  let max = 0;
  const students = graphData.graph_students
  for (const student of students) {
    if (student.successful_runs < min) {
      min = student.successful_runs
    } else if (student.successful_runs > max) {
      max = student.successful_runs
    }
  }
  if (max == 0) {
    max = 12
  }
  let data: dataPoint[] = students.map((student: student) => {
  const radius  = (student.successful_runs - min) * (MAX_BUBBLE_SIZE - MIN_BUBBLE_SIZE) / (max - min) + MIN_BUBBLE_SIZE
    return {
      x: student.adventures_tried,
      y: student.number_of_errors,
      r: radius,
      successful_runs: student.successful_runs,
      name: student.username
    }
  });
  new Chart(
    graphElement,
    {
      type: 'bubble',
      data: {
        datasets: [
          {
            backgroundColor: '#c9dded',
            borderColor: '#35a4ff',
            data: data,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        onHover: (event, chartElement) => {
          //@ts-ignore
          event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default'
        },
        interaction: {
          mode: 'point'
        },
        onClick: (_e, activePoints, chart) => {
          if (activePoints.length === 0) return;
          const item: dataPoint = chart.data.datasets[0].data[activePoints[0].index] as dataPoint
          for(const point of activePoints) {
            console.log(chart.data.datasets[0].data[point.index])
          }
          document.getElementById('programs_container')?.classList.remove('hidden')
          htmx.ajax(
            'GET',
            `/for-teachers/get_student_programs/${item.name}`,
            '#programs_container'
          )
        },
        scales: {
          x: {
            title: {
              display: true,
              text: ClientMessages['adventures_tried'],
              font: {
                size: 15
              },
            },
            min: 0
          },
          y: {
            title: {
              display: true,
              text: ClientMessages['errors'],
              font: {
                size: 15
              }
            },
            suggestedMin: -0.3,
            suggestedMax: 1
          }
        },
        plugins: {
          title: {
            display: true,
            text: ClientMessages['graph_title'].replace('{level}', graphData.level.toString()),
            font: {
              size: 19
            }
          },
          legend: {
            display: false
          },
          tooltip: {
            displayColors: false,
            callbacks: {
              title: (tooltipItems) => {
                // A single point can have 2 data points associated.
                const names = tooltipItems.map((currentValue) => {
                  const item: dataPoint = currentValue.dataset.data[currentValue.dataIndex] as dataPoint
                  return item.name
                })
                return names.join(', ')
              },
              label: (tooltipItem) => {
                const item: dataPoint = tooltipItem.dataset.data[tooltipItem.dataIndex] as dataPoint
                return [
                  ClientMessages['adventures_completed'].replace('{number_of_adventures}', item.x.toString()),
                  ClientMessages['number_of_errors'].replace('{number_of_errors}', item.y.toString()),
                  ClientMessages['successful_runs'].replace('{successful_runs}', item.successful_runs.toString())
                ]
              }
            }
          }
        }
      },
    }
  );
}

export function invite_support_teacher(requester: string) {
  modal.prompt(`Invite a teacher to support ${requester}.`, '', function (username) {
    $.ajax({
        type: 'POST',
        url: "/super-teacher/invite-support",
        data: JSON.stringify({
          sourceUser: requester,
          targetUser: username,
        }),
        contentType: 'application/json',
        dataType: 'json'
    }).done(function() {
        location.reload();
    }).fail(function(err) {
        modal.notifyError(err.responseText);
    });
  });
}

export function invite_to_class(class_id: string, prompt: string, type: "student" | "second_teacher", is_second_teacher: boolean = false) {
  const input = document.getElementById('modal_search_input')
  const vals = {class_id, 'user_type': type}
  input?.setAttribute('hx-vals', JSON.stringify(vals))
  modal.search(prompt, send_invitations, [type, is_second_teacher], ClientMessages['invite']);
}

export function add_user_to_invite_list(username: string, button: HTMLButtonElement) {
  button.closest('li')?.remove() // We remove the user from the list
  const userList = document.getElementById('users_to_invite')
  for (const userLi of userList?.querySelectorAll('li') || []) {
    const p = userLi.querySelector('p')
    if (p?.textContent?.trim() === username) {
      return
    }
  }
  const template = document.querySelector('#user_list_template') as HTMLTemplateElement
  const clone = template.content.cloneNode(true) as HTMLElement
  let close = clone.querySelector('.close');  
  close?.addEventListener('click', () => {   
    close?.parentElement?.remove()
  })
  let p = clone.querySelector('p[class^="details"]')!
  p.textContent = username
  let input = clone.querySelector('input')!
  input.value = username
  userList?.appendChild(clone)
}

export async function send_invitations(invite_as: string = "student", is_second_teacher: boolean = false) {
  const li = document.querySelectorAll('#users_to_invite > li')
  let list = []
  for (const userLi of li) {
    list.push(userLi.textContent?.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim())
  }
  const url = new URL(window.location.href)
  const class_id = url.pathname.split('/for-teachers/class/')[1]
  htmx.ajax(
    'POST', "/invite", { values: { "class_id": class_id, "is_second_teacher": is_second_teacher, "invite_as": invite_as, "usernames": list }, target: "#invite_block" }
  ).then(() => {
    modal.notifySuccess(ClientMessages['invitations_sent'])
  })
}
import { modal } from './modal';
import {getHighlighter, showAchievements, turnIntoAceEditor} from "./app";

import DOMPurify from 'dompurify'

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
      if (response.achievement) {
        showAchievements(response.achievement, false, '/for-teachers/customize-class/' + response.id);
      } else {
        window.location.pathname = '/for-teachers/customize-class/' + response.id ;
      }
    }).fail(function(err) {
      return modal.alert(err.responseText, 3000, true);
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
        }).done(function(response) {
          if (response.achievement) {
            showAchievements(response.achievement, true, "");
          } else {
            location.reload();
          }
        }).fail(function(err) {
          return modal.alert(err.responseText, 3000, true);
        });
    });
}

export function delete_class(id: string, prompt: string) {
  modal.confirm (prompt, function () {
    $.ajax({
      type: 'DELETE',
      url: '/class/' + id,
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      if (response.achievement) {
        showAchievements(response.achievement, false, '/for-teachers');
      } else {
        window.location.pathname = '/for-teachers';
      }
    }).fail(function(err) {
      modal.alert(err.responseText, 3000, true);
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
    }).done(function(response) {
      if (response.achievement) {
          showAchievements(response.achievement, false, '/programs');
      } else {
          window.location.pathname = '/programs';
      }
    }).fail(function(err) {
      if (err.status == 403) { //The user is not logged in -> ask if they want to
         return modal.confirm (err.responseText, function () {
            localStorage.setItem ('hedy-join', JSON.stringify ({id: id, name: name}));
            window.location.pathname = '/login';
         });
      } else {
          modal.alert(ErrorMessages['Connection_error'], 3000, true);
      }
    });
}

export function invite_student(class_id: string, prompt: string) {
    modal.prompt (prompt, '', function (username) {
      $.ajax({
          type: 'POST',
          url: '/invite_student',
          data: JSON.stringify({
            username: username,
            class_id: class_id
          }),
          contentType: 'application/json',
          dataType: 'json'
      }).done(function() {
          location.reload();
      }).fail(function(err) {
          modal.alert(err.responseText, 3000, true);
      });
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
          return modal.alert(err.responseText, 3000, true);
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
    }).done(function(response) {
      if (response.achievement) {
          showAchievements(response.achievement, true, "");
      } else {
          location.reload();
      }
    }).fail(function(err) {
        modal.alert(err.responseText, 3000, true);
    });
  });
}

export function create_adventure(prompt: string) {
    modal.prompt (prompt, '', function (adventure_name) {
        $.ajax({
          type: 'POST',
          url: '/for-teachers/create_adventure',
          data: JSON.stringify({
            name: adventure_name
          }),
          contentType: 'application/json',
          dataType: 'json'
        }).done(function(response) {
          window.location.pathname = '/for-teachers/customize-adventure/' + response.id ;
        }).fail(function(err) {
          return modal.alert(err.responseText, 3000, true);
        });
    });
}

function update_db_adventure(adventure_id: string) {
   const adventure_name = $('#custom_adventure_name').val();
   const level = $('#custom_adventure_level').val();
   const content = DOMPurify.sanitize(<string>$('#custom_adventure_content').val());
   const agree_public = $('#agree_public').prop('checked');

    $.ajax({
      type: 'POST',
      url: '/for-teachers/customize-adventure',
      data: JSON.stringify({
        id: adventure_id,
        name: adventure_name,
        level: level,
        content: content,
        public: agree_public
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function(response) {
      modal.alert (response.success, 3000, false);
    }).fail(function(err) {
      modal.alert(err.responseText, 3000, true);
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

export function preview_adventure() {
    let content = DOMPurify.sanitize(<string>$('#custom_adventure_content').val());
    const name = <string>$('#custom_adventure_name').val();
    const level = <string>$('#custom_adventure_level').val();
    let container = $('<div>');
    container.addClass('preview border border-black px-8 py-4 text-left rounded-lg bg-gray-200 text-black');
    container.css('white-space', 'pre-wrap');
    container.css('width', '40em');
    container.html(content);

    // We have to show the modal first before we can "find" the <pre> attributes and convert them to ace editors
    modal.preview(container, name);
    for (const preview of $('.preview pre').get()) {
        $(preview).addClass('text-lg rounded');
        const exampleEditor = turnIntoAceEditor(preview, true)
        exampleEditor.setOptions({ maxLines: Infinity });
        exampleEditor.setOptions({ minLines: 2 });
        exampleEditor.setValue(exampleEditor.getValue().replace(/\n+$/, ''), -1);
        const mode = getHighlighter(level);
        exampleEditor.session.setMode(mode);
    }
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
            modal.alert(err.responseText, 3000, true);
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
              modal.alert(response.success, 3000, false);
            }).fail(function (err) {
              modal.alert(err.responseText, 3000, true);
            });
        });
    });
}

export function show_doc_section(section_key: string) {
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
     $ ('.common-mistakes-section').hide ();
     $('#section-' + section_key).toggle();
   }
   // Loop-index -1 doesn't exist -> automatically hide all "common mistakes" sections
   show_common_mistakes("-1");
}

export function show_common_mistakes(section_key: string) {
    $(".common-mistakes-button").each(function(){
       if ($(this).hasClass('blue-btn')) {
           $(this).removeClass("blue-btn");
           $(this).addClass("green-btn");
       }
   });
   if ($ ('#common_mistakes-' + section_key).is (':visible')) {
       $("#cm-button-" + section_key).removeClass("blue-btn");
       $("#cm-button-" + section_key).addClass("green-btn");
       $ ('.common-mistakes-section').hide ();
   } else {
     $("#cm-button-" + section_key).removeClass("green-btn");
     $("#cm-button-" + section_key).addClass("blue-btn");
     $('.common-mistakes-section').hide();
     $('#common_mistakes-' + section_key).toggle();
   }
}

//https://stackoverflow.com/questions/7196212/how-to-create-dictionary-and-add-key-value-pairs-dynamically?rq=1
export function save_customizations(class_id: string) {
    let levels: (string | undefined)[] = [];
    $('.level-select-button').each(function() {
        if ($(this).hasClass("green-btn")) {
            levels.push(<string>$(this).val());
        }
    });
    let adventures = {};
    $('.adventure_keys').each(function() {
        const name = <string>$(this).attr('adventure');
        // @ts-ignore
        adventures[name] = [];
    });
    $('.adventure_level_input').each(function() {
        const name = <string>$(this).attr('adventure');
        // @ts-ignore
        let current_list = adventures[name];
        if ($(this).prop("checked")) {
            current_list.push(<string>$(this).attr('level'));
            // @ts-ignore
            adventures[name] = current_list;
        }
    });
    let teacher_adventures: string[] = [];
    $('.teacher_adventures_checkbox').each(function() {
        if ($(this).prop("checked")) {
            teacher_adventures.push(<string>$(this).attr('id'));
        }
    });
    let other_settings: string[] = [];
    $('.other_settings_checkbox').each(function() {
        if ($(this).prop("checked")) {
            other_settings.push(<string>$(this).attr('id'));
        }
    });
    let opening_dates = {};
    $('.opening_date_container').each(function() {
        if ($(this).is(":visible")) {
            $(this).find(':input').each(function () {
                // @ts-ignore
                opening_dates[<string>$(this).attr('level')] = $(this).val();
            });
        }
    });
    $.ajax({
      type: 'POST',
      url: '/for-teachers/customize-class/' + class_id,
      data: JSON.stringify({
          levels: levels,
          opening_dates: opening_dates,
          adventures: adventures,
          teacher_adventures: teacher_adventures,
          other_settings: other_settings
      }),
      contentType: 'application/json',
      dataType: 'json'
    }).done(function (response) {
      modal.alert(response.success, 3000, false);
      $('#remove_customizations_button').removeClass('hidden');
    }).fail(function (err) {
      modal.alert(err.responseText, 3000, true);
    });
}

export function remove_customizations(class_id: string, prompt: string) {
    modal.confirm (prompt, function () {
        $.ajax({
            type: 'DELETE',
            url: '/for-teachers/customize-class/' + class_id,
            contentType: 'application/json',
            dataType: 'json'
        }).done(function (response) {
            $('#remove_customizations_button').addClass('hidden');
            $('.adventure_level_input').show();
            $('.adventure_level_input').prop('checked', true);
            $('.teacher_adventures_checkbox').prop('checked', false);
            $('.other_settings_checkbox').prop('checked', false);
            $('.level-select-button').removeClass('blue-btn');
            $('.level-select-button').addClass('green-btn');
            $('.opening_date_container').removeClass('hidden');

            // Remove the value from all input fields -> reset to text to show placeholder
            $('.opening_date_input').prop("type", "text");
            $('.opening_date_input').blur();
            $('.opening_date_input').val('');
            modal.alert(response.success, 3000, false);
        }).fail(function (err) {
            modal.alert(err.responseText, 3000, true);
        });
    });
}

export function select_all_levels_adventure(adventure_name: string) {
    let first_input = true;
    let checked = true;
    $('.adventure_level_input').each(function() {
        const name = <string>$(this).attr('adventure');
        if (name == adventure_name && $(this).is(":visible")) {
            if (first_input) {
                checked = $(this).prop("checked");
                first_input = false;
            }
            $(this).prop("checked", !checked);
        }
    });
}

export function select_all_level_adventures(level: string) {
    // It is not selected yet -> select all and change color
    if ($('#level_button_' + level).hasClass('blue-btn')) {
        $('.adventure_level_' + level).each(function(){
            $(this).removeClass('hidden');
            if ($(this).is(':enabled')) {
                $(this).prop("checked", true);
            }
        });
        $('#level_button_' + level).removeClass('blue-btn');
        $('#level_button_' + level).addClass('green-btn');

        // We also have to add this level to the "Opening dates" section
        $('#opening_date_level_' + level).removeClass('hidden');
        $('#opening_date_level_' + level).find('input').val('');
        $('#opening_date_level_' + level).find('input').prop({type:"text"});
    } else {
        $('.adventure_level_' + level).each(function () {
            $(this).prop("checked", false);
            $(this).addClass('hidden');
        });
        $('#level_button_' + level).removeClass('green-btn');
        $('#level_button_' + level).addClass('blue-btn');

        // We also have to remove this level from the "Opening dates" section
        $('#opening_date_level_' + level).addClass('hidden');
    }
}

export function add_account_placeholder() {
    let row = $("#account_row_unique").clone();
    row.removeClass('hidden');
    row.attr('id', "");
    // Set all inputs expect class to required
    row.find(':input').each(function() {
       if ($(this).prop('id') != 'classes') {
           $(this).prop('required', true);
       }
    });
    row.appendTo("#account_rows_container");
}

export function create_accounts(prompt: string) {
    modal.confirm (prompt, function () {
        $('#account_rows_container').find(':input').each(function () {
            $(this).removeClass('border-2 border-red-500');
        });
        let accounts: {}[] = [];
        $('.account_row').each(function () {
            if ($(this).is(':visible')) { //We want to skip the hidden first "copy" row
                let account = {};
                $(this).find(':input').each(function () {
                    // @ts-ignore -> Not sure why TypeScript has issues, this should be valid
                    account[$(this).attr("name")] = $(this).val();
                });
                accounts.push(account);
            }
        });
        $.ajax({
            type: 'POST',
            url: '/for-teachers/create-accounts',
            data: JSON.stringify({
                accounts: accounts
            }),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function (response) {
            if (response.error) {
                modal.alert(response.error, 3000, true);
                $('#account_rows_container').find(':input').each(function () {
                    if ($(this).val() == response.value) {
                        $(this).addClass('border-2 border-red-500');
                    }
                });
                return;
            } else {
                modal.alert(response.success, 3000, false);
                if ($('#download_credentials_checkbox').prop('checked')) {
                    download_login_credentials(accounts);
                }
                $('#account_rows_container').find(':input').each(function () {
                   $(this).val("");
                });
                $('#download_credentials_checkbox').prop("checked", false);
            }
        }).fail(function (err) {
            modal.alert(err.responseText, 3000, true);
        });
    });
}

function download_login_credentials(accounts: any) {
    // https://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Username, Password" + "\r\n";

    accounts.forEach(function(account: any) {
        let row = account.username + "," + account.password;
        csvContent += row + "\r\n";
    });

    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "accounts.csv");
    document.body.appendChild(link); // Required for Firefox

    link.click();
}
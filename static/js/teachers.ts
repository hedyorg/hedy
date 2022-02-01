import { modal, error } from './modal';
import { auth } from './auth';
import {showAchievements} from "./app";

export function create_class() {
  modal.prompt (auth.texts['class_name_prompt'], '', function (class_name) {
    if (!class_name) {
      modal.alert(auth.texts['class_name_empty'], 2000, true);
      return;
    }
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
      if (err.responseText == "duplicate") {
        modal.alert(auth.texts['class_name_duplicate'], 2000, true);
        return;
      }
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
  });
}

export function rename_class(id: string) {
  modal.prompt (auth.texts['class_name_prompt'], '', function (class_name) {
    if (!class_name) {
      modal.alert(auth.texts['class_name_empty'], 2000, true);
      return;
    }
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
      if (err.responseText == "duplicate") {
        modal.alert(auth.texts['class_name_duplicate'], 2000, true);
        return;
      }
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
  });
}

export function delete_class(id: string) {
  modal.confirm (auth.texts['delete_class_prompt'], function () {

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
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
  });
}

export function join_class(id: string, name: string) {
  // If there's no session but we want to join the class, we store the program data in localStorage and redirect to /login.
  if (! auth.profile) {
    return modal.confirm (auth.texts['join_prompt'], function () {
      localStorage.setItem ('hedy-join', JSON.stringify ({id: id, name: name}));
      window.location.pathname = '/login';
      return;
    });
  }

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
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
}

export function invite_student(class_id: string) {
  modal.prompt (auth.texts['invite_prompt'], '', function (username) {
      if (!username) {
          return modal.alert("This value is empty");
      }
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
          return modal.alert(err.responseText, 3000, true);
      });
  });
}

export function remove_student_invite(username: string, class_id: string) {
  return modal.confirm (auth.texts['delete_invite_prompt'], function () {
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

export function remove_student(class_id: string, student_id: string, self_removal: boolean) {
  let confirm_text;
  if (self_removal) {
    confirm_text = auth.texts['self_removal_prompt'];
  } else {
    confirm_text = auth.texts['remove_student_prompt'];
  }
  modal.confirm (confirm_text, function () {
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
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
  });
}

export function change_password_student(username: string) {
    modal.prompt ( auth.texts['enter_password'] + " " + username + ":", '', function (password) {
        modal.confirm (auth.texts['password_change_prompt'], function () {
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
     $('#section-' + section_key).toggle();
   }
}

export function save_level_settings(id: string, level: number) {
     let selected_adventures: (string | null)[] = [];
     $('#adventures_overview li').each(function() {
         if ($(this).is(':visible') && $(this).find(':input').prop('checked')) {
             selected_adventures.push(this.getAttribute('id'));
         }
     });

     const hide_level = !!$(`#hide_level${level}`).prop('checked');
     const hide_next_level = !!$(`#hide_level${level - 1}`).prop('checked');
     const example_programs = !!$(`#example_programs${level}`).prop('checked');
     const hide_prev_level = !!$(`#hide_level${level - 1}`).prop('checked');

     $.ajax({
       type: 'PUT',
       url: '/customize-class/' + id,
       data: JSON.stringify({
         adventures: selected_adventures,
         example_programs: example_programs,
         hide_level: hide_level,
         hide_prev_level: hide_prev_level,
         hide_next_level: hide_next_level,
         level: level
       }),
       contentType: 'application/json',
       dataType: 'json'
     }).done(function(response) {
       if (response.achievement) {
         showAchievements(response.achievement, true, "");
       } else {
         location.reload ();
       }
     }).fail(function(err) {
       console.error(err);
       error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
     });
 }

export function reset_level_preferences(level: number) {
    $('#adventures_overview li').each(function() {
     if ($(this).is(':visible')) {
         $(this).find(':input').prop("checked", true);
     }
    });
    $('#example_programs' + level).prop("checked", true);
    $('#hide_level' + level).prop("checked", false);
}

export function add_account_placeholders() {
    const amount = <number>$('#add_placeholders').val();
    for (let i = 0; i < amount; i++) {
        let row = $("#account_row_unique").clone();
        row.removeClass('hidden');
        row.attr('id', "");
        row.appendTo("#account_rows_container");
    }
}

export function create_accounts() {
    modal.confirm ("Are you sure you want to create these accounts?", function () {
        $('#account_rows_container').find(':input').each(function () {
            $(this).removeClass('border-2 border-red-500');
        });
        let accounts: {}[] = [];
        $('.account_row').each(function () {
            if ($(this).is(':visible')) { //We want to skip the hidden first "copy" row
                let account = {};
                $(this).find(':input').each(function () {
                    // @ts-ignore
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
                $('#account_rows_container').find(':input').each(function () {
                   $(this).val("");
                });
            }
        }).fail(function (err) {
            modal.alert(err.responseText, 3000, true);
        });
    });
}
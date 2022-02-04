import { modal, error } from './modal';
import { auth } from './auth';
import {getHighlighter, showAchievements, turnIntoAceEditor} from "./app";

import DOMPurify from 'dompurify'

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
          return modal.alert(auth.texts['username_empty']);
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
        modal.alert(err.responseText, 3000, true);
    });
  });
}

export function create_adventure() {
    modal.prompt (auth.texts['adventure_prompt'], '', function (adventure_name) {
        adventure_name = adventure_name.trim();
        console.log("test");
        if (!adventure_name) {
          modal.alert(auth.texts['adventure_empty'], 3000, true);
          return;
    }
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

export function update_adventure(adventure_id: string, first_edit: boolean) {
   if (!first_edit) {
    modal.confirm (auth.texts['update_adventure_prompt'], function () {
        update_db_adventure(adventure_id);
    });
   } else {
       update_db_adventure(adventure_id);
   }
}

export function preview_adventure() {
    let content = DOMPurify.sanitize(<string>$('#custom_adventure_content').val());
    const name = <string>$('#custom_adventure_name').val();
    const level = <number>$('#custom_adventure_level').val();
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

export function delete_adventure(adventure_id: string) {
    modal.confirm(auth.texts['delete_adventure_prompt'], function () {
        $.ajax({
            type: 'DELETE',
            url: '/for-teachers/customize-adventure/' + adventure_id,
            contentType: 'application/json',
            dataType: 'json'
        }).done(function () {
            window.location.href = '/for-teachers';
        }).fail(function (err) {
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

     let selected_teacher_adventures: (string | null)[] = [];
     $('#teacher_adventures_overview li').each(function() {
         if ($(this).is(':visible') && $(this).find(':input').prop('checked')) {
             selected_teacher_adventures.push(this.getAttribute('id'));
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
         teacher_adventures: selected_teacher_adventures,
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
         // location.reload ();
         // TODO TB -> Front-end already up to date; no need for re-load! Look into this with customizations impro.
       }
     }).fail(function(err) {
       console.error(err);
       error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
     });
}

export  function reset_level_preferences(level: number) {
 $('#adventures_overview li').each(function() {
     if ($(this).is(':visible')) {
         $(this).find(':input').prop("checked", true);
     }
 });
 $('#example_programs' + level).prop("checked", true);
 $('#hide_level' + level).prop("checked", false);
}


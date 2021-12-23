import { modal, error } from './modal';
import { auth } from './auth';

export function create_class() {
  modal.prompt (auth.texts['class_name_prompt'], '', function (class_name) {
    if (!class_name) {
      modal.alert(auth.texts['class_name_empty']);
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
    }).done(function(_response) {
      window.location.pathname = '/customize-class/' + _response.id ;
    }).fail(function(err) {
      if (err.responseText == "duplicate") {
        modal.alert(auth.texts['class_name_duplicate']);
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
      modal.alert(auth.texts['class_name_empty']);
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
    }).done(function(_response) {
      location.reload ();
    }).fail(function(err) {
      if (err.responseText == "duplicate") {
        modal.alert(auth.texts['class_name_duplicate']);
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
    }).done(function(_response) {
      window.location.pathname = '/for-teachers';
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
    });
  });
}

export function join_class(link: string, name: string, noRedirect=false) {
  // If there's no session but we want to join the class, we store the program data in localStorage and redirect to /login.
  if (! auth.profile) {
    return modal.confirm (auth.texts['join_prompt'], function () {
      localStorage.setItem ('hedy-join', JSON.stringify ({link: link, name: name}));
      window.location.pathname = '/login';
      return;
    });
  }

  $.ajax({
    type: 'GET',
    url: link,
  }).done(function(_response) {
    modal.alert (auth.texts['class_join_confirmation'] + ' ' + name);
    if (! noRedirect) window.location.pathname = '/programs';
  }).fail(function(err) {
    console.error(err);
    error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
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
    }).done(function(_response) {
      location.reload ();
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages['Connection_error'], JSON.stringify(err));
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
     }).done(function(_response) {
       location.reload ();
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


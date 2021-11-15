import { modal, error } from './modal';
import { auth } from './auth';

export function create_class() {
  modal.prompt (auth.texts['class_name_prompt'], '', function (class_name) {

    $.ajax({
      type: 'POST',
      url: '/class',
      data: JSON.stringify({
        name: class_name
      }),
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

export function rename_class(id: string) {
  modal.prompt (auth.texts['class_name_prompt'], '', function (class_name) {
    if (! class_name) {
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

export function remove_student(class_id: string, student_id: string) {
  modal.confirm (auth.texts['remove_student_prompt'], function () {

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


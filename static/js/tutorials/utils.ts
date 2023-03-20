// All these functions are general and easy to use within all tutorial .ts files
// Most important is the tutorialPopup() function that retrieves the actual step from the server

import {modal} from "../modal";

export function addHighlightBorder(element_id: string) {
  $('#' + element_id).addClass('border-2 rounded-lg border-red-500');
}

export function removeBorder(element_id: string) {
  $('#' + element_id).removeClass('border-2 border-red-500');
}

export function relocatePopup(x: number, y: number) {
  $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  if (x && y) {
    let left = x.toString() + "%"
    let top = y.toString() + "%"
    $('#tutorial-pop-up').css({'top': top, 'left': left});
  }

}

export function tutorialPopup(current_level: string, step: number) {
  let route = "/get_tutorial_step/" + current_level + "/"
  $.ajax({
    type: 'GET',
    url: route + step.toString(),
    dataType: 'json'
  }).done(function(response: any) {
      $('#tutorial_title').text(response.title);
      $('#tutorial_text').text(response.text);
      $('#tutorial-pop-up').fadeIn(800);
  }).fail(function(response) {
    modal.notifyError(response.responseText);
  });
}
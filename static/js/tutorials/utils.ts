import {modal} from "../modal";

function addHighlightBorder(element_id: string) {
  $('#' + element_id).addClass('border-2 rounded-lg border-red-500');
}

function removeBorder(element_id: string) {
  $('#' + element_id).removeClass('border-2 border-red-500');
}

function relocatePopup(x: number, y: number) {
  $('#tutorial-pop-up').css({'top': '20%', 'left': '50%'});
  if (x && y) {
    let left = x.toString() + "%"
    let top = y.toString() + "%"
    $('#tutorial-pop-up').css({'top': top, 'left': left});
  }

}

// We should keep this code right here -> the rest should move to dedicated files!

function tutorialPopup(step: number) {
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
    modal.alert(response.responseText, 3000, true);
  });
}
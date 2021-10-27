/**
 * The modal we pop up to have children confirm things
 */
class Modal {
  constructor() {
    // Just one binding, never needs stat
    $('#modal-confirm-button').on('click', () => this.hide());
    $('#modal-no-button').on('click', () => this.hide());
    $('#modal-cancel-button').on('click', () => this.hide());
  }

  public show() {
    $('#modal-mask').show();
    $('#modal-content').show();
    window.scrollTo(0, 0);
  }

  public hide() {
    $('#modal-mask').hide();
    $('#modal-content').hide();
    $('#modal-alert').hide();
    $('#modal-prompt').hide();
    $('#modal-confirm').hide();
  }

  public alert(message: string, timeoutMs?: number) {
    $('#modal-alert-text').text(message);
    this.show();
    $('#modal-alert').show();
    if (timeoutMs) setTimeout(() => this.hide(), timeoutMs);
  }

  public confirm(message: string, confirmCb: () => void) {
    $('#modal-confirm-text').text(message);
    this.show();
    $('#modal-confirm').show();

    // Since we need to close over the callback, replace the handler
    $('#modal-yes-button').off('click').on('click', () => {
      this.hide();
      confirmCb();
    });
  }

  public prompt(message: string, defaultValue: string, confirmCb: (x: string) => void) {
    $('#modal-prompt-text').text(message);
    this.show();
    $('#modal-prompt').show();
    if (defaultValue) $('#modal-prompt-input').val(defaultValue);

    // Since we need to close over the callback, replace the handler
    $('#modal-ok-button').off('click').on('click', () => {
      this.hide();

      const value = $('#modal-prompt-input').val();
      if (typeof value === 'string') {
        confirmCb(value);
      }
    });
  }
}

let editor: AceAjax.Editor | undefined;

/**
 * The error that appears underneath the code editor
 */
export const error = {
  setEditor(e: AceAjax.Editor) {
    editor = e;
  },

  hide() {
    $('#errorbox').hide();
    $('#warningbox').hide();
    editor?.resize();
  },

  hideFeedback() {
    $('#feedbackbox').hide();
    editor?.resize();
  },

  showWarning(caption: string, message: string) {
    $('#warningbox .caption').text(caption);
    $('#warningbox .details').text(message);
    $('#warningbox').show();
    editor?.resize();
  },

  showFeedback(caption: string, message: string) {
    $('#feedbackbox .caption').text(caption);
    var obj = $("#feedbackbox .details").text(message);
    obj.html(obj.html().replace(/\n/g,'<br/>'));
    obj.html(obj.html().replace(/\t/g, '&nbsp&nbsp&nbsp&nbsp'));
    $('#feedbackbox').show();
    editor?.resize();
  },

  show(caption: string, message: string) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').text(message);
    $('#errorbox').show();
    editor?.resize();
  }
}

export const modal = new Modal();

/**
 * The modal we pop up to have children confirm things
 */

class Modal {
  constructor() {
    // Just one binding, never needs stat
    $('#modal-confirm-button').on('click', () => this.hide());
    $('#modal-no-button').on('click', () => this.hide());
    $('#modal-cancel-button').on('click', () => this.hide());
    $('#modal-copy-ok-button').on('click', () => this.hide());
    $('#modal-copy-close-button').on('click', () => this.hide());
    $('#modal-repair-button').on('click', () => this.hide());
    $('#modal-preview-button').on('click', () => this.hide());
    $('#modal-alert-button').on('click', () => this.hide_alert());
  }

  private _timeout?: ReturnType<typeof setTimeout>
  private _alert_timeout?: ReturnType<typeof setTimeout>

  public show() {
    $('#modal-mask').show();
    $('#modal-content').show();
    window.scrollTo(0, 0);
  }

  public hide() {
    $('#modal-mask').hide();
    $('#modal-content').hide();
    $('#modal-prompt').hide();
    $('#modal-confirm').hide();
    $('#modal-copy').hide();
    $('#modal-repair').hide();
    $('#modal-preview').hide();
    $('#modal-feedback').hide();
  }

  public hide_alert() {
    $('#modal-alert').fadeOut(500);
  }

  /**
   * Display a temporary success popup
   */
  public notifySuccess(message: string, timeoutMs: number = 3000) {
    return this.alert(message, timeoutMs);
  }

  /**
   * Display a temporary error popup
   */
  public notifyError(message: string, timeoutMs: number = 5000) {
    return this.alert(message, timeoutMs, true);
  }

  /**
   * Display a temporary popup
   */
  private alert(message: string, timeoutMs?: number, error?: boolean) {
    $('#modal_alert_container').toggleClass('bg-red-100 border-red-400 text-red-700', !!error);
    $('#modal_alert_container').toggleClass('bg-green-100 border-green-400 text-green-700', !error);
    $('#modal-alert-button').toggleClass('text-red-500', !!error);
    $('#modal-alert-button').toggleClass('text-green-500', !error);

    $('#modal_alert_text').html(message);
    $('#modal-alert').fadeIn(500);

    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._alert_timeout) {
      clearTimeout(this._alert_timeout);
      this._alert_timeout = undefined;
    }
    if (timeoutMs) this._alert_timeout = setTimeout(() => this.hide_alert(), timeoutMs);
  }

  public copy_alert(message: string, timeoutMs?: number, title: string = '',) {
    this.hide();
    if(title != '') {
      $('#modal-copy-title').html(title);
      $('#modal-copy-title').removeClass('hidden');
    }
    else{
      $('#modal-copy-title').html('');
      $('#modal-copy-title').addClass('hidden');
    }
    $('#modal-copy-text').html(message);
    this.show();
    $('#modal-copy').show();
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
    if (timeoutMs) this._timeout = setTimeout(() => this.hide(), timeoutMs);
  }

  public preview(content: JQuery, title: string) {
    this.hide();
    $('#modal-preview-title').html(title);
    const target = $('#modal-preview-content');
    content.attr('id', 'modal-preview-content');
    target.replaceWith(content);

    this.show();
    $('#modal-preview').show();
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
  }

  public repair(message: string, timeoutMs?: number,  title: string = '') {
    this.hide();
    if(title != '') {
      $('#modal-repair-title').html(title);
      $('#modal-repair-title').removeClass('hidden');
    }
    else{
      $('#modal-repair-title').html('');
      $('#modal-repair-title').addClass('hidden');
    }
    $('#modal-repair-text').html(message);
    this.show();
    $('#modal-repair').show();
    if (timeoutMs) setTimeout(() => this.hide(), timeoutMs);
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
    if (timeoutMs) this._timeout = setTimeout(() => this.hide(), timeoutMs);
  }

  /**
   * modal.confirm as a promise
   */
  public confirmP(message: string): Promise<void> {
    return new Promise<void>(ok => this.confirm(message, ok));
  }

  // The declineCb is optional, mainly for relic code support: add if needed otherwise leave empty on call
  public confirm(message: string, confirmCb: () => void, declineCb: () => void = function(){}) {
    this.hide();
    $('#modal-confirm-text').text(message);
    this.show();
    $('#modal-confirm').show();
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
    // Since we need to close over the callback, replace the handler
    $('#modal-yes-button').off('click').on('click', () => {
      this.hide();
      confirmCb();
    });
    $('#modal-no-button').off('click').on('click', () => {
      this.hide();
      declineCb();
    });
  }

  public prompt(message: string, defaultValue: string, confirmCb: (x: string) => void) {
    this.hide();
    $('#modal-prompt-text').text(message);
    this.show();
    $('#modal-prompt').show();
    if (defaultValue) $('#modal-prompt-input').val(defaultValue);
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }

    // Since we need to close over the callback, replace the handler
    $('#modal-ok-button').off('click').on('click', () => {
      this.hide();

      const value = $('#modal-prompt-input').val();
      if (typeof value === 'string') {
        // Always empty the value on success -> otherwise this value is shown on new prompt (without a page reload)
        $('#modal-prompt-input').val('');
        confirmCb(value);
      }
    });
  }

    public feedback(message: string) {
      this.hide();
      $('#modal-feedback-message').text(message);
      this.show();
      $('#modal-feedback').show();
      $('#modal-feedback-input').trigger("focus");
    }
}

/**
 * The error that appears underneath the code editor
 */
export const success = {
  hide: function () {
    $('#okbox').hide();
  },

  showWarning(caption: string, message: string) {
    $('#okbox .caption').text(caption);
    $('#okbox .details').text(message);
    $('#okbox').show();
  },

  show(caption: string, confetti: boolean) {
    if (confetti){
      $('#confetti-button').show();
    }
    $('#okbox .caption').text(caption);
    $('#okbox').show();
    setTimeout(function() {
      $('#okbox').hide();
    }, 3000);
  }
}

export const error = {
  hide() {
    $('#errorbox').hide();
    $('#warningbox').hide();
  },
  showWarning(caption: string, message: string) {
    this.hide();
    $('#warningbox .caption').text(caption);
    $('#warningbox .details').text(message);
    $('#warningbox').show();
  },

  show(caption: string, message: string) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').html(message);
    $('#errorbox').show();
  },

  showFadingWarning(caption: string, message: string) {
    error.showWarning(caption, message);
    setTimeout(function(){
      $('#warningbox').fadeOut();
    }, 10000);
  }
}

export const modal = new Modal();

/**
 * Run a code block, show a popup if we catch an exception
 */
export async function tryCatchPopup(cb: () => void | Promise<void>) {
  try {
    return await cb();
  } catch (e: any) {
    console.log('Error', e);
    modal.notifyError(e.message);
  }
}

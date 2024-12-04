/**
 * The modal we pop up to have children confirm things
 */

class Modal {
  constructor() {
    // Just one binding, never needs stat
    $('#modal_confirm_button').on('click', () => this.hide());
    $('#modal_no_button').on('click', () => this.hide());
    $('#modal_cancel_button').on('click', () => this.hide());
    $('#modal_copy_ok_button').on('click', () => this.hide());
    $('#modal_copy_close_button').on('click', () => this.hide());
    $('#modal_repair_button').on('click', () => this.hide());
    $('#modal_preview_button').on('click', () => this.hide());
    $('#modal_alert_button').on('click', () => this.hide_alert());
  }

  private _timeout?: ReturnType<typeof setTimeout>
  private _alert_timeout?: ReturnType<typeof setTimeout>

  public show() {
    $('#modal_mask').show();
    $('#modal_content').show();
    window.scrollTo(0, 0);
  }

  public hide() {
    $('#modal_mask').hide();
    $('#modal_content').hide();
    $('#modal_prompt').hide();
    $('#modal_confirm').hide();
    $('#modal_copy').hide();
    $('#modal_repair').hide();
    $('#modal_preview').hide();
  }

  public hide_alert() {
    $('#modal_alert').fadeOut(500);
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
    $('#modal_alert_button').toggleClass('text-red-500', !!error);
    $('#modal_alert_button').toggleClass('text-green-500', !error);

    $('#modal_alert_text').html(message);
    $('#modal_alert').fadeIn(500);

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
      $('#modal_copy_title').html(title);
      $('#modal_copy_title').removeClass('hidden');
    }
    else{
      $('#modal_copy_title').html('');
      $('#modal_copy_title').addClass('hidden');
    }
    $('#modal_copy_text').html(message);
    this.show();
    $('#modal_copy').show();
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
    if (timeoutMs) this._timeout = setTimeout(() => this.hide(), timeoutMs);
  }

  public preview(content: JQuery, title: string) {
    this.hide();
    $('#modal_preview_title').html(title);
    const target = $('#modal_preview_content');
    content.attr('id', 'modal_preview_content');
    target.replaceWith(content);

    this.show();
    $('#modal_preview').show();
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
  }

  public repair(message: string, timeoutMs?: number,  title: string = '') {
    this.hide();
    if(title != '') {
      $('#modal_repair_title').html(title);
      $('#modal_repair_title').removeClass('hidden');
    }
    else{
      $('#modal_repair_title').html('');
      $('#modal_repair_title').addClass('hidden');
    }
    $('#modal_repair_text').html(message);
    this.show();
    $('#modal_repair').show();
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
    $('#modal_confirm_text').text(message);
    this.show();
    $('#modal_confirm').show();
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }
    // Since we need to close over the callback, replace the handler
    $('#modal_yes_button').off('click').on('click', () => {
      this.hide();
      confirmCb();
    });
    $('#modal_no_button').off('click').on('click', () => {
      this.hide();
      declineCb();
    });
  }

  public prompt(message: string, defaultValue: string, confirmCb: (x: string) => void) {
    this.hide();
    $('#modal_prompt_text').text(message);
    this.show();
    $('#modal_prompt').show();
    if (defaultValue) $('#modal_prompt_input').val(defaultValue);
    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }

    // Since we need to close over the callback, replace the handler
    $('#modal_ok_button').off('click').on('click', () => {
      this.hide();

      const value = $('#modal_prompt_input').val();
      if (typeof value === 'string') {
        // Always empty the value on success -> otherwise this value is shown on new prompt (without a page reload)
        $('#modal_prompt_input').val('');
        confirmCb(value);
      }
    });
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
      $('#confetti_button').show();
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
  showWarning(message: string) {
    this.hide();
    $('#warningbox .details').text(message);
    $('#warningbox').show();
  },

  show(caption: string, message: string) {
    $('#errorbox .details').html(caption + " " + message);
    $('#errorbox').show();
  },

  showFadingWarning(message: string) {
    error.showWarning(message);
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

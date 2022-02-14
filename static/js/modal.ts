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

  public show_alert() {
    $('#modal-alert').fadeIn(1000);
  }

  public hide() {
    $('#modal-mask').hide();
    $('#modal-content').hide();
    $('#modal-prompt').hide();
    $('#modal-confirm').hide();
    $('#modal-copy').hide();
    $('#modal-repair').hide();
    $('#modal-preview').hide();
  }

  public hide_alert() {
    $('#modal-alert').fadeOut(1000);
  }

  public alert(message: string, timeoutMs?: number, error?: boolean) {
    // Always hide possible previous alert -> make sure it is hidden
    this.hide_alert();
    $('#modal_alert_container').removeClass('bg-red-100 border-red-400 text-red-700');
    $('#modal-alert-button').removeClass('text-red-500');
    $('#modal_alert_container').addClass('bg-green-100 border-green-400 text-green-700');
    $('#modal-alert-button').addClass('text-green-500');
    if (error) {
      $('#modal_alert_container').removeClass('bg-green-100 border-green-400 text-green-700');
      $('#modal-alert-button').removeClass('text-green-500');
      $('#modal_alert_container').addClass('bg-red-100 border-red-400 text-red-700');
      $('#modal-alert-button').addClass('text-red-500');
    }
    $('#modal_alert_text').html(message);
    this.show_alert();
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

  public confirm(message: string, confirmCb: () => void) {
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
        confirmCb(value);
      }
    });
  }
}

let editor: AceAjax.Editor | undefined;

/**
 * The error that appears underneath the code editor
 */
export const success = {
  setEditor(e: AceAjax.Editor) {
    editor = e;
  },

  hide: function () {
    $('#okbox').hide();
    editor?.resize();

  },

  showWarning(caption: string, message: string) {
    $('#okbox .caption').text(caption);
    $('#okbox .details').text(message);
    $('#okbox').show();
    editor?.resize();
  },

  show(caption: string) {
    $('#okbox .caption').text(caption);
    $('#okbox').show();
    editor?.resize();
    setTimeout(function(){     $('#okbox').hide();
    editor?.resize(); }, 3000);
  }
}

export const error = {
  setEditor(e: AceAjax.Editor) {
    editor = e;
  },

  hide() {
    $('#errorbox').hide();
    $('#warningbox').hide();
    editor?.resize();
  },

  showWarning(caption: string, message: string) {
    $('#warningbox .caption').text(caption);
    $('#warningbox .details').text(message);
    $('#warningbox').show();
    editor?.resize();
  },

  show(caption: string, message: string) {
    $('#errorbox .caption').text(caption);
    $('#errorbox .details').html(message);
    $('#errorbox').show();
    editor?.resize();
  }
}

export const modal = new Modal();

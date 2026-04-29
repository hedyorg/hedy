declare const htmx: typeof import('./htmx');
/**
 * The modal we pop up to have children confirm things
 */

class Modal {
  private readonly redesignConfirmDefaultButtonClass: string;
  private readonly redesignConfirmDefaultButtonLabel: string;
  private readonly redesignConfirmDefaultActionsClass: string;

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
    $('#redesign_confirm_close_button').on('click', () => this.hideRedesignConfirm());
    $('#redesign_confirm_no_button').on('click', () => this.hideRedesignConfirm());
    $('#redesign_confirm_backdrop').on('click', () => this.hideRedesignConfirm());
    $('#redesign_prompt_close_button').on('click', () => this.hideRedesignPrompt());
    $('#redesign_prompt_cancel_button').on('click', () => this.hideRedesignPrompt());
    $('#redesign_prompt_backdrop').on('click', () => this.hideRedesignPrompt());
    $('#redesign_search_close_button').on('click', () => this.hideRedesignSearch());
    $('#redesign_search_cancel_button').on('click', () => this.hideRedesignSearch());
    $('#redesign_search_backdrop').on('click', () => this.hideRedesignSearch());

    const redesignConfirmYesButton = $('#redesign_confirm_yes_button');
    const redesignConfirmActions = $('#redesign_confirm_actions');
    this.redesignConfirmDefaultButtonClass = String(redesignConfirmYesButton.attr('class') ?? 'green-btn-new');
    this.redesignConfirmDefaultButtonLabel = String(redesignConfirmYesButton.text()).trim();
    this.redesignConfirmDefaultActionsClass = String(redesignConfirmActions.attr('class') ?? '');
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
    $('#modal_search').hide();
    this.hideRedesignConfirm();
    this.hideRedesignPrompt();
    this.hideRedesignSearch();
  }

  public hideRedesignConfirm() {
    $('#redesign_confirm_modal').addClass('hidden').removeClass('flex');
    $('body').removeClass('overflow-hidden');
  }

  public hideRedesignPrompt() {
    $('#redesign_prompt_modal').addClass('hidden').removeClass('flex');
    $('#redesign_prompt_input').val('');
    $('body').removeClass('overflow-hidden');
  }

  public hideRedesignSearch() {
    $('#redesign_search_modal').addClass('hidden').removeClass('flex');
    $('#redesign_search_input').val('');
    $('body').removeClass('overflow-hidden');
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

  public confirmRedesign(
    message: string,
    confirmCb: () => void,
    declineCb: () => void = function(){},
    options?: {
      confirmButtonClass?: string;
      confirmButtonLabel?: string;
      confirmActionsClass?: string;
    },
  ) {
    this.hide();
    const redesignConfirmYesButton = $('#redesign_confirm_yes_button');
    const redesignConfirmActions = $('#redesign_confirm_actions');

    redesignConfirmYesButton.attr('class', options?.confirmButtonClass ?? this.redesignConfirmDefaultButtonClass);
    redesignConfirmYesButton.text(options?.confirmButtonLabel ?? this.redesignConfirmDefaultButtonLabel);
    redesignConfirmActions.attr('class', options?.confirmActionsClass ?? this.redesignConfirmDefaultActionsClass);

    $('#redesign_confirm_text').text(message);
    $('#redesign_confirm_modal').removeClass('hidden').addClass('flex');
    $('body').addClass('overflow-hidden');

    // If there's a timeout from a previous modal that hasn't been cleared yet, clear it to avoid hiding the present message before its due time.
    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }

    $('#redesign_confirm_yes_button').off('click').on('click', () => {
      this.hideRedesignConfirm();
      confirmCb();
    });

    $('#redesign_confirm_no_button, #redesign_confirm_close_button').off('click').on('click', () => {
      this.hideRedesignConfirm();
      declineCb();
    });

    $('#redesign_confirm_backdrop').off('click').on('click', () => {
      this.hideRedesignConfirm();
      declineCb();
    });
  }

  /**
   * Modal for a htmx-based search.
   * 
   * @param message The text to show above the search box
   * @param input_attr HTMX attributes to attach to the search input box
   * @param confirm_attr HTMX attributes to attach to the confirm button
   * @param result_target The target element to update with the search results
   * @param confirm_label Optional text to use for the confirmation
   */
  public htmx_search(message: string, input_attr: Record<string, string>, confirm_attr: Record<string, string>, result_target: string, confirm_label?: string, success_message?: string, modalVariant: 'legacy' | 'redesign' = 'legacy') {
    if (modalVariant === 'redesign') {
      return this.htmx_search_redesign(message, input_attr, confirm_attr, result_target, confirm_label, success_message);
    }

    this.hide();
    $('#modal_search_text').text(message);
    if (confirm_label) $('#modal_ok_search_button').text(confirm_label)
    $('#modal_search_input').attr(input_attr);
    $('#modal_ok_search_button').attr(confirm_attr);
    $(result_target).attr({'hx-on::after-settle': `hedyApp.close_htmx_search_modal("${success_message}")`});
    htmx.process(document.body)
    this.show();
    $('#modal_search').show();
    $('#modal_cancel_search_button').off('click').on('click', () => {
      this.hide();
      this.clear_search_boxes();
    });
  }

  public htmx_search_redesign(message: string, input_attr: Record<string, string>, confirm_attr: Record<string, string>, result_target: string, confirm_label?: string, success_message?: string) {
    this.hide();
    $('#redesign_search_text').text(message);
    if (confirm_label) $('#redesign_search_ok_button').text(confirm_label)
    $('#redesign_search_input').attr(input_attr);
    $('#redesign_search_ok_button').attr(confirm_attr);
    $(result_target).attr({'hx-on::after-settle': `hedyApp.close_htmx_search_modal("${success_message}")`});
    htmx.process(document.body)
    $('#redesign_search_modal').removeClass('hidden').addClass('flex');
    $('body').addClass('overflow-hidden');
    $('#redesign_search_cancel_button').off('click').on('click', () => {
      this.hideRedesignSearch();
      this.clear_search_boxes();
    });
  }
  
  public clear_search_boxes() {
    $('#modal_search_input').val("");
    const users_to_invite = document.getElementById('users_to_invite');
    if (users_to_invite) users_to_invite.innerHTML = ''
    const search_results = document.getElementById('search_results')
    if (search_results) search_results.innerHTML = ''
    $('#redesign_search_input').val("");
    const redesign_users_to_invite_container = document.getElementById('redesign_users_to_invite_container');
    if (redesign_users_to_invite_container) redesign_users_to_invite_container.classList.add('hidden')
    const redesign_users_to_invite = document.getElementById('redesign_users_to_invite');
    if (redesign_users_to_invite) redesign_users_to_invite.innerHTML = ''
    const redesign_search_results = document.getElementById('redesign_search_results')
    if (redesign_search_results) redesign_search_results.innerHTML = ''
  }

  public prompt(message: string, defaultValue: string, confirmCb: (x: string) => void, modalVariant: 'legacy' | 'redesign' = 'legacy', title: string = '') {
    if (modalVariant === 'redesign') {
      return this.promptRedesign(message, defaultValue, confirmCb, title);
    }

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

  public promptRedesign(message: string, defaultValue: string, confirmCb: (x: string) => void, title: string = '') {
    this.hide();
    $('#redesign_prompt_title').text(title);
    $('#redesign_prompt_text').text(message);
    $('#redesign_prompt_input').val(defaultValue || '');
    $('#redesign_prompt_modal').removeClass('hidden').addClass('flex');
    $('body').addClass('overflow-hidden');

    if(this._timeout) {
      clearTimeout(this._timeout);
      this._timeout = undefined;
    }

    const submit = () => {
      const value = $('#redesign_prompt_input').val();
      this.hideRedesignPrompt();
      if (typeof value === 'string') {
        confirmCb(value);
      }
    };

    $('#redesign_prompt_ok_button').off('click').on('click', submit);
    $('#redesign_prompt_input').off('keydown').on('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        submit();
      }
    });

    $('#redesign_prompt_cancel_button, #redesign_prompt_close_button').off('click').on('click', () => {
      this.hideRedesignPrompt();
    });

    $('#redesign_prompt_backdrop').off('click').on('click', () => {
      this.hideRedesignPrompt();
    });

    $('#redesign_prompt_input').trigger('focus');
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


export function close_htmx_search_modal(confirmation_message?: string) {
  modal.hide()
  modal.clear_search_boxes()
  if (confirmation_message) {
    modal.notifySuccess(confirmation_message)
  }
}

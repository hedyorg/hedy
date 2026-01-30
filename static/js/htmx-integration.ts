/**
 * Custom integrations we have with HTMX
 */
import { initializeHighlightedCodeBlocks } from './app';
import { ClientMessages } from './client-messages';
import { modal } from './modal';
import Sortable from 'sortablejs';

declare const htmx: typeof import('./htmx');

/**
 * Disable elements as they are being used to submit HTMX requests.
 *
 * Prevents impatient kids from double-triggering server-side events.
 */
htmx.defineExtension('disable-element', {
  onEvent: function (name, evt) {
      let elt = evt.detail.elt;
      if (!elt.getAttribute) {
        return;
      }

      let target = elt.getAttribute("hx-disable-element") ?? 'self';
      let targetElement = (target == "self") ? elt : document.querySelector(target);

      if (name === "htmx:beforeRequest" && targetElement) {
          targetElement.disabled = true;
      } else if (name == "htmx:afterRequest" && targetElement) {
          targetElement.disabled = false;
      }
  }
});

/**
 * We have some custom JavaScript to run on new content that's loaded into the DOM.
 *
 * What we do:
 *
 * - Turning <pre>s into Ace editors
 * - Initialize sortables
 * - Reset the scroll position on lists that need it
 */
htmx.onLoad((content) => {
    initializeHighlightedCodeBlocks(content, true);

    $(content).find('.htmx-resetscroll').scrollTop(0);

    var sortables =  content.querySelectorAll('.sortable');
    for (let i = 0; i < sortables.length; i++) {
        var sortable = sortables[i] as HTMLElement;
        new Sortable(sortable, {
            animation: 150,
            ghostClass: 'drop-adventures-active'
        })
    }
});

interface HtmxEvent {
    readonly xhr: XMLHttpRequest;
    readonly error: string;
}

/**
 * If the server reports an error, we send it into our regular error popup
 */
htmx.on('htmx:responseError', (ev) => {
    const event = ev as CustomEvent<HtmxEvent>;
    const xhr: XMLHttpRequest = event.detail.xhr;
    const genericError = event.detail.error;
    try {
        const jsonResponse = JSON.parse(xhr.response)
        const message = jsonResponse?.message ?? genericError
        const stack_trace = jsonResponse?.stack_trace ?? "";
        console.error('======================================');
        console.error('There was a server error, please report to the maintainers at hello@hedy.org');
        console.error(stack_trace);
        console.error('======================================');
        modal.notifyError(message.length < 1000 ? message : genericError);
    } catch (e) {
        modal.notifyError(genericError);
        return;
    }
});

htmx.on('htmx:sendError', () => {
    modal.notifyError(`${ClientMessages.Connection_error} ${ClientMessages.CheckInternet}`);
});

htmx.on("htmx:confirm", function(e: any) {
    e.preventDefault();
    const modalPrompt = e.target.getAttribute("hx-confirm");
    // this is to prevent window.confirm. Just passing true to issueRequest isn't enough.
    if (!modalPrompt) {
        // if no confirm attribute was attached, just continue with the  request.
        e.detail.issueRequest(true);
        return;
    }
    modal.confirm(modalPrompt, () => {
        e.target.removeAttribute("hx-confirm");
        e.detail.issueRequest(true);
        const success_message = e.target.getAttribute("data-success-message")
        if (success_message) {
            modal.notifySuccess(success_message);
        }
    });
});

/**
 * Custom integrations we have with HTMX
 */
import { initializeHighlightedCodeBlocks, showAchievements } from './app';
import { ClientMessages } from './client-messages';
import { modal } from './modal';
import { Achievement } from './types';
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
 * (Notably: turning <pre>s into Ace editors)
 */
htmx.onLoad((content) => {
    initializeHighlightedCodeBlocks(content);
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
    modal.notifyError(xhr.responseText.length < 1000 ? xhr.responseText : genericError);
});

htmx.on('htmx:sendError', () => {
    modal.notifyError(`${ClientMessages.Connection_error} ${ClientMessages.CheckInternet}`);
});


/**
 * The server can trigger achievement events
 */
htmx.on('displayAchievements', (ev) => {
    const payloads = (ev as any).detail.value
    for (const payload of payloads) {
        const achievement= payload["achievement"] as Achievement[]
        showAchievements(achievement, payload["reload"], payload["redirect"])
    }
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
    });
});

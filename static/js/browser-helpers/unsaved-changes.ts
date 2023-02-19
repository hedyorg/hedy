import { ClientMessages } from '../client-messages';

function unloadHandler(event: BeforeUnloadEvent) {
  event.preventDefault();
  return event.returnValue = ClientMessages['Unsaved_Changes'];
}

let unsavedChanges = false;

export function hasUnsavedChanges() {
  return unsavedChanges;
}

/**
 * Whether there are unsaved changes (used by the HTML)
 */
export function markUnsavedChanges() {
  unsavedChanges = true;
  window.addEventListener('beforeunload', unloadHandler, { capture: true });
}

/**
 * Clear unsaved changes marker
 */
export function clearUnsavedChanges() {
  unsavedChanges = false;
  // MDN tells me to add and remove this listener as necessary: https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event
  window.removeEventListener('beforeunload', unloadHandler, { capture: true });
}

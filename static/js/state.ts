import { ClientMessages } from './client-messages';

/**
 * The global state we keep
 *
 * This should contain as little as possible: preferably, we know
 * for each bit of code what data it needs, and we pass it directly.
 */
export interface State {
  /**
   * Current language
   *
   * Written: by every page, on page load.
   * Used: on the code page, to do speech synthesis and to send to the server.
   */
  lang: string;

  /**
   * Current level
   *
   * Written: by every page, on page load.
   *
   * Used: on the code page, to initialize the highlighter, to translate the program,
   * to determine timeouts, to load the quiz iframe, to show the variable inspector,
   * to show a debugger,  to load parsons exercises, to initialize a default save name.
   */
  level: number;

  /**
   * Current keyword language
   *
   * Written: by every page, on page load.
   *
   * Used: set on the Ace editor, and then is used to do some magic that I don't
   * quite understand.
   */
  keyword_language: string;
}

/**
 * A mutable version of the state, only writable from inside this module.
 */
const THE_STATE: State = {
  lang: 'en',
  level: 1,
  keyword_language: 'en',
};

/**
 * A readonly version of the state
 */
export const APP_STATE: Readonly<State> = THE_STATE;

/**
 * Pass some state in from the HTML page
 */
export function setState(stateUpdate: Partial<State>) {
  for (const [key, value] of Object.entries(stateUpdate)) {
    (THE_STATE as any)[key] = value;
  }
}

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

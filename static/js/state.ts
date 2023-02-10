import { ClientMessages } from './client-messages';

/**
 * The global state we keep
 *
 * This is in desperate need of cleaning up!!
 *
 * This shouldn't contain as much as it does.
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

  /**
   * The adventure data available on the current page
   *
   * Written: We set Adventure.loaded_program in app.ts to the
   * code of the loaded program, on load.
   *
   * Used: when switching tabs, to set one of the programs values.
   */
  adventures?: Adventure[];

  /**
   * Load program info
   *
   * Written: on page load, if a program has been loaded by ID.
   *
   * Used: to initialize the code page, and the viewer.
   */
  loaded_program?: Program;
}

export interface Adventure {
  example_code: string;
  short_name: string;
  loaded_program?: Program;
  default_save_name: string;
  start_code: string;
  extra_stories?: ExtraStory[];
  image?: string | null;
  name: string; // Translated name
  text?: string;
}

export interface ExtraStory {
  example_code?: string;
  text?: string;
}

export interface Program {
  name: string;
  code: string;
  adventure_name?: string;
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

const CONVERTERS: Partial<{ [K in keyof State]: (x: unknown) => State[K] }> = {
  level: (x: unknown): number => {
    if (typeof x === 'number') { return x; }
    return parseInt(`${x}`, 10);
  }
};

/**
 * Pass some state in from the HTML page
 */
export function passStateFromHtml(stateUpdate: Partial<State>) {
  for (const [key, value] of Object.entries(stateUpdate)) {
    (THE_STATE as any)[key] = ((CONVERTERS as any)[key] ?? identity)(value);
  }
}

function identity<A>(x: A): A {
  return x;
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

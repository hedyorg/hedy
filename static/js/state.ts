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
   * The translation of the word 'level' in the current language
   *
   * Written: on page load
   *
   * Used: when building strings.
   */
  level_title?: string;

  /**
   * The keyword name of the currently displayed adventure, if displaying an adventure.
   *
   * "default" if the first tab, not updated if showing parsons or quiz tabs.
   *
   * Written: on page load (from a loaded program), and when switching tabs.
   *
   * Used: on page load, to select the right tab, and to send to server for
   * storing a program under an adventure,
   */
  adventure_name?: string;

  /**
   * Adventure name at the time the page was loaded.
   *
   * Not affected by switching tabs.
   *
   * (Only available in code page)
   *
   * Written: on page load.
   *
   * Used: in tabs.ts to set loaded program code into the editor.
   */
  adventure_name_onload?: string;

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

  /**
   * Represents whether there's an open 'ask' prompt
   */
  disable_run?: boolean;

  /**
   * Used in very many places to make the "leave this page?" popup appear
   */
  unsaved_changes?: boolean;

  /**
   * Prevent the unsaved changes prompt
   */
  no_unload_prompt?: boolean;

  /**
   * Used to record and undo pygame-related settings
   */
  pygame_running?: boolean;
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

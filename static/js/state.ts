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
   */
  lang: string;

  /**
   * Current level
   */
  level: number;

  /**
   * Current keyword language
   */
  keyword_language: string;

  /**
   * Title of current level
   */
  level_title?: string;

  /**
   * ?
   *
   * (Only available in code page)
   */
  adventure_name?: string;

  /**
   * Adventure name at the time the page was loaded.
   *
   * Not affected by switching tabs.
   *
   * (Only available in code page)
   */
  adventure_name_onload?: string;
  adventures?: Adventure[];
  default_program?: string;
  loaded_program?: Program;
  default_program_name?: string;
  disable_run?: boolean;
  unsaved_changes?: boolean;
  no_unload_prompt?: boolean;
  programsInExecution?: number;
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

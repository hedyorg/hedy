export interface Adventure {
  /** Identifier */
  short_name: string;

  /** Translated tab name */
  name: string;

  /** The type of adventure */
  is_teacher_adventure: boolean;

  /** Is this an adventure about a keyword? */
  is_command_adventure: boolean;

  /** Markdown for the introductory paragraph */
  text?: string;

  /** Example code for the introductory paragraph */
  example_code?: string;

  /** Image to go along with the tab (unused) */
  image?: string | null;

  /** More paragraphs of text and code */
  extra_stories?: ExtraStory[];

  /**
   * Name of the saved program for this adventure
   *
   * (Either the loaded program or a default).
   */
  save_name: string;

  /**
   * Initial code given in the editor
   *
   * (Either from the loaded program or a default).
   */
  start_code: string;

  /**
   * If the current program is from a save, some additional
   * information about the save.
   *
   * Either a ServerSaveInfo object if the program was loaded from a server save,
   * or the string 'local-storage' if the program was loaded from local storage.
   */
  save_info?: ServerSaveInfo | 'local-storage';
}

/**
 * Whether the given field is actually a SaveInfo object
 */
export function isServerSaveInfo(x: Adventure['save_info']): x is ServerSaveInfo {
  return !!x && typeof x === 'object' && !!x.id;
}

export interface ServerSaveInfo {
  /** Identifier of the program in the database */
  id: string;

  /**
   * Public is 0, 1 or undefined
   */
  public?: number;

  /**
   * Submitted is false, true or undefined
   */
  submitted?: boolean;

  /**
   * URL for this program if it is public
   */
  public_url?: string;
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
 * Definition of an achievement
 *
 * Array of [title, text, statistics].
 */
export type Achievement = [string, string, string];

export interface Adventure {
  /** Identifier */
  short_name: string;

  /** Translated tab name */
  name: string;

  /** The type of adventure */
  is_teacher_adventure: boolean;

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
   */
  save_info?: SaveInfo;
}

export interface SaveInfo {
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

export interface AvailableAdventure {
  from_teacher: boolean;
  name: string;
}

export interface TeacherAdventure {
  id: string;
  level: string;
}

/**
 * Definition of an achievement
 *
 * Array of [title, text, statistics].
 */
export type Achievement = [string, string, string];

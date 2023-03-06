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

export interface AvailableAdventure {
  from_teacher: boolean;
  name: string;
}

export interface TeacherAdventure {
  id: string;
  level: string;
}

import { parser as level1Parser} from './level1-parser'
import { parser as level2Parser} from './level2-parser'
import { parser as level3Parser} from './level3-parser'
import { parser as level4Parser} from './level4-parser'
import { parser as level5Parser} from './level5-parser'
import { parser as level6Parser} from './level6-parser'
import { parser as level7Parser } from './level7-parser'
import { parser as level8Parser } from './level8-parser'
import { parser as level9Parser } from './level9-parser'
import { parser as level10Parser } from './level10-parser'
import { parser as level11Parser } from './level11-parser'
import { parser as level12Parser } from './level12-parser'
import { parser as level13Parser } from './level13-parser'
import { parser as level14Parser } from './level14-parser'
import { parser as level15Parser } from './level15-parser'
import { parser as level16Parser } from './level16-parser'
import { parser as level17Parser } from './level17-parser'
import { parser as level18Parser} from './level18-parser'
import { LRParser } from '@lezer/lr';

export let languagePerLevel: Record<number, LRParser> = {
    1: level1Parser,
    2: level2Parser,
    3: level3Parser,
    4: level4Parser,
    5: level5Parser,
    6: level6Parser,
    7: level7Parser,
    8: level8Parser,
    9: level9Parser,
    10: level10Parser,
    11: level11Parser,
    12: level12Parser,
    13: level13Parser,
    14: level14Parser,
    15: level15Parser,
    16: level16Parser,
    17: level17Parser,
    18: level18Parser,
};

export const keywords = [
  "print",
  "at",
  "forward",
  "turn",
  "color",
  "play",
  "sleep",
  "is",
  "add",
  "remove",
  "from",
  "to_list",
  "clear",
  "not_in",
  "repeat",
  "times",
  "for",
  "to",
  "range",
  "return",
  "define",
  "if",
  "pressed",
  "ask",
  "echo",
  "random",
  "else",
  "and",
  "or",
  "in",
  "is",
  "while",
  "elif",
  "call",
  "with",
  "input",
  "def"
]
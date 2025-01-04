import { generateParser as generateLevel1Parser} from './level1-parser'
import { generateParser as generateLevel2Parser} from './level2-parser'
import { generateParser as generateLevel3Parser} from './level3-parser'
import { generateParser as generateLevel4Parser} from './level4-parser'
import { generateParser as generateLevel5Parser} from './level5-parser'
import { generateParser as generateLevel6Parser} from './level6-parser'
import { generateParser as generateLevel7Parser } from './level7-parser'
import { generateParser as generateLevel8Parser } from './level8-parser'
import { generateParser as generateLevel9Parser } from './level9-parser'
import { generateParser as generateLevel10Parser } from './level10-parser'
import { generateParser as generateLevel11Parser } from './level11-parser'
import { generateParser as generateLevel12Parser } from './level12-parser'
import { generateParser as generateLevel13Parser } from './level13-parser'
import { generateParser as generateLevel14Parser } from './level14-parser'
import { generateParser as generateLevel15Parser } from './level15-parser'
import { generateParser as generateLevel16Parser } from './level16-parser'
import { generateParser as generateLevel17Parser } from './level17-parser'
import { generateParser as generateLevel18Parser} from './level18-parser'
import { LRParser } from '@lezer/lr';

export let languagePerLevel: Record<number, (lang: string) => LRParser> = {
     1: (lang) => generateLevel1Parser(1, lang),
     2: (lang) => generateLevel2Parser(2, lang),
     3: (lang) => generateLevel3Parser(3, lang),
     4: (lang) => generateLevel4Parser(4, lang),
     5: (lang) => generateLevel5Parser(5, lang),
     6: (lang) => generateLevel6Parser(6, lang),
     7: (lang) => generateLevel7Parser(7, lang),
     8: (lang) => generateLevel8Parser(8, lang),
     9: (lang) => generateLevel9Parser(9, lang),
    10: (lang) => generateLevel10Parser(10, lang),
    11: (lang) => generateLevel11Parser(11, lang),
    12: (lang) => generateLevel12Parser(12, lang),
    13: (lang) => generateLevel13Parser(13, lang),
    14: (lang) => generateLevel14Parser(14, lang),
    15: (lang) => generateLevel15Parser(15, lang),
    16: (lang) => generateLevel16Parser(16, lang),
    17: (lang) => generateLevel17Parser(17, lang),
    18: (lang) => generateLevel18Parser(18, lang),
};

export const keywords = [
  "print",
  "at",
  "forward",
  "turn",
  "true",
  "True",
  "false",
  "False",
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

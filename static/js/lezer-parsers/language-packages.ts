import { parser as level1Parser} from './level1-parser'
import { parser as level2Parser} from './level2-parser'
import { parser as level3Parser} from './level3-parser'
import { parser as level4Parser} from './level4-parser'
import { parser as level5Parser} from './level5-parser'
import { parser as level6Parser} from './level6-parser'
import { parser as level7Parser } from './level7-parser'
import { parser as level8Parser } from './level8-parser'
import { parser as level10Parser } from './level10-parser'
import { parser as level11Parser } from './level11-parser'
import { parser as level12Parser } from './level12-parser'
import { parser as level18Parser} from './level18-parser'
import { tags as t } from "@lezer/highlight";
import { LRParser } from '@lezer/lr';

interface languageSupport {
    parser: LRParser,
    styleTags: Record<string, any>
}

export let languagePerLevel: Record<number, languageSupport> ={
    1: {
        parser: level1Parser,
        styleTags: {
            "print ask echo forward turn color": t.keyword,      
            Comment: t.lineComment,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    2: {
        parser: level2Parser,
        styleTags: {
            "print forward turn color ask is sleep": t.keyword,            
            Comment: t.lineComment,            
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    3: {
        parser: level3Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma": t.keyword,   
            Comment: t.lineComment,
            "Name": t.name,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    4: {
        parser: level4Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma": t.keyword,
            "clear": t.color, 
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    5: {
        parser: level5Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in": t.keyword,
            "clear pressed": t.color, 
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    6: {
        parser: level6Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in": t.keyword,
            "clear pressed": t.color, 
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Int": t.number,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    7: {
        parser: level7Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in repeat times": t.keyword,
            "clear pressed": t.color,
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Int": t.number,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    8: {
        parser: level8Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in repeat times": t.keyword,
            "clear pressed": t.color,
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Int": t.number,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    // same as level 8
    9: {
        parser: level8Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in repeat times": t.keyword,
            "clear pressed": t.color,
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Int": t.number,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    10: {
        parser: level10Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in repeat times for": t.keyword,
            "clear pressed": t.color,
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Int": t.number,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    11: {
        parser: level11Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in repeat times for range to": t.keyword,
            "clear pressed": t.color,
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Int": t.number,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    12: {
        parser: level12Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Op at random remove from add to Comma if else in not_in repeat times for range to with": t.keyword,
            "clear pressed": t.color,
            Comment: t.lineComment,
            "Name": t.name,
            "String": t.string,
            "Number": t.number,
            "define call": t.operatorKeyword,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    18: {
        parser: level18Parser,
        styleTags: {
            "print forward turn color ask is echo sleep Comma at random remove from add to if else in not Op repeat times for range with return and or while elif def input toList": t.keyword,    
            Comment: t.lineComment,
            "String": t.string,
            "clear pressed": t.color,
            "Number": t.number,
            "define call": t.operatorKeyword,
            "Command/ErrorInvalid/Text": t.invalid,
        }
    },
    
}
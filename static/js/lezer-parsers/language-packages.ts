import { parser as level1Parser} from './level1-parser'
import { parser as level18Parser} from './level18-parser'
import { tags as t } from "@lezer/highlight";
import { LRParser } from '@lezer/lr';

interface languageSupport {
    parser: LRParser,
    styleTags: Record<string, any>
}

export let languagePerLevel: Record<number, languageSupport> ={
    1: {
        "parser": level1Parser,
        "styleTags": {
            "print ask echo forward turn color": t.keyword,
            Text: t.string,        
            Comment: t.lineComment,
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
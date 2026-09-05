import { SyntaxNode } from "@lezer/common";

import { PARSER_FACTORIES, keywords } from "./lezer-parsers/language-packages";
import { traductionMap } from "./lezer-parsers/tokens";

export function addCurlyBracesToCode(code: string, level: number, language: string = 'en') {
    if (code.match(/\{(\w|_)+\}/g)) return code

    let parser = PARSER_FACTORIES[level](language);
    let parseResult = parser.parse(code);
    let formattedCode = ''
    let previous_node: SyntaxNode | undefined = undefined

    parseResult.iterate({
        enter: (node) => {
            const nodeName = node.node.name;
            let number_spaces = 0
            let previous_name = ''
            if (keywords.includes(nodeName)) {
                if (previous_node !== undefined) {
                    number_spaces = node.from - previous_node.to
                    previous_name = previous_node.name
                }
                if (previous_name !== nodeName) {
                    formattedCode += ' '.repeat(number_spaces) + '{' + nodeName + '}';
                }
                previous_node = node.node
            } else if (['Number', 'String', 'Text', 'Op', 'Comma', 'Int'].includes(nodeName)) {
                if (previous_node !== undefined) {
                    number_spaces = node.from - previous_node.to
                    previous_name = previous_node.name
                }
                formattedCode += ' '.repeat(number_spaces) + code.slice(node.from, node.to)
                previous_node = node.node
            }
        },
        leave: (node) => {
            if (node.node.name === "Command" && formattedCode[formattedCode.length - 1] !== '\n') {
                formattedCode += '\n'
                previous_node = undefined
            }
        }
    });

    let formattedLines = formattedCode.split('\n');
    let lines = code.split('\n');
    let resultingLines = []

    for (let i = 0, j = 0; i < lines.length; i++) {
        if (lines[i].trim() === '') {
            resultingLines.push(lines[i]);
            continue;
        }
        const indent_number = lines[i].search(/\S/)
        if (indent_number > -1) {
            resultingLines.push(' '.repeat(indent_number) + formattedLines[j])
        }
        j += 1;
    }
    formattedCode = resultingLines.join('\n');

    return formattedCode;
}

export function addCurlyBracesToKeyword(name: string, language?: string) {
    const lang = language || 'en';
    const TRADUCTION = traductionMap(lang);

    for (const [key, regexString] of TRADUCTION) {
        if ((new RegExp(`^(${regexString})$`, 'gu').test(name)) || name === key) {
            return `{${key}}`
        }
    }

    return name;
}
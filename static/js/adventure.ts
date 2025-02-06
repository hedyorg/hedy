import ClassicEditor from "./ckeditor";
import { CustomWindow } from './custom-window';
import { PARSER_FACTORIES, keywords } from "./lezer-parsers/language-packages";
import { SyntaxNode } from "@lezer/common";
import DOMPurify from "dompurify";
import { ClientMessages } from "./client-messages";
import { autoSave } from "./autosave";
import { HedySelect } from "./custom-elements";
import { traductionMap } from "./lezer-parsers/tokens";

declare let window: CustomWindow;

export interface InitializeCustomizeAdventurePage {
    readonly page: 'customize-adventure';
    readonly level: number;
}

let $editor: ClassicEditor;
let keywordHasAlert: Map<string, boolean> = new Map()

export async function initializeCustomAdventurePage(_options: InitializeCustomizeAdventurePage) {
    const editorContainer = document.querySelector('#adventure-editor') as HTMLElement;
    const editorSolutionExampleContainer = document.querySelector('#adventure-solution-editor') as HTMLElement;
    // Initialize the editor with the default language
    let lang = (document.querySelector('#languages_dropdown') as HedySelect).selected[0]

    if (editorContainer) {
        await initializeEditor(lang, editorContainer);
        await initializeEditor(lang, editorSolutionExampleContainer, true);
        showWarningIfMultipleKeywords(traductionMap(lang))
        $editor.model.document.on('change:data', () => {
            showWarningIfMultipleKeywords(traductionMap(lang))
        })
    }

    $('#language').on('change', () => {
        lang = (document.querySelector('#languages_dropdown') as HedySelect).selected[0]
    })

    // Autosave customize adventure page
    autoSave("customize_adventure")

    showWarningIfMultipleLevels()
    document.querySelectorAll('#levels_dropdown div div .option').forEach((el) => {
        el.addEventListener('click', () => {
            setTimeout(showWarningIfMultipleLevels, 100)
        })
    })
}
function showWarningIfMultipleLevels() {
    const numberOfLevels = (document.querySelector('#levels_dropdown') as HedySelect).selected.length;
    const numberOfSnippets = document.querySelectorAll('pre[data-language="Hedy"]').length
    if(numberOfLevels > 1 && numberOfSnippets > 0) {
        $('#warningbox').show()
    } else if(numberOfLevels <= 1 || numberOfSnippets === 0) {
        $('#warningbox').hide()
    }
}
function showWarningIfMultipleKeywords(TRADUCTION: Map<string, string>) {
    const content = DOMPurify.sanitize($editor.getData())
    const parser = new DOMParser();
    const html = parser.parseFromString(content, 'text/html');

    for (const tag of html.getElementsByTagName('code')) {
        if (tag.className !== "language-python") {
            const coincidences = findCoincidences(tag.innerText, TRADUCTION);
            if (coincidences.length > 1 && !keywordHasAlert.get(tag.innerText)) {
                keywordHasAlert.set(tag.innerText, true);
                // We create the alert box dynamically using the template element in the HTML object
                const template = document.querySelector('#warning_template') as HTMLTemplateElement
                const clone = template.content.cloneNode(true) as HTMLElement
                let close = clone.querySelector('.close-dialog');
                close?.addEventListener('click', () => {
                    keywordHasAlert.set(tag.innerText, false);
                    close?.parentElement?.remove()
                })
                let p = clone.querySelector('p[class^="details"]')!
                let message = ClientMessages['multiple_keywords_warning']
                message = message.replace("{orig_keyword}", formatKeyword(tag.innerText))
                let keywordList = ''
                for (const keyword of coincidences) {
                    keywordList = keywordList === '' ? formatKeyword(`${keyword}`) : keywordList + `, ${formatKeyword(`${keyword}`)}`
                }
                message = message.replace("{keyword_list}", keywordList)
                p.innerHTML = message
                // Once the warning has been created we append it to the container
                const warningContainer = document.getElementById('warnings_container')!
                warningContainer.appendChild(clone)
            }
        }
    }
}

function formatKeyword(name: string) {
    return `<span class='command-highlighted'>${name}</span>`
}

function findCoincidences(name: string, TRADUCTION: Map<string, string>) {
    let coincidences = [];
    for (const [key, regexString] of TRADUCTION) {
        if (new RegExp(`^(${regexString})$`, 'gu').test(name)) {
            coincidences.push(key)
        }
    }
    return coincidences;
}

function initializeEditor(language: string, editorContainer: HTMLElement, solutionExample=false): Promise<void> {
    return new Promise((resolve, reject) => {
        ClassicEditor
            .create(editorContainer, {
                codeBlock: {
                    languages: [
                        { language: 'python', label: 'Hedy', class: "language-python"},
                    ],
                },
                language,
            })
            .then(editor => {
                if (solutionExample) {
                    window.ckSolutionEditor = editor;
                } else {
                    window.ckEditor = editor;
                    $editor = editor;
                }
                editor.model.document.on("change:data", e => autoSave("customize_adventure", e))
                resolve();
            })
            .catch(error => {
                console.error(error);
                reject(error);
            });
    });
}

export function addCurlyBracesToCode(code: string, level: number, language: string = 'en') {
    // If code already has curly braces, we don't do anything about it
    if (code.match(/\{(\w|_)+\}/g)) return code

    let parser = PARSER_FACTORIES[level](language);
    let parseResult = parser.parse(code);
    let formattedCode = ''
    let previous_node: SyntaxNode | undefined = undefined

    // First we're going to iterate trhough the parse tree, but we're only interested in the set of node
    // that actually have code, meaning the leaves of the tree
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
                // In case that we have a case of a keyword that uses spaces, then we don't need
                // to include the keyword several times in the translation!
                // For example `if x not in list` should be `if x {not_in} list`
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
            // Commads signify start of lines, except for level 7, 8 repeats
            // In that case, don't add more than one new line
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

export function addCurlyBracesToKeyword(name: string) {
    let lang =  (document.querySelector('#languages_dropdown') as HedySelect).selected[0]
    let TRADUCTION = traductionMap(lang);

    for (const [key, regexString] of TRADUCTION) {
        if ((new RegExp(`^(${regexString})$`, 'gu').test(name)) || name === key) {
            return `{${key}}`
        }
    }

    return name;
}
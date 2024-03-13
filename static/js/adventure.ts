import ClassicEditor from "./ckeditor";
import { CustomWindow } from './custom-window';
import { languagePerLevel, keywords } from "./lezer-parsers/language-packages";
import { SyntaxNode } from "@lezer/common";
import { initializeTranslation } from "./lezer-parsers/tokens";
import { theKeywordLanguage } from "./app";

declare let window: CustomWindow;

export interface InitializeCustomizeAdventurePage {
    readonly page: 'customize-adventure';
}

let $editor: ClassicEditor;

export async function initializeCustomAdventurePage(_options: InitializeCustomizeAdventurePage) {
    const editorContainer = document.querySelector('#adventure-editor') as HTMLElement;
    const lang = document.querySelector('html')?.getAttribute('lang') || 'en';
    // Initialize the editor with the default language
    if (editorContainer) {
        initializeEditor(lang, editorContainer);
    }

    // We wait until Tailwind generates the select
    const tailwindSelects = await waitForElm('[data-te-select-option-ref]')
    tailwindSelects.forEach((el) => {
        el.addEventListener('click', () => {
            // After clicking, it takes some time for the checkbox to change state, so if we want to target the checkbox
            // that are checked after clicking we can't do that inmediately after the click
            // therofore we wait for 100ms
            setTimeout(function(){
                const numberOfLevels = document.querySelectorAll('[aria-selected="true"]').length;
                const numberOfSnippets = document.querySelectorAll('pre[data-language="Hedy"]').length
                if(numberOfLevels > 1 && numberOfSnippets > 0) {
                    $('#warningbox').show()
                } else if(numberOfLevels <= 1 || numberOfSnippets === 0) {
                    $('#warningbox').hide()
                }
            }, 100);
        })
    })
}

function initializeEditor(language: string, editorContainer: HTMLElement): Promise<void> {
    return new Promise((resolve, reject) => {
        if ($editor) {
            $editor.destroy();
        }

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
                window.ckEditor = editor;
                $editor = editor;
                resolve();
            })
            .catch(error => {
                console.error(error);
                reject(error);
            });
    });
}

export function addCurlyBracesToCode(code: string, level: number) {
    // If code already has curly braces, we don't do anything about it
    if (code.match(/\{(\w|_)+\}/g)) return code
    
    initializeTranslation({keywordLanguage: theKeywordLanguage, level: level})

    let parser = languagePerLevel[level];
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

function waitForElm(selector: string): Promise<NodeListOf<Element>>  {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelectorAll(selector));
        }

        const observer = new MutationObserver(_mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelectorAll(selector));
            }
        });

        // If you get "parameter 1 is not of type 'Node'" error, see https://stackoverflow.com/a/77855838/492336
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}
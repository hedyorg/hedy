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

function addEditorExplanationButton(editor: ClassicEditor, explanationId: string) {
    const toolbarItems = editor.ui.view.toolbar.element?.querySelector('.ck-toolbar__items') as HTMLElement | null;
    if (!toolbarItems) {
        return;
    }

    if (toolbarItems.querySelector('.hedy-editor-explanation-toggle')) {
        return;
    }

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'ck ck-button ck-off hedy-editor-explanation-toggle';
    button.setAttribute('aria-label', 'Toggle editor explanation');
    button.title = 'Editor explanation';
    button.innerHTML = '<svg class="ck ck-icon" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"></path></svg>';
    button.addEventListener('click', () => {
        const explanation = document.getElementById(explanationId);
        if (!explanation) {
            return;
        }
        explanation.classList.toggle('hidden');
    });

    toolbarItems.appendChild(button);
}

export async function initializeCustomAdventurePage(_options: InitializeCustomizeAdventurePage) {
    const editorContainer = document.querySelector('#adventure-editor') as HTMLElement | null;
    const editorSolutionExampleContainer = document.querySelector('#adventure-solution-editor') as HTMLElement | null;
    const languagesDropdown = document.querySelector('#languages_dropdown') as HedySelect | null;
    // Initialize the editor with the default language
    let lang = languagesDropdown?.selected?.[0] || 'en';

    if (editorContainer && editorSolutionExampleContainer) {
        await initializeEditor(lang, editorContainer);
        await initializeEditor(lang, editorSolutionExampleContainer, true);
        showWarningIfMultipleKeywords(traductionMap(lang))
        $editor.model.document.on('change:data', () => {
            showWarningIfMultipleKeywords(traductionMap(lang))
        })
    }

    $('#language').on('change', () => {
        const selectedLanguage = (document.querySelector('#languages_dropdown') as HedySelect | null)?.selected?.[0];
        if (selectedLanguage) {
            lang = selectedLanguage;
        }
    })

    // Autosave customize adventure page
    autoSave("customize_adventure")

    showWarningIfMultipleLevels()
    const levelOptions = document.querySelectorAll('#levels_dropdown div div .option');
    levelOptions.forEach((el) => {
        el.addEventListener('click', () => {
            setTimeout(showWarningIfMultipleLevels, 100)
        })
    })

    updateAdventureLevelsFromSwitches('customize_adventure');
    const levelSwitches = document.querySelectorAll('input[name="adventure_levels"]') as NodeListOf<HTMLInputElement>;
    levelSwitches.forEach((el) => {
        el.addEventListener('change', () => {
            showWarningIfMultipleLevels();
            const formElement = document.getElementById('customize_adventure') as HTMLFormElement | null;
            if (formElement) {
                update_adventure_redesign(formElement);
            }
        });
    });
}

function updateAdventureLevelsFromSwitches(formId: string) {
    const form = document.getElementById(formId) as HTMLFormElement | null;
    if (!form) {
        return;
    }

    const selected = Array.from(
        document.querySelectorAll('input[name="adventure_levels"]:checked')
    ).map((input) => (input as HTMLInputElement).value);

    form.dataset['adventureLevels'] = JSON.stringify(selected);

    const numberOfSnippets = document.querySelectorAll('pre[data-language="Hedy"]').length;
    if (selected.length > 1 && numberOfSnippets > 0) {
        $('#warningbox').show();
    } else {
        $('#warningbox').hide();
    }
}

function parseJsonStringArray(rawValue: string | undefined): string[] {
    if (!rawValue) {
        return [];
    }

    try {
        const parsed = JSON.parse(rawValue);
        if (!Array.isArray(parsed)) {
            return [];
        }
        return parsed.map((value) => String(value));
    } catch {
        return [];
    }
}

function getAdventureNameFromPage(fallback: string): string {
    const title = document.querySelector('h1');
    const titleText = title?.firstChild?.textContent?.trim();
    return titleText || fallback;
}

function getSelectedAdventureLevels(formElement: HTMLFormElement): string[] {
    const selectedSwitches = Array.from(document.querySelectorAll('input[name="adventure_levels"]:checked')) as HTMLInputElement[];
    if (selectedSwitches.length > 0) {
        return selectedSwitches.map((input) => input.value);
    }

    const levelsDropdown = document.querySelector('#levels_dropdown') as HedySelect | null;
    if (levelsDropdown?.selected?.length) {
        return levelsDropdown.selected.map((value) => String(value));
    }

    return parseJsonStringArray(formElement.dataset['adventureLevels']);
}

function getFormattedAdventureContent(content: string, levels: string[], language: string): string {
    if (!content) {
        return '';
    }

    const html = new DOMParser().parseFromString(content, 'text/html');
    const snippets = html.querySelectorAll('pre[data-language="Hedy"]') || [];
    const snippetsFormatted = [];
    const keywordsFormatted = [];
    const minLevel = levels.map((value) => parseInt(value, 10)).reduce((a, b) => Math.min(a, b), Infinity);

    for (const el of snippets) {
        snippetsFormatted.push(el.textContent || '');
    }

    for (const el of html.querySelectorAll('code:not(pre code)')) {
        keywordsFormatted.push(el.textContent || '');
    }

    for (let i = 0; i < snippets.length; i++) {
        snippetsFormatted[i] = addCurlyBracesToCode(snippetsFormatted[i], minLevel, language || 'en');
    }

    for (let i = 0; i < keywordsFormatted.length; i++) {
        keywordsFormatted[i] = addCurlyBracesToKeyword(keywordsFormatted[i]);
    }

    let i = 0;
    let j = 0;
    for (const tag of html.getElementsByTagName('code')) {
        if (tag.className === 'language-python') {
            tag.innerText = snippetsFormatted[i++] || '';
        } else {
            tag.innerText = keywordsFormatted[j++] || '';
        }
    }

    return html.getElementsByTagName('body')[0].outerHTML.replace(/<br>/g, '\n');
}

export function update_adventure_redesign(formElement: HTMLFormElement) {
    const adventureId = formElement.dataset['adventureId'];
    if (!adventureId) {
        return;
    }

    const levels = getSelectedAdventureLevels(formElement);
    if (levels.length === 0) {
        return;
    }

    const classes = parseJsonStringArray(formElement.dataset['adventureClasses']);
    const language = (document.querySelector('#languages_dropdown') as HedySelect | null)?.selected?.[0]
        || formElement.dataset['adventureLanguage']
        || 'en';
    const fallbackName = formElement.dataset['adventureName'] || '';
    const adventureName = getAdventureNameFromPage(fallbackName);
    const isPublic = formElement.dataset['adventurePublic'] === '1' || formElement.dataset['adventurePublic'] === 'true';

    const content = DOMPurify.sanitize(window.ckEditor?.getData() || '');
    const solutionExample = DOMPurify.sanitize(window.ckSolutionEditor?.getData() || '');

    const formattedContent = getFormattedAdventureContent(content, levels, language);
    const formattedSolution = getFormattedAdventureContent(solutionExample, levels, language);

    $.ajax({
        type: 'POST',
        url: '/for-teachers/customize-adventure',
        data: JSON.stringify({
            id: adventureId,
            name: adventureName,
            content: content,
            formatted_content: formattedContent,
            formatted_solution_code: formattedSolution,
            public: isPublic,
            language,
            classes,
            levels,
        }),
        contentType: 'application/json',
        dataType: 'json'
    }).fail(function (err) {
        console.error('Could not autosave redesign adventure', err);
    });
}

function showWarningIfMultipleLevels() {
    const levelSwitches = document.querySelectorAll('input[name="adventure_levels"]:checked');
    let numberOfLevels = levelSwitches.length;

    if (numberOfLevels === 0) {
        const levelsDropdown = document.querySelector('#levels_dropdown') as HedySelect | null;
        numberOfLevels = levelsDropdown?.selected?.length || 0;
    }

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
                    addEditorExplanationButton(editor, 'explanation_solution');
                } else {
                    window.ckEditor = editor;
                    $editor = editor;
                    addEditorExplanationButton(editor, 'explanation');
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

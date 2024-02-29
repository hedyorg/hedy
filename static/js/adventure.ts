import ClassicEditor from "./ckeditor";
import { CustomWindow } from './custom-window';

declare let window: CustomWindow;


let $editor: ClassicEditor;
const editorContainer = document.querySelector('#adventure-editor') as HTMLElement;
const lang = document.querySelector('html')?.getAttribute('lang') || 'en';
// Initialize the editor with the default language
if (editorContainer) {
    initializeEditor(lang);
}

function initializeEditor(language: string): Promise<void> {
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

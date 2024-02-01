// @ts-ignore
// import CKEditorInspector from '@ckeditor/ckeditor5-inspector';

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
                // hljs.highlightAll();

                resolve();
            })
            .catch(error => {
                console.error(error);
                reject(error);
            });
    });
}


// Update the editor with new data
// export async function update_adv_editor(js: any) {
//     try {
//         if (js.lang !== 'en') {
//             await initializeEditor(js.lang);
//         }
//         $editor.setData(js.content);
        
        
//         const prePattern = /<pre[^>]*>(.*?)<\/pre>/gs;
//         const matches = js.content.match(prePattern);

//         let content = "";
//         if (matches) {
//             for (const match of matches) {
//                 // Extract content within <pre> tags
//                 const contentMatch = /<pre[^>]*>(.*?)<\/pre>/s.exec(match);
//                 if (contentMatch) {
//                     content += contentMatch[1].trim();
//                 }
//             }
//         }
            
//         console.log("content", content)

        
//         for (const codeBlock of document.querySelectorAll('.ck pre')) {
//             console.log('a block here:', codeBlock)
//             const exampleEditor = editorCreator.initializeReadOnlyEditor(codeBlock as HTMLElement, 'ltr');
//             exampleEditor.contents = content.trimEnd();        
//             for (const level of [1,2,3,4]) {
//               initializeTranslation({
//                 keywordLanguage: js.lang,
//                 level: level,
//               })
//               exampleEditor.setHighlighterForLevel(level);                

//             }
//         }
        


//     } catch (error) {
//         // Handle initialization error
//         console.error(error);
//     }
// }
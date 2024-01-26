import ClassicEditor from "./ckeditor";

const editor = document.querySelector('#adventure-editor') as HTMLElement;

export function initialize_adv_editor(js: any) {

    if (editor) {
        ClassicEditor.create(editor, {
            initialData: js.content,
            language: js.lang,
            
            codeBlock: {
                languages: [
                    { language: 'python', label: 'Hedy', class: "hedy", },
                ]
            },
        })
        .then( editor => {
            console.log( editor );
            (window as any).ckEditor = editor;
            // TODO: make sure to highlight Hedy code.

        } )
        .catch( error => {
            console.error( error );
        } );
    }
}
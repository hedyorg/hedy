import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

/*
    In this file, you could define any additional variables
    that you need to attach to the window object, otherwise
    TS will complain that window doesn't have such variables.
*/
export interface CustomWindow extends Window {
    ckEditor: ClassicEditor;
}
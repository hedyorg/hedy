import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

export interface CustomWindow extends Window {
    ckEditor: ClassicEditor;
}
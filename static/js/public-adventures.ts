import { initialize } from "./initialize";

document.addEventListener("updateTSCode", (e: any) => {
    console.log('updateTSCode', e);
    const js = e.detail;
    initialize({
        lang: js.lang,
        level: parseInt(js.level),
        keyword_language: js.lang,
        javascriptPageOptions: js
    });
})

import { HedySelect } from "./custom-elements";
import { initialize } from "./initialize";

function updateURL() {
    const levelSelect = document.getElementById("level_select") as HedySelect;
    const languageSelect = document.getElementById("language_select") as HedySelect;
    const tagsSelect = document.getElementById("tag_select") as HedySelect;
    const searchInput = document.getElementById('search_adventure') as HTMLInputElement;
    
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const level = levelSelect.selected[0];
    const language = languageSelect.selected[0];
    const tags = tagsSelect.selected.join(',');

    urlParams.set('level', level)
    urlParams.set('lang', language)
    urlParams.set('tag', tags)
    if (searchInput) {
        urlParams.set('search', searchInput.value)
    }
    window.history.pushState({}, '', `${window.location.pathname}?${urlParams.toString()}`);
}


document.addEventListener("updateTSCode", (e: any) => {
    setTimeout(() => {
        const js = e.detail;
        updateURL();
        initialize({
            lang: js.lang, level: parseInt(js.level), keyword_language: js.lang,
            javascriptPageOptions: js
        });
    }, 1000);
})
import { initialize } from "./initialize";

let levelSelect: HTMLElement;
let languageSelect: HTMLElement;
let tagsSelect: HTMLElement;
let searchInput: HTMLInputElement;

function initializeVariables() {
    // Get and initialize needed variables
    levelSelect = document.getElementById("level-select") as HTMLElement;
    languageSelect = document.getElementById("language-select") as HTMLElement;
    tagsSelect = document.getElementById("tag-select") as HTMLElement;
    searchInput = document.getElementById('search_adventure') as HTMLInputElement;
}

function updateURL() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const level = levelSelect.getAttribute("data-value") || "";
    const lanugage = languageSelect.getAttribute("data-value") || "";
    const tags = tagsSelect.getAttribute("data-value") || "";

    urlParams.set('level', level)
    urlParams.set('lang', lanugage)
    urlParams.set('tag', tags)
    if (searchInput) {
        urlParams.set('search', searchInput.value)
    }
    window.history.pushState({}, '', `${window.location.pathname}?${urlParams.toString()}`);

}


document.addEventListener("updateTSCode", (e: any) => {
    setTimeout(() => {
        initializeVariables();
        const js = e.detail;

        updateURL();
        initialize({
            lang: js.lang, level: parseInt(js.level), keyword_language: js.lang,
            javascriptPageOptions: js
        });
    }, 1000);
})
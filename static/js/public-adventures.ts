import { Select } from "tw-elements";
import { modal } from './modal';
import { initialize } from "./initialize";
import { initializeHighlightedCodeBlocks } from "./app";
import { postJson } from "./comm";

// Get and initialize needed variables
const level = document.getElementById("level");
const language = document.getElementById("language");
const tags = document.getElementById("tag");

const searchInput = document.getElementById('search_adventure') as HTMLInputElement | null;
let searchTimeout: NodeJS.Timeout;

const levelInstance = Select.getInstance(level);
const languageInstance = Select.getInstance(language);
const tagsInstance = Select.getInstance(tags);

// Attach needed events for updating the DOM 
level?.addEventListener('valueChange.te.select', updateDOM)
language?.addEventListener('valueChange.te.select', updateDOM)
tags?.addEventListener('valueChange.te.select', updateDOM)
searchInput?.addEventListener('input', handleSearchInput);

document.addEventListener("DOMContentLoaded", () => {
    updateDOM()
    setTimeout(() => {
        if (!levelInstance)
            return
        // Since we render html as a string, the js is lost and thus any js needed
        // has to be applied again.
        const cloneBtn = document.getElementById(`clone_adventure_btn_${levelInstance.value}`);
        cloneBtn?.addEventListener('click', handleCloning);
    }, 500)
})


async function handleCloning(e: MouseEvent) {
    const target = e.target as HTMLElement;
    const adventureId = target.getAttribute("data-id");
    try {
        const data = await postJson(`public-adventures/clone/${adventureId}`);
        modal.notifySuccess(data.message)
        await updateDOM();
    } catch (error: any) {
        modal.notifyError(error.responseText)
    }
}

function handleSearchInput() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(updateDOM, 500);
}


function updateURL() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    urlParams.set('level', levelInstance.value)
    urlParams.set('lang', languageInstance.value)
    urlParams.set('tag', tagsInstance.value)
    if (searchInput) {
        urlParams.set('search', searchInput.value)
    }
    window.history.pushState({}, '', `${window.location.pathname}?${urlParams.toString()}`);

}

async function updateDOM() {
    if (!levelInstance || !languageInstance || !tagsInstance)
        return
    // Since the select has no default values, we don't want to pass undefined to the backend.
    const level = levelInstance.value ? levelInstance.value : ""
    const response = await fetch(`public-adventures/filter?tag=${tagsInstance.value}`
                    + `&lang=${languageInstance.value}&level=${level}`
                    + `&search=${searchInput?.value}`, {
      method: 'GET',
      keepalive: true,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
      },
    });
    const { html, js } = await response.json()
    updateURL()

    const publicAdventuresBody = document.getElementById('public-adventures-body') ;
    if (publicAdventuresBody) {
        publicAdventuresBody.innerHTML = html

        // Since we render html as a string, the js is lost and thus any js needed
        // has to be applied again.
        initialize({lang: js.lang, level: js.level, keyword_language: js.lang,
            javascriptPageOptions: js})

        initializeHighlightedCodeBlocks(publicAdventuresBody)
        
        const cloneBtn = document.getElementById(`clone_adventure_btn_${levelInstance.value}`);
        cloneBtn?.addEventListener('click', handleCloning);
    }
}
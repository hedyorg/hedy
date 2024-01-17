import { Select } from "tw-elements";
import { modal } from './modal';
import { initialize } from "./initialize";
import { initializeHighlightedCodeBlocks } from "./app";
import { postJson } from "./comm";

export function cloned(message: string, success: Boolean = true) {
    if (success) {
        modal.notifySuccess(message)
    } else {
        modal.notifyError(message)
    }
}

export function applyFilter(term: string, type: string, filtered: any) {
    term = term.trim()
    filtered[type] = filtered[type] || {exclude: []}
    filtered[type]['term'] = term
    const filterExist = (<HTMLInputElement>document.querySelector('#search_adventure')).value ||
        (<HTMLInputElement>document.querySelector('#language')).value ||
        (<HTMLInputElement>document.querySelector('#tag')).value
    

    if (!term) {
        filtered[type] = {term, exclude: []}
    }
    const adventures = document.querySelectorAll('.adventure')

    if (!filterExist) {
        for (const adv of adventures) {
            adv.classList.remove('hidden')
        }
        filtered = {}
        return
    }
    for (const adv of adventures) {
        let toValidate;
        let skip = false;
        if (type === 'search') {
            toValidate = adv.querySelector('.name')?.innerHTML
        } else if (type === 'lang') {
            toValidate = adv.getAttribute('data-lang')
        } else {
            const advTags = adv.querySelector('#tags-list')?.children || []
            for (const t of advTags) {
                const value = t.innerHTML.trim()
                if (term.includes(value)) {
                    if (filtered[type].exclude.some((a: Element) => a === adv)) {
                        filtered[type].exclude = filtered[type].exclude.filter((a: Element) => a !== adv)
                    }
                    skip = true; // at least one tag is found in the current adventure.
                    break
                }
            }
        }
        if (skip)
            continue;

        if (term && toValidate?.includes(term)) {
            if (filtered[type].exclude.some((a: Element) => a === adv)) {
                filtered[type].exclude = filtered[type].exclude.filter((a: Element) => a !== adv)
            }
        } else if (term) {
            if (filtered.term !== term && !filtered[type].exclude.some((a: Element) => a === adv)) {
                filtered[type].exclude.push(adv)
            }
        }
    }

    for (const adv of adventures) {
        let allFiltersPassed = true;
        for (const t in filtered) {
            if (filtered[t].exclude.some((a: Element) => a === adv)) {
                allFiltersPassed = false;
            }
        }
        if (allFiltersPassed) {
            adv.classList.remove('hidden')
        } else {
            adv.classList.add('hidden')
        }
    }
}

declare global {
    interface Window {
        $filtered: any;
    }
}


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
    const response = await fetch(`public-adventures/filter?tag=${tagsInstance.value}`
                    + `&lang=${languageInstance.value}&level=${levelInstance.value}`
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
    if (js.state_changed && publicAdventuresBody) {
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
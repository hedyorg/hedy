import { modal } from './modal';
import { initialize } from "./initialize";
import { initializeHighlightedCodeBlocks } from "./app";
import { postJson } from "./comm";

// Get and initialize needed variables
const levelSelect = document.getElementById("level-select") as Element;
const languageSelect = document.getElementById("language-select") as Element;
const tagsSelect = document.getElementById("tag-select") as Element;

const searchInput = document.getElementById('search_adventure') as HTMLInputElement | null;
let searchTimeout: NodeJS.Timeout;

searchInput?.addEventListener('input', handleSearchInput);

document.addEventListener("DOMContentLoaded", () => {

    const options = document.querySelectorAll('.option');

    options.forEach(function (option) {
        option.addEventListener('click', function () {
            const dropdown = option.closest(".dropdown") as Element;
            if (!dropdown) {
                return;
            }
            const isSingleSelect = dropdown?.getAttribute('data-type') === 'single';

            if (isSingleSelect && !option.classList.contains('selected')) {
                // Deselect other options within the same dropdown
                const otherOptions = dropdown.querySelectorAll('.option.selected');
                otherOptions.forEach(otherOption => otherOption.classList.remove('selected'));
            }

            // Update value of the relative select dropdown.
            let nextValue = dropdown.getAttribute("data-value") as string;
            if (option.classList.contains("selected")) {
                nextValue = nextValue?.replace(option.getAttribute("data-value") as string, "") as string;
                if (!isSingleSelect) {
                    nextValue = nextValue.split(",").filter(v => v).join(","); // remove standalone ,
                } else {
                    // it's selected and dropdown is single, so skip and do nothing.
                    return;
                }
            } else if (!isSingleSelect) {
                const currentValue = dropdown.getAttribute("data-value") || "";
                nextValue = [currentValue, option.getAttribute("data-value") || ""].filter(v => v).join(",");
            } else {
                nextValue =  option.getAttribute("data-value") || "";
            }
            dropdown.setAttribute("data-value", nextValue)
            option.classList.toggle('selected');

            updateLabelText(dropdown);
            updateDOM()
        });
    });
    
    
    
    
    updateDOM()
    setTimeout(() => {
        if (!levelSelect)
            return
        // Since we render html as a string, the js is lost and thus any js needed
        // has to be applied again.
        const level = levelSelect.getAttribute("data-value") || "";
        const cloneBtn = document.getElementById(`clone_adventure_btn_${level}`);
        cloneBtn?.addEventListener('click', handleCloning);
    }, 500)
})


function getSelectedOptions(_options: NodeListOf<Element>) {
    return Array.from(_options)
        .filter(option => option.classList.contains('selected'))
        .map(option => option.textContent?.trim());
}


function updateLabelText(dropdown: Element) {
    const toggleButton = dropdown.querySelector('.toggle-button') as Element;
    const relativeOptions = dropdown.querySelectorAll(".option") as NodeListOf<Element>;
    const label = toggleButton.querySelector(".label") as Element;
    const selectedOptions = getSelectedOptions(relativeOptions);
    label.textContent = selectedOptions.length === 0 ? label.getAttribute("data-value") : selectedOptions.join(', ');
}



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

async function updateDOM() {
    if (!levelSelect || !languageSelect || !tagsSelect)
        return
    // Since the select has no default values, we don't want to pass undefined to the backend.
    const level = levelSelect.getAttribute("data-value") || "";
    const lanugage = languageSelect.getAttribute("data-value") || "";
    const tags = tagsSelect.getAttribute("data-value") || "";
    const response = await fetch(`public-adventures/filter?tag=${tags}`
                    + `&lang=${lanugage}&level=${level}`
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
        
        const cloneBtn = document.getElementById(`clone_adventure_btn_${level}`);
        cloneBtn?.addEventListener('click', handleCloning);
    }
}
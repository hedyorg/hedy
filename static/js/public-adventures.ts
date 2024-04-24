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

document.addEventListener("DOMContentLoaded", prepareDropdowns);

function prepareDropdowns() {
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
        });
    });
}
    

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
        prepareDropdowns();
        initialize({lang: js.lang, level: parseInt(js.level), keyword_language: js.lang,
            javascriptPageOptions: js
            });
    }, 1000);
})
import { ClientMessages } from "./client-messages";
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

// document.addEventListener("DOMContentLoaded", prepareDropdowns);

function prepareDropdowns() {
    const options = document.querySelectorAll('.option');
    const dropdowns = document.querySelectorAll("[data-dropdown-initialize]");
    dropdowns.forEach((dropdown) => {
        updateLabelText(dropdown)
    })
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

            if (!isSingleSelect && option.getAttribute("data-value") === "select_all") {
                const selected = !option.classList.contains("selected")
                const otherOptions = dropdown.querySelectorAll('.option');
                otherOptions.forEach(otherOption => {
                    if (otherOption.getAttribute('data-value') === 'select_all') return
                    otherOption.classList.toggle('selected', selected)
                });
            } else {
                dropdown.querySelector('.option[data-value="select_all"]')?.classList.remove('selected')
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
                nextValue = option.getAttribute("data-value") || "";
            }
            dropdown.setAttribute("data-value", nextValue)
            option.classList.toggle('selected');
            dropdown.dispatchEvent(new Event('change', { bubbles: true }))
            updateLabelText(dropdown);
        });
    });
}


function getSelectedOptions(_options: NodeListOf<HTMLElement>) {
    return Array.from(_options)
        .filter(option => option.classList.contains('selected') && option.dataset['value'] !== 'select_all')
        .map(option => option.textContent?.trim());
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
        initialize({
            lang: js.lang, level: parseInt(js.level), keyword_language: js.lang,
            javascriptPageOptions: js
        });
    }, 1000);
})

export class HedySelect extends HTMLElement {
    multiple: boolean = false;
    
    constructor() {
        super();
    }
    connectedCallback() {
        const template = document.getElementById('hedy_select') as HTMLTemplateElement;
        const clone = template.content.cloneNode(true) as HTMLElement;
        this.appendChild(clone);
        const select = this.querySelector('select');

        if (select === null) {
            throw new Error('Expected an inner select to go with the hedy-select component!')
        }

        select.hidden = true;
        const options = select.querySelectorAll('option');
        const dropdownMenu = this.querySelector('.dropdown-menu')!;
        this.multiple = select.multiple;
        this.dataset['type'] = select.multiple ? 'multiple' : 'single';
        if (select.multiple) {
            const newDiv = document.createElement('div');
            newDiv.classList.add('option');
            newDiv.innerHTML = ClientMessages['select_all'];
            newDiv.dataset['value'] = 'select_all';
            dropdownMenu.appendChild(newDiv)
            newDiv.addEventListener('click', this.onOptionClick)
        }

        for (const option of options) {
            const newDiv = document.createElement('div');
            newDiv.classList.add('option');
            newDiv.innerHTML = option.innerText;
            newDiv.dataset['value'] = option.value;
            newDiv.classList.toggle('selected', option.selected);
            dropdownMenu.appendChild(newDiv)
            newDiv.addEventListener('click', this.onOptionClick)
        }
        updateLabelText(this.querySelector('.dropdown')!)
    }

    onOptionClick(this: HTMLDivElement, _event: MouseEvent) {        
        const select = this.closest("hedy-select") as Element;
        if (!select) {
            return;
        }
        const isSingleSelect = select?.getAttribute('data-type') === 'single';
    
        if (isSingleSelect && !this.classList.contains('selected')) {
            // Deselect other options within the same dropdown
            const otherOptions = select.querySelectorAll('.option.selected');
            otherOptions.forEach(otherOption => otherOption.classList.remove('selected'));
        }
    
        if (!isSingleSelect && this.getAttribute("data-value") === "select_all") {
            const selected = !this.classList.contains("selected")
            const otherOptions = select.querySelectorAll('.option');
            otherOptions.forEach(otherOption => {
                if (otherOption.getAttribute('data-value') === 'select_all') return
                otherOption.classList.toggle('selected', selected)
            });
        } else {
            select.querySelector('.option[data-value="select_all"]')?.classList.remove('selected')
        }
        this.classList.toggle('selected');
        select.dispatchEvent(new Event('change', { bubbles: true }))
        updateLabelText(select);
        return;
    }

    get selected() {
        let selected: string[] = []
        this.querySelectorAll('.option.selected').forEach((el) => {
            if (el.getAttribute("data-value") !== 'select_all') {
                selected.push(el.getAttribute("data-value") as string)
            }
        })
        return selected;
    }
}

function updateLabelText(dropdown: Element) {
    const toggleButton = dropdown.querySelector('.toggle-button') as Element;
    const relativeOptions = dropdown.querySelectorAll(".option") as NodeListOf<HTMLElement>;
    const label = toggleButton.querySelector(".label") as Element;
    const selectedOptions = getSelectedOptions(relativeOptions);
    let text: string;
    if (selectedOptions.length === 0) {
        text = label.getAttribute("data-value")!
    } else if (selectedOptions.length < 6) {
        text = selectedOptions.join(', ')
    } else {
        text = `${selectedOptions.length} ${ClientMessages['selected']}`
    }
    label.textContent = text;
}
customElements.define('hedy-select', HedySelect)


export function toggleDropdown(event: Event) {
    let element = event.target as HTMLElement;
    if (element.tagName === 'SPAN') {
        element = element.parentElement!
    }
    const dropdown = element.parentElement?.querySelector('.dropdown-menu');
    if (dropdown === undefined || dropdown === null) {
        throw new Error('Unexpected error!');
    }
    $(dropdown).slideToggle('medium');
}
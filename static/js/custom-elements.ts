import { ClientMessages } from "./client-messages";

export class HedySelect extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        const template = document.getElementById('hedy_select') as HTMLTemplateElement;
        const clone = template.content.cloneNode(true) as HTMLElement;
        this.appendChild(clone);
        const options = this.querySelectorAll('option');
        const label = this.dataset['label'] || '';       
        const dropdownMenu = this.querySelector('.dropdown-menu')!;                
        if (this.dataset['type'] === 'multiple') {
            const newDiv = document.createElement('div');
            newDiv.classList.add('option');
            newDiv.innerHTML = ClientMessages['select_all'];
            newDiv.dataset['value'] = 'select_all';
            dropdownMenu.appendChild(newDiv)
            newDiv.addEventListener('click', this.onOptionClick)
        }
        for (const option of options) {
            option.hidden = true;
            const newDiv = document.createElement('div');
            newDiv.classList.add('option');
            newDiv.innerHTML = option.innerText;
            newDiv.dataset['value'] = option.value;
            newDiv.classList.toggle('selected', option.selected);
            dropdownMenu.appendChild(newDiv)
            newDiv.addEventListener('click', this.onOptionClick)
            for(const attribute of option.attributes) {
                if(attribute.name.includes('hx-')) {
                    newDiv.setAttribute(attribute.name, attribute.value);
                } else if(attribute.name == "data-cy") {
                    newDiv.setAttribute(attribute.name, attribute.value);
                    option.removeAttribute(attribute.name);
                }
            }
        }
        const span = this.getElementsByTagName('span')
        if (span.length !== 1) {
            throw new Error('HedySelect should only have one span element!');
        }        
        span[0].dataset['value'] = label;
        span[0].textContent = label;
        updateLabelText(this.querySelector('.dropdown')!)
    }

    onOptionClick(this: HTMLDivElement, _event: MouseEvent) {        
        const select = this.closest("custom-select") as Element;
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

function getSelectedOptions(_options: NodeListOf<HTMLElement>) {
    return Array.from(_options)
        .filter(option => option.classList.contains('selected') && option.dataset['value'] !== 'select_all')
        .map(option => option.textContent?.trim());
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

document.addEventListener("click", (e) => {
    let dropdowns = [...document.getElementsByClassName('dropdown-menu')]
    let target = e.target as HTMLElement;
    const dropdown = target.closest('.dropdown-menu') || target.closest('.dropdown');    
    if (!dropdown) {
        dropdowns.forEach((dropdown) => {
            if ($(dropdown).is(":hidden")) return;
            $(dropdown).slideToggle("medium");
        })
    }
});

customElements.define('custom-select', HedySelect)
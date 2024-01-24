import { Select } from "tw-elements";
import { modal } from './modal';

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

const tags = document.getElementById("tag");
const tagsInstance = Select.getInstance(tags);
tags?.addEventListener('valueChange.te.select', () => {
    const value = tagsInstance.value.join(",")
    applyFilter(value.replaceAll(",", " "), "tags", window.$filtered || {})
})
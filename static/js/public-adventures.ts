
export function applyFilter(term: string, type: string, filtered: any) {
    term = term.trim()
    filtered[type] = filtered[type] || {term, exclude: []}
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
        if (type === 'search') {
            toValidate = adv.querySelector('.name')?.innerHTML
        } else if (type === 'lang') {
            toValidate = adv.getAttribute('data-lang')
        } else {
            const tags = adv.querySelector('#tags-list')?.children || []
            const tagNames = []
            for (const t of tags) {
                tagNames.push(t.innerHTML)
            }
            toValidate = tagNames.join(' ')
        }

        if (term && toValidate?.includes(term)) {
            if (filtered[type].exclude.some((a: Element) => a === adv)) {
                filtered[type].exclude = filtered[type].exclude.filter((a: Element) => a !== adv)
            }
        } 
        else if (term) {
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
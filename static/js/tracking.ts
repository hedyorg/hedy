const ELEMENT_TO_TRACK = [
    "debug_button",
    "developers_toggle_container",
];
export function initializeTracking() {
    document.addEventListener('click', trackEvent);
    document.addEventListener('change', trackEvent);
}

function trackEvent(event: Event) {
    const target = event.target as HTMLElement;

    console.log(target, event.type)
    if (target.matches('button') || target.matches('a') || target.matches('input') || target.matches('select') || target.matches("div")) {
        let elementIdOrName = target.id;

        if (!elementIdOrName && target.hasAttribute("name")) {
            elementIdOrName = target.getAttribute("name") || "";
        }

        if (ELEMENT_TO_TRACK.includes(elementIdOrName)) {

            console.log(target)
            console.log(`Event: ${event.type}, Element ID or Name: ${elementIdOrName}`);
            
            // You can perform additional tracking or send the data to your server here
        } 


    }
}





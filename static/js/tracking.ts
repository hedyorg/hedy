const ELEMENT_TO_TRACK = [
    // Debug and Developer buttons
    "debug_button",
    "developers_toggle",

    // Cheatsheet buttons
    "dropdown_chetsheet_button",
    "try_button1",
    "try_button2",
    "try_button3",
    "try_button4",
    "try_button5",
    "try_button6",

    // Dropdowns and Toggles
    "speak_dropdown",
    "language-dropdown",
    "commands_dropdown",
    "keyword_toggle",

    // Level buttons
    "level_button_1",
    "level_button_2",
    "level_button_3",
    "level_button_4",
    "level_button_5",
    "level_button_6",
    "level_button_7",
    "level_button_8",
    "level_button_9",
    "level_button_10",
    "level_button_11",
    "level_button_12",
    "level_button_13",
    "level_button_14",
    "level_button_15",
    "level_button_16",
    "level_button_17",
    "level_button_18",

    // Class and Adventure buttons
    "create_class_button",
    "create_adventure_button",
    "public-adventures-link",
    "to_class_button",
    "customize_class_button",
    "go_back_to_teacher_page_button",
    "live_stats_button",
    "grid_overview_button",
    

    // Info buttons
    "classes_info",
    "adventures_info",
    "slides_info",
    "download-slides-2",
    "download-slides-3",
    "download-slides-4",
    "download-slides-5",
    "download-slides-6",
    "download-slides-7",
    "download-slides-8",
    "download-slides-9",
    "download-slides-10",
    "download-slides-11",
    "download-slides-12",
    "download-slides-13",
    "download-slides-14",
    "download-slides-15",
    "download-slides-16",
    "download-slides-17",
    "download-slides-18",

    // Explore page buttons
    "explore_page_adventure",
    "explore_page_level"
];
export function initializeTracking() {
    document.addEventListener('click', trackEvent);
    document.addEventListener('change', trackEvent);
}

const clickCounts = Object();
function trackEvent(event: Event) {
    const target = event.target as HTMLElement;
    console.log(target, event.type)
    if (target.matches('button') || target.matches('a') || target.matches('input') || target.matches('select') || target.matches("div")) {
        let elementIdOrName = target.id;

        if (!elementIdOrName && target.hasAttribute("name")) {
            elementIdOrName = target.getAttribute("name") || "";
        }

        if (ELEMENT_TO_TRACK.includes(elementIdOrName)) {
            

            if (clickCounts[elementIdOrName]) {
                clickCounts[elementIdOrName] = clickCounts[elementIdOrName] + 1;
            } 
            else {
                clickCounts[elementIdOrName] = 0;
            }
            

            console.log(target)
            console.log(`Event: ${event.type}, Element ID or Name: ${elementIdOrName}, Click Count: ${clickCounts[elementIdOrName]}`);
           


            
            
            // You can perform additional tracking or send the data to your server here
        } 


    }
    console.log(clickCounts)
}

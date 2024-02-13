import { postJson } from "./comm";

// const WAITING_TIME = 5 * 60 * 1000; // 5min in milliseconds
const WAITING_TIME = 3000; // 3s for testing
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
const CLICK_COUNTS = "clickCounts";
const LAST_ACTIVE = "lastActiveTime";
const INTERVAL_KEY = "interval";


let clickCounts: any = [];
let lastActiveTime = Date.now();
let changesSent = false;


export function initializeTracking() {
    document.addEventListener("DOMContentLoaded", documentLoaded);
}

function documentLoaded() {
    // attach events
    document.addEventListener('click', trackEvent);
    document.addEventListener('change', trackEvent);

    // initialize variables
    clickCounts = handleLocalStorage(CLICK_COUNTS);
    lastActiveTime = handleLocalStorage(LAST_ACTIVE, Date.now());

    removeTrackingInterval(); // Possibly removing lingering ones.
    setTrackingInterval(); // Resume with fresh timer
}

function removeTrackingInterval() {
    const storedData = localStorage.getItem(INTERVAL_KEY);
    if (storedData) {
        try {
            const parsedData = JSON.parse(storedData);
            clearInterval(parsedData.id); // Clear any potentially lingering timer
            console.log(parsedData.id, " interval was removed")
        } catch (error) {
            console.error("Error parsing tracking interval data:", error);
        }
    }

}

function setTrackingInterval() {
  const timerId = setInterval(checkUserActivity, WAITING_TIME);
  localStorage.setItem(INTERVAL_KEY, JSON.stringify({ id: timerId, timestamp: Date.now() }));
}


async function trackEvent(event: Event) {
    // the following check is necessary since some elements issue click and change events.
    const currentTime = Date.now();
    const inactiveDuration = currentTime - lastActiveTime;
    if (inactiveDuration <= 200) {
        return;
    }
    const target = event.target as HTMLElement;
    // console.log(target, event.type)
    if (target.matches('button') || target.matches('a') || target.matches('input') || target.matches('select') || target.matches("div")) {
        let elementIdOrName = target.id;

        if (!elementIdOrName && target.hasAttribute("name")) {
            elementIdOrName = target.getAttribute("name") || "";
        }

        if (ELEMENT_TO_TRACK.includes(elementIdOrName)) {
            clickCounts = handleLocalStorage(CLICK_COUNTS);
            
            const page = window.location.pathname;

            const value = (target as HTMLInputElement).value || "";

            clickCounts.push({time: currentTime, id: elementIdOrName, page, extra: value});
            
            console.log(target, clickCounts)
            console.log(`Event: ${event.type}, Element ID or Name: ${elementIdOrName}, Click Count: ${clickCounts}`);
            handleUserActivity(clickCounts);
        } 
    }
}

// Function to handle user activity
function handleUserActivity(clickCounts: any) {
    lastActiveTime = handleLocalStorage(LAST_ACTIVE, Date.now());
    clickCounts = handleLocalStorage(CLICK_COUNTS, clickCounts);
    changesSent = false;
}

// Retrieve or set items in local storage.
function handleLocalStorage(item: string, value: any = undefined) {
    const retrievedItem = window.localStorage.getItem(item);
    if (!retrievedItem || value !== undefined) {
        value = value || [];
        window.localStorage.setItem(item, JSON.stringify(value));
    } else {
        if (item === CLICK_COUNTS) {
            value = JSON.parse(retrievedItem);
        } else if (item === LAST_ACTIVE) {
            value = parseInt(retrievedItem);
        }
    }
    return value;
}

// Function to check user activity and send request if inactive for 5 minutes
async function checkUserActivity() {
    if (changesSent) {
        // Perhaps add current page with no action by the user.
        // clickCounts = handleLocalStorage(CLICK_COUNTS);
        // const page = window.location.pathname;
        // clickCounts.push({time: lastActiveTime, id: '', page});
        // handleUserActivity(clickCounts);
        return;
    }
    const currentTime = Date.now();
    const inactiveDuration = currentTime - lastActiveTime;
    if (inactiveDuration >= WAITING_TIME) {
        sendRequestToServer();
    }
}

// Function to send request to the server
async function sendRequestToServer() {
    try {
        const data = handleLocalStorage(CLICK_COUNTS)
        if (data.length) {
            console.log('Sending request to server...');
            await postJson('/tracking', data);
            handleUserActivity([]);
            changesSent = true;
        }
    } catch (error) {
        console.error(error)
    }
}



// If not focused on current document, remove interval. Otherwise initialize a new one.
document.addEventListener('visibilitychange', () => {
    removeTrackingInterval();
    if (!document.hidden) {
        setTrackingInterval();
    }
});
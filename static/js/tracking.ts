import { postJson } from "./comm";

const WAITING_TIME = 1000; // in milliseconds
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

function handleLocalStorage(item: string, value=Object()) {
    const retrievedItem = window.localStorage.getItem(item);
    if (!retrievedItem || JSON.stringify(value) !== retrievedItem) {
        window.localStorage.setItem(item, JSON.stringify(value));
    }

    if (retrievedItem) {
        if (item === CLICK_COUNTS) {
            value = JSON.parse(retrievedItem);
        } else if (item === LAST_ACTIVE) {
            value = parseInt(retrievedItem);
        }
    }
    return value;
}

const clickCounts = handleLocalStorage("clickCounts");
let lastActiveTime = handleLocalStorage("lastActiveTime", Date.now());


export function initializeTracking() {
    document.addEventListener('click', trackEvent);
    document.addEventListener('change', trackEvent);
}

async function trackEvent(event: Event) {
    const target = event.target as HTMLElement;
    // console.log(target, event.type)
    if (target.matches('button') || target.matches('a') || target.matches('input') || target.matches('select') || target.matches("div")) {
        let elementIdOrName = target.id;

        if (!elementIdOrName && target.hasAttribute("name")) {
            elementIdOrName = target.getAttribute("name") || "";
        }

        if (ELEMENT_TO_TRACK.includes(elementIdOrName)) {
            
            const page = window.location.pathname;
            if (clickCounts.hasOwnProperty(page)) {
                clickCounts[page].push({time: Date.now(), id: elementIdOrName});
            } else {
                clickCounts[page] = [{time: Date.now(), id: elementIdOrName}];
            }
            

            console.log(target, clickCounts)
            console.log(`Event: ${event.type}, Element ID or Name: ${elementIdOrName}, Click Count: ${clickCounts[page]}`);
            handleUserActivity();
            changesSent = false;
            // You can perform additional tracking or send the data to your server here
        } 
    }
}

// Set interval to check user activity every 5 minutes
let interval = setInterval(checkUserActivity, WAITING_TIME);
let intervalCanceled = false;
let changesSent = false;


// Function to send request to the server
async function sendRequestToServer() {
    console.log('Sending request to server...', clickCounts);
    // Your code to send a request to the server goes here
    try {
        await postJson('/tracking', clickCounts);
    } catch (error) {
        console.error(error)
        
    }
    changesSent = true;
}


// Function to handle user activity
function handleUserActivity() {
    lastActiveTime = Date.now();
    handleLocalStorage(LAST_ACTIVE, lastActiveTime);
    handleLocalStorage(CLICK_COUNTS, clickCounts);
    if (intervalCanceled) {
        console.log('set an interval again!')
        interval = setInterval(checkUserActivity, WAITING_TIME);
    }
}

// Function to check user activity and send request if inactive for 5 minutes
function checkUserActivity() {
    if (changesSent) {
        return;
    }
    const currentTime = Date.now();
    const inactiveDuration = currentTime - lastActiveTime;
    if (inactiveDuration >= WAITING_TIME) {
        sendRequestToServer();
        // clearInterval(interval)
        // intervalCanceled = true;
    }
}


// Event listener for visibility change
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) { // Page becomes visible
        console.log("visibility changed: VISIBLE")
        handleUserActivity();
    } else {
        console.log("visibility changed: NOT VISIBLE")
        sendRequestToServer();
        clearInterval(interval)
        intervalCanceled = true;
    }
});



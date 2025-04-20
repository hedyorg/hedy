
export function isLoggedIn() {
    if (document.body.dataset["loggedIn"]) {
        return parseInt(document.body.dataset["loggedIn"])
    }
    return false;
}

export function escapeHTML(str: string) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
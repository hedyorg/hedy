
export function isLoggedIn() {
    if (document.body.dataset["loggedIn"]) {
        return parseInt(document.body.dataset["loggedIn"])
    }
    return false;
}
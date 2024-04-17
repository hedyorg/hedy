import { autoSave } from "./autosave";

export interface InitializeMyProfilePage {
    readonly page: 'my-profile';
}

export function initializeMyProfilePage(_options: InitializeMyProfilePage) {
        // Autosave my profile page; only users' details.
        autoSave("profile");
}
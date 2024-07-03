import { navigate_home_button } from "../tools/navigation/nav";

it('Is able to click on all footer buttons', () => {
    navigate_home_button('subscribe_button', Cypress.env('subscribe_page'))
    navigate_home_button('learnmore_button', Cypress.env('learn_more_page'))
    navigate_home_button('footer_manual_button', Cypress.env('manual_page'))
    navigate_home_button('privacy_button', Cypress.env('privacy_page'))
})

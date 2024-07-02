import { navigate_home_button } from "../tools/navigation/nav";

it('Is able to click on all footer buttons', () => {
    navigate_home_button('subscribe_button', '/subscribe')
    navigate_home_button('learnmore_button', '/learn-more')
    navigate_home_button('footer_manual_button', '/for-teachers/manual')
    navigate_home_button('privacy_button', '/privacy')
})

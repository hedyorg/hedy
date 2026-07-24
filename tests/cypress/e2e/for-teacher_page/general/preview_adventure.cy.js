import {loginForTeacher} from '../../tools/login/login.js'
import { createAdventure } from '../../tools/adventures/adventure.js';

const adventures = ["adventure_preview_one", "adventure_preview_three"];

adventures.forEach((adventure) => {
  it('Is able to preview adventures', () => {
    const uniqueAdventureName = `${adventure}_${Date.now()}_${Math.floor(Math.random() * 10000)}`;
    loginForTeacher();
    createAdventure(uniqueAdventureName);
    cy.getDataCy('preview').click();
    cy.get('.tab_content.preview').should('be.visible');
  })
})

import {loginForTeacher} from '../tools/login/login.js'

const languages = [
  'ar',      'bg', 'bn',    'ca',    'cs',
  'cy',      'da', 'de',    'el',    'en',
  'eo',      'es', 'et',    'fa',    'fi',
  'fr',      'fy', 'he',    'hi',    'hu',
  'ia',      'id', 'it',    'ja',    'kmr',
  'ko',      'mi', 'nb_NO', 'nl',    'pa_PK',
  'pap',     'pl', 'pt_BR', 'pt_PT', 'ro',
  'ru',      'sq', 'sr',    'sv',    'sw',
  'te',      'th', 'tl',    'tn',   'tr', 
  'uk',      'ur',    'vi',    'zh_Hans',
  'zh_Hant'
];

describe('Check placeholders', () => {
  for (const lang of languages) {
    it(`passes ${lang}`, () => {
      loginForTeacher();
      cy.visit(`/hedy?language=${lang}`)
      const pages = Cypress.env();
      for (const key of Object.keys(pages)) {
        if (typeof pages[key] === "string") {
          const page = pages[key].includes("class") ? pages[key] + "5c39c2a936f24db1a4935c52fab77cd7" : pages[key];
          if (!page.includes("admin")) {
            cy.visit(page);
            cy.checkForPlaceholders();
          }
        }
      }
    });
  }
});

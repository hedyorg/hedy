import { initializeApp } from './app';
import { initializeFormSubmits } from './auth';
import { setClientMessageLanguage } from './client-messages';
import { logs } from './logs';
import { initializeQuiz } from './quiz';
import { APP_STATE } from './state';
import { initializeTabs } from './tabs';
import { initializeTutorial } from './tutorials/tutorial';

export interface InitializeOptions {
  readonly logs?: boolean;
}

/**
 * This function gets called by the HTML when the page is being initialized.
 */
export function initialize(options: InitializeOptions={}) {
  setClientMessageLanguage(APP_STATE.lang);

  initializeApp();
  initializeFormSubmits();
  initializeQuiz();
  initializeTabs();
  initializeTutorial();

  // initializing the teacher/customize class pages is done in a different
  // file. That is not great, we should be using a parameter to this function
  // probably, but for now that is what it is.

  if (options.logs) {
    logs.initialize();
  }
}


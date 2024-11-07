import { initializeAdminUserPage, InitializeAdminUsersPageOptions } from './admin';
import { initializeCustomAdventurePage, InitializeCustomizeAdventurePage } from './adventure';
import { initializeMyProfilePage, InitializeMyProfilePage } from './profile';
import { initializeApp, initializeCodePage, InitializeCodePageOptions, initializeViewProgramPage, InitializeViewProgramPageOptions } from './app';
import { initializeFormSubmits } from './auth';
import { setClientMessageLanguage } from './client-messages';
import { logs } from './logs';
import { initializeClassOverviewPage, InitializeClassOverviewPageOptions, initializeCustomizeClassPage, InitializeCustomizeClassPageOptions, initializeTeacherPage, InitializeTeacherPageOptions, initializeCreateAccountsPage, InitializeCreateAccountsPageOptions } from './teachers';
import { initializeTutorial } from './tutorials/tutorial';

export interface InitializeOptions {
  /**
   * Current language
   *
   * Written: by every page, on page load.
   * Used: on the code page, to do speech synthesis and to send to the server.
   */
  readonly lang: string;

  /**
   * Current level
   *
   * Written: by every page, on page load.
   *
   * Used: on the code page, to initialize the highlighter, to translate the program,
   * to determine timeouts, to load the quiz iframe, to show the variable inspector,
   * to show a debugger,  to load parsons exercises, to initialize a default save name.
   */
  readonly level: number;

  /**
   * Current keyword language
   *
   * Written: by every page, on page load.
   *
   * Used: set on the Ace editor, and then is used to do some magic that I don't
   * quite understand.
   */
  readonly keyword_language: string;

  readonly logs?: boolean;

  /**
   * The URL root where static content is hosted
   */
  readonly staticRoot?: string;

  /**
   * The domain name used in this page, as set up in the back-end
   */
  readonly domainName: string;

  readonly javascriptPageOptions?: InitializePageOptions;
}

type InitializePageOptions =
  | InitializeCodePageOptions
  | InitializeCustomizeClassPageOptions
  | InitializeTeacherPageOptions
  | InitializeCreateAccountsPageOptions
  | InitializeViewProgramPageOptions
  | InitializeClassOverviewPageOptions
  | InitializeAdminUsersPageOptions
  | InitializeCustomizeAdventurePage
  | InitializeMyProfilePage
  ;


/**
 * This function gets called by the HTML when the page is being initialized.
 */
export function initialize(options: InitializeOptions) {
  setClientMessageLanguage(options.lang);

  let level = options.level;

  if (!level && options.javascriptPageOptions?.page == "customize-adventure") {
    level = options.javascriptPageOptions.level
  }

  initializeApp({
    level: level,
    keywordLanguage: options.keyword_language,
    staticRoot: options.staticRoot,
    domainName: options.domainName
  });
  initializeFormSubmits();
  initializeTutorial();

  // The above initializations are often also page-specific
  switch (options.javascriptPageOptions?.page) {
    case 'code':
      initializeCodePage(options.javascriptPageOptions);
      break;

    case 'customize-class':
      initializeCustomizeClassPage(options.javascriptPageOptions);
      break;

    case 'for-teachers':
      initializeTeacherPage(options.javascriptPageOptions);
      break;

    case 'create-accounts':
      initializeCreateAccountsPage(options.javascriptPageOptions);
      break;

    case 'class-overview':
      initializeClassOverviewPage(options.javascriptPageOptions);
      break;

    case 'view-program':
      initializeViewProgramPage(options.javascriptPageOptions);
      break;

    case 'admin-users':
      initializeAdminUserPage(options.javascriptPageOptions);
      break;
    
    case 'customize-adventure':
      initializeCustomAdventurePage(options.javascriptPageOptions);
      break;

    case 'my-profile':
      initializeMyProfilePage(options.javascriptPageOptions);
      break;
    
    case 'tryit':
      initializeCodePage(options.javascriptPageOptions);
  }

  // FIXME: I think this might also be page-specific
  if (options.logs) {
    logs.initialize();
  }
}

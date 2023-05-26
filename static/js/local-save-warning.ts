/**
 * Show the warning if the "Run" button has been clicked this many times
 */
const SHOW_AFTER_RUN_CLICKS = 10;

/**
 * Show the warning if the program has hit this length
 */
const MIN_LINES_TO_WARN = 20;

/**
 * Show the warning after this many minutes on the same tab
 */
const SHOW_AFTER_MINUTES = 10;

/**
 * Holds state to do with the "make sure you log in" warning
 */
export class LocalSaveWarning {
  private runCounter = 0;
  private loggedIn = false;
  private programLength = 0;
  private timer?: NodeJS.Timeout;

  constructor() {
    this.reset();
  }

  /**
   * Mark the user as logged in. This disables everything.
   */
  public setLoggedIn() {
    this.loggedIn = true;
  }

  public clickRun() {
    this.runCounter += 1;
    if (this.runCounter >= SHOW_AFTER_RUN_CLICKS) {
      this.display(true);
    }
  }

  public setProgramLength(lines: number) {
    this.programLength = lines;
  }

  public switchTab() {
    this.reset();
    const startTime = Date.now();

    if (this.timer) {
      clearInterval(this.timer);
    }
    this.timer = setInterval(() => {
      if (this.programLength >= MIN_LINES_TO_WARN) {
        this.display(true);
      }
      if (Date.now() - startTime >= SHOW_AFTER_MINUTES * 60_000) {
        this.display(true);
      }
    }, 60_000);
  }

  private reset() {
    this.runCounter = 0;
    this.programLength = 0;
    this.display(false);
  }

  private display(show: boolean) {
    if (this.loggedIn) {
      // Never do it if user is logged in
      return;
    }
    $('#not-logged-in-warning').toggle(show);
  }
}

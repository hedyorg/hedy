import { EventEmitter } from './event-emitter';

export interface SwitchTabsEvent {
  readonly oldTab: string;
  readonly newTab: string;
}

export interface TabEvents {
  beforeSwitch: SwitchTabsEvent;
  afterSwitch: SwitchTabsEvent;
}

export interface TabOptions {
  readonly initialTab?: string;

  /**
   * Only activate tabs inside this scope
   */
  readonly where?: Element;
}

/**
 * Tabs
 *
 * Protocol:
 *
 * - Tabs consist of a TAB (the sticky-outy bit) and a TARGET
 *   (the pane that gets shown and hidden).
 *
 * - TABS should have: <... data-tab="SOME-ID">
 *
 * - TARGETS should have: <... data-tabtarget="SOME-ID">
 *
 * When a TAB is clicked, the TARGET with the matching id is shown
 * (and all other TARGETS in the same containing HTML element are hidden).
 *
 * The active TAB is indicated by the  '.tab-selected' class, the active
 * TARGET by the *absence* of the '.hidden' class.
 *
 * The active tab class can be changed by setting
 *
 * ```
 * data-activeclass="CLASSNAME"
 * ```
 */
export class Tabs {
  private _currentTab: string = '';

  private tabEvents = new EventEmitter<TabEvents>({
    beforeSwitch: true,
    afterSwitch: true,
  });

  constructor(options: TabOptions={}) {
    const root = $(options.where ?? document.body);

    root.find('*[data-tab]').on('click', (e) => {
      const tab = $(e.target);
      const tabName = tab.data('tab') as string;

      e.preventDefault();
      this.switchToTab(tabName);
    });

    // Determine initial tab
    // 1. Given by code
    // 2. In the URL
    // 3. Otherwise the first one we find
    let initialTab = options.initialTab;
    if (!initialTab && window.location.hash) {
      const hashFragment = window.location.hash.replace(/^#/, '');
      initialTab = hashFragment;
    }
    if (!initialTab) {
      initialTab = root.find('.tab:first').attr('data-tab');
    }

    if (initialTab) {
      this.switchToTab(initialTab);
    }
  }

  public switchToTab(tabName: string) {
    const doSwitch = () => {
      const oldTab = this._currentTab;
      this._currentTab = tabName;

      // Do a 'replaceState' to add a '#anchor' to the URL
      const hashFragment = tabName !== 'level' ? tabName : '';
      if (window.history) { window.history.replaceState(null, '', '#' + hashFragment); }

      // Find the tab that leads to this selection, and its siblings
      const tab = $('*[data-tab="' + tabName + '"]');
      const allTabs = tab.siblings('*[data-tab]');

      // Find the target associated with this selection, and its siblings
      const target = $('*[data-tabtarget="' + tabName + '"]');
      const allTargets = target.siblings('*[data-tabtarget]');

      // Fix classes
      allTabs.each((_, tab) => {
        const activeClass = $(tab).attr('data-activeclass') ?? 'tab-selected';
        $(tab).removeClass(activeClass);
      });
      const activeClass = tab.attr('data-activeclass') ?? 'tab-selected';
      tab.addClass(activeClass);

      allTargets.addClass('hidden');
      target.removeClass('hidden');

      this.tabEvents.emit('afterSwitch', { oldTab, newTab: tabName });
    }

    // We don't do a beforeSwitch event for the very first tab switch
    if (this._currentTab != '') {
      const event = this.tabEvents.emit('beforeSwitch', { oldTab: this._currentTab, newTab: tabName });
      event.then(doSwitch);
    } else {
      doSwitch();
    }
  }

  public get currentTab() {
    return this._currentTab;
  }

  public on(key: Parameters<typeof this.tabEvents.on>[0], handler: Parameters<typeof this.tabEvents.on>[1]) {
    const ret = this.tabEvents.on(key, handler);
    // Immediately invoke afterSwitch when it's being registered
    if (key === 'afterSwitch') {
      this.tabEvents.emit('afterSwitch', { oldTab: '', newTab: this._currentTab });
    }
    return ret;
  }
}


export function getPreviousAndNext() {
  const selected = document.querySelector('.tab-selected')
  if (!selected) return []
  const i = parseInt(selected.getAttribute('tabindex') || '0')
  const prev = document.querySelector(`.tab[tabindex='${i-1}']`)
  const next = document.querySelector(`.tab[tabindex='${i+1}']`)
  return [prev, next]
}
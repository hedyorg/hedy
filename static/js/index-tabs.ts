import { EventEmitter } from './event-emitter';

export interface SwitchAdventureEvent {
  readonly oldTab: string;
  readonly newTab: string;
}

export interface TabEvents {
  beforeSwitch: SwitchAdventureEvent;
  afterSwitch: SwitchAdventureEvent;
}

export interface TabOptions {
  readonly initialTab?: string;
  readonly level?: number;
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
 */
export class IndexTabs {
  private _currentTab: string = '';
  private _currentLevel?: number;

  private tabEvents = new EventEmitter<TabEvents>({
    beforeSwitch: true,
    afterSwitch: true,
  });

  constructor(options: TabOptions={}) {
    this._currentLevel = options.level;
    
    $('*[data-tab]').on('click', (e) => {
      const tab = $(e.target).closest('*[data-tab]');
      const tabName = tab.data('tab') as string;
      const level = tab.data('level');
      const parsedLevel = typeof level === 'number' ? level : Number(level);
      e.preventDefault();

      if (this._currentLevel != null && !Number.isNaN(parsedLevel) && this._currentLevel !== parsedLevel) {
        let endpoint = ''
        try {
          endpoint = window.location.pathname.split('/')[1];
        } catch (e) {
          endpoint = 'hedy';
        }
        location.href = `/${endpoint}/${level}#${tabName}`
      } else {
        this.switchToTab(tabName, parsedLevel);
      }
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
      initialTab = $('.tab:first').attr('data-tab');
    }

    if (initialTab && this._currentLevel) {
      this.switchToTab(initialTab, this._currentLevel);
    }
  }

  public switchToTab(tabName: string, level?: number) {
    const doSwitch = () => {
      // Once the javascript has loeaded, we can remove the loading spinner
      // and show the content
      document.getElementById('adventure_loading')?.classList.add('hidden')
      const oldTab = this._currentTab;
      this._currentTab = tabName;

      // Do a 'replaceState' to add a '#anchor' to the URL
      const hashFragment = tabName !== 'level' ? tabName : '';
      if (window.history) { window.history.replaceState(null, '', '#' + hashFragment); }

      const matchingTabs = $(`*[data-tab="${tabName}"]`);
      const tab = level != null && !Number.isNaN(level)
        ? matchingTabs.filter(`[data-level="${level}"]`).first()
        : matchingTabs.first();
      const allTabs = tab.siblings('*[data-tab]');

      // Find the target associated with this selection, and its siblings
      const target = $(`*[data-tabtarget="${tabName}"]`).first();
      const allTargets = target.siblings('*[data-tabtarget]');

      const activeClass = tab.attr('data-activeclass');
      if (activeClass) {
        allTabs.each((_, siblingTab) => {
          const siblingActiveClass = $(siblingTab).attr('data-activeclass') ?? 'tab-selected';
          $(siblingTab).removeClass(siblingActiveClass);
        });
        tab.addClass(activeClass);
      } else {
        allTabs.removeClass('adv-selected');
        allTabs.addClass('not-selected-adv')
        tab.removeClass('not-selected-adv')
        tab.addClass('adv-selected');
      }

      const tabTitle = document.getElementById('adventure_name');
      tabTitle && (tabTitle.textContent = tab.text().trim())
      const levelAdventureTitle = document.getElementById('level_adventure_title')
      const type = tab.data('type');
      levelAdventureTitle?.classList.remove('border-green-300', 'border-[#fdb2c5]', 'border-blue-300', 'border-blue-900')
      if (type == 'teacher') {
        levelAdventureTitle?.classList.add('border-green-300');
      } else if(type == 'command') {
        levelAdventureTitle?.classList.add('border-[#fdb2c5]')
      } else if (type == 'special') {
        levelAdventureTitle?.classList.add('border-blue-300')
      } else {
        levelAdventureTitle?.classList.add('border-blue-900')
      }

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

export function getNext() {
  const selected = document.querySelector('.adv-selected')
  if (!selected) return []
  const i = parseInt(selected.getAttribute('tabindex') || '0')
  const next = document.querySelector(`li[tabindex='${i+1}']`)
  return next
}

export function getCurrentAdv() {
  const selectedElement = document.querySelector('.adv-selected');
  if (selectedElement) {
    return selectedElement.textContent?.trim() ?? '';
  }
  return '';
}

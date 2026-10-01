/**
 * The index of the teacher manual.
 *
 * The index itself is rendered by the server, so it is there and it works before any of
 * this runs: every entry is an anchor, and every level folds open. What this adds is the
 * part a plain list of links cannot do -- following along while you read.
 *
 * - the entry for the heading you are at is highlighted, and scrolled into view inside
 *   the index when the index is longer than the window;
 * - the level you are reading folds open, and folds shut again once you have left it,
 *   unless you opened it yourself; a whole section of the manual folds away only when
 *   someone folds it away;
 * - picking an entry on a narrow screen folds the whole index away again.
 *
 * The way back to the top of the manual lives here too: it is the same question of where
 * in the page you are.
 */

export interface InitializeManualPageOptions {
  readonly page: 'teacher-manual';
}

/**
 * How far below the top of the window a heading counts as the one being read.
 *
 * Headings above this line are behind you; the first one below it is what you are
 * reading. It leaves room for the menu bar, and matches the `scroll-margin-top` the
 * stylesheet gives the headings, so that a heading jumped to from the index lands
 * exactly on the line that then marks it as current.
 */
const READING_LINE = 96;

const ACTIVE_CLASS = 'manual-index-link-active';

/** Marks a group this code folded open, so it may fold it shut again later. */
const AUTO_EXPANDED = 'manualIndexAutoExpanded';

export function initializeManualPage(_options: InitializeManualPageOptions) {
  initializeBackToTop();

  const indexes = Array.from(document.querySelectorAll<HTMLElement>('[data-manual-index]'));
  if (!indexes.length) {
    return;
  }

  // The index is on the page twice -- a column next to the text, and a folded list above
  // it on a narrow screen -- so one heading has more than one link pointing at it.
  const linksByHeading = new Map<HTMLElement, HTMLAnchorElement[]>();
  const headings: HTMLElement[] = [];

  for (const index of indexes) {
    for (const link of Array.from(index.querySelectorAll<HTMLAnchorElement>('a[href^="#"]'))) {
      const heading = headingFor(link);
      if (!heading) {
        continue;
      }
      const links = linksByHeading.get(heading);
      if (links) {
        links.push(link);
      } else {
        // The first copy of the index is in document order, so the headings are too.
        linksByHeading.set(heading, [link]);
        headings.push(heading);
      }
    }
  }
  if (!headings.length) {
    return;
  }

  for (const toggle of Array.from(document.querySelectorAll<HTMLElement>('[data-manual-index-toggle]'))) {
    toggle.addEventListener('click', () => {
      const group = toggle.closest<HTMLElement>('[data-manual-index-group]');
      if (group) {
        // Opening or closing a group by hand makes it yours: leave it alone from here on.
        setExpanded(group, !isExpanded(group));
        delete group.dataset[AUTO_EXPANDED];
      }
    });
  }

  // On a narrow screen the index covers the text it points into, so get it out of the way.
  for (const index of indexes) {
    index.addEventListener('click', (event) => {
      const link = (event.target as HTMLElement).closest('a[href^="#"]');
      const fold = link && index.closest<HTMLDetailsElement>('[data-manual-index-fold]');
      if (fold) {
        fold.open = false;
      }
    });
  }

  let active: HTMLElement | undefined;
  const onScreen = new Set<Element>();

  /**
   * Watch the band between the reading line and the bottom third of the window, rather
   * than listening for scroll events: it also notices a heading that moves across the
   * line without the window scrolling, as when a code block finishes loading and pushes
   * the rest of the page down.
   */
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        onScreen.add(entry.target);
      } else {
        onScreen.delete(entry.target);
      }
    }
    update();
  }, { rootMargin: `-${READING_LINE}px 0px -60% 0px` });

  for (const heading of headings) {
    observer.observe(heading);
  }
  update();

  function update() {
    // A long section can leave the band empty: its heading has scrolled past the top and
    // the next one is still below the fold. Then the section you are in is the last one
    // whose heading you went by.
    const current = headings.find((heading) => onScreen.has(heading))
      ?? lastHeadingPassed()
      ?? active
      ?? headings[0];

    if (current === active) {
      return;
    }
    if (active) {
      for (const link of linksByHeading.get(active) ?? []) {
        link.classList.remove(ACTIVE_CLASS);
        link.removeAttribute('aria-current');
      }
    }
    active = current;

    foldAroundActive();
    for (const link of linksByHeading.get(active) ?? []) {
      link.classList.add(ACTIVE_CLASS);
      link.setAttribute('aria-current', 'true');
      keepInView(link);
    }
  }

  function lastHeadingPassed() {
    let passed: HTMLElement | undefined;
    for (const heading of headings) {
      if (heading.getBoundingClientRect().top > READING_LINE) {
        break;
      }
      passed = heading;
    }
    return passed;
  }

  /**
   * Fold open the level the active heading belongs to, and fold the rest back up.
   *
   * Only the groups that asked for it, which is the levels. A section of the manual folds
   * away because a teacher folded it away, and reading something inside it is no reason to
   * put it back.
   */
  function foldAroundActive() {
    const current = active && linksByHeading.get(active)
      ?.map((link) => link.closest<HTMLElement>('[data-manual-index-autofold]'))
      .filter((group): group is HTMLElement => group !== null);
    const open = new Set(current ?? []);

    for (const group of Array.from(document.querySelectorAll<HTMLElement>('[data-manual-index-autofold]'))) {
      if (open.has(group)) {
        if (!isExpanded(group)) {
          setExpanded(group, true);
          group.dataset[AUTO_EXPANDED] = 'yes';
        }
      } else if (group.dataset[AUTO_EXPANDED]) {
        setExpanded(group, false);
        delete group.dataset[AUTO_EXPANDED];
      }
    }
  }
}

/**
 * Show the way back to the top once the top is out of sight, and take the reader there.
 *
 * What it watches is the page's own heading rather than a scroll position, so it is right
 * whatever the window is doing: it appears exactly when the thing it would scroll back to
 * has left the screen.
 */
function initializeBackToTop() {
  const button = document.querySelector<HTMLElement>('[data-manual-to-top]');
  const top = document.querySelector('h1');
  if (!button || !top) {
    return;
  }

  new IntersectionObserver(([entry]) => {
    button.classList.toggle('hidden', entry.isIntersecting);
  }).observe(top);

  button.addEventListener('click', () => {
    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' });
    // Someone who got here by keyboard should carry on from the top of the page, not from
    // a button that is about to disappear. Moving focus must not scroll: that would land
    // the page in one jump and undo the scrolling just asked for.
    document.querySelector<HTMLElement>('[data-manual-index] a')?.focus({ preventScroll: true });
  });
}

function headingFor(link: HTMLAnchorElement) {
  const id = decodeURIComponent(link.hash.slice(1));
  return id ? document.getElementById(id) : null;
}

function isExpanded(group: HTMLElement) {
  return group.querySelector('[data-manual-index-toggle]')?.getAttribute('aria-expanded') === 'true';
}

function setExpanded(group: HTMLElement, expanded: boolean) {
  group.querySelector('[data-manual-index-toggle]')?.setAttribute('aria-expanded', String(expanded));
  group.querySelector('[data-manual-index-children]')?.classList.toggle('hidden', !expanded);
}

/**
 * Scroll the index so that the entry just highlighted is on screen.
 *
 * Only the index scrolls: `scrollIntoView` would take the page with it and fight the
 * scrolling that brought us here in the first place.
 */
function keepInView(link: HTMLElement) {
  const panel = link.closest<HTMLElement>('[data-manual-index-scroll]');
  if (!panel || panel.scrollHeight <= panel.clientHeight) {
    return;
  }
  const margin = 16;
  const panelBox = panel.getBoundingClientRect();
  const linkBox = link.getBoundingClientRect();

  if (linkBox.top < panelBox.top + margin) {
    panel.scrollTop -= panelBox.top + margin - linkBox.top;
  } else if (linkBox.bottom > panelBox.bottom - margin) {
    panel.scrollTop += linkBox.bottom - panelBox.bottom + margin;
  }
}

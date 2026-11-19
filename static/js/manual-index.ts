/**
 * The index of the teacher manual. The server renders it; this follows along as you read:
 * highlighting the entry for the heading you are at, folding the level you are in open,
 * and showing the way back to the top.
 */

export interface InitializeManualPageOptions {
  readonly page: 'teacher-manual';
}

/** Where a heading counts as the one being read. Matches the headings' `scroll-mt-24`. */
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

  // The index is on the page twice, so a heading has more than one link pointing at it.
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
        // The first copy is in document order, so the headings are too.
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
        // Folding by hand makes the group yours: leave it alone from here on.
        setExpanded(group, !isExpanded(group));
        delete group.dataset[AUTO_EXPANDED];
      }
    });
  }

  // On a narrow screen the index covers the text it points into.
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

  // A band rather than scroll events, so it also notices a heading moved by a code block
  // finishing loading below it.
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
    // A long section leaves the band empty; then it is the last heading you went by.
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

  /** Folds the level being read open and the rest shut. Sections are left alone: folding
   *  one away is deliberate, and reading inside it is no reason to put it back. */
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

/** Shows the way back to the top once the page's own heading is out of sight. */
function initializeBackToTop() {
  const button = document.querySelector<HTMLElement>('[data-manual-to-top]');
  const top = document.querySelector('h1');
  if (!button || !top) {
    return;
  }

  // A scroll right after the page loads can arrive in the same batch as the first report,
  // so only the last entry says where the heading is now.
  new IntersectionObserver((entries) => {
    button.classList.toggle('hidden', entries[entries.length - 1].isIntersecting);
  }).observe(top);

  button.addEventListener('click', () => {
    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' });
    // Carry the keyboard to the top, without scrolling: that would undo the smooth scroll.
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

/** Scrolls the index, never the page: `scrollIntoView` would fight the scroll that got us
 *  here. */
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

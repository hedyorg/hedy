const HANDLERS = new Map<Element, () => void>();

/**
 * Watches elements with an IntersectionObserver rather than the window's scroll event,
 * so it also notices an element that comes into view without the window scrolling:
 * a tab being switched, a layout change above it, or a scroll inside a container.
 *
 * The margin starts the work a little before the element is on screen, so by the
 * time the user gets there it is already done.
 */
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    const handler = HANDLERS.get(entry.target);
    HANDLERS.delete(entry.target);
    observer.unobserve(entry.target);
    handler?.();
  }
}, { rootMargin: '300px 0px' });

export function onElementBecomesVisible(element: HTMLElement, handler: () => void) {
  HANDLERS.set(element, handler);
  observer.observe(element);
}

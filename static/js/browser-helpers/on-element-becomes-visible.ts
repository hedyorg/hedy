const SCROLL_HANDLERS = new Array<[HTMLElement, () => void]>();

function isInView(elem: HTMLElement) {
  var docViewTop = $(window).scrollTop()!;
  var docViewBottom = docViewTop + $(window).height()!;
  var elemTop = $(elem).offset()!.top;
  return ((elemTop <= docViewBottom) && (elemTop >= docViewTop));
}

export function checkNow() {
  for (let i = 0; i < SCROLL_HANDLERS.length; ) {
    const [element, handler] = SCROLL_HANDLERS[i];
    if (isInView(element)) {
      handler();
      SCROLL_HANDLERS.splice(i, 1);
    } else {
      i += 1;
    }
  }
}

$(window).on('scroll', checkNow);

export function onElementBecomesVisible(element: HTMLElement, handler: () => void) {
  if (isInView(element)) {
    handler();
  } else {
    SCROLL_HANDLERS.push([element, handler]);
  }
}

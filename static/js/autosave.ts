
const DEBOUNCE_TIMEOUT = 1000;

let timeoutId: ReturnType<typeof setTimeout> | null = null;
function debounce<F extends (...args: any[]) => any> (func: F, delay: number): (...args: Parameters<F>) => void {
  return (...args: Parameters<F>) => {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      func(...args);
    }, delay);
  };
}

interface GetRequest {
  trigger: string; // event type that we need to trigger.
  elementId: string; // element's id to trigger the event on.
}

export function autoSave(formId: string,
  customEvent: Event | any=null,
  triggerGetRequest: GetRequest | null = null,
  timeout: number=DEBOUNCE_TIMEOUT,
   ) {
    const formElement = document.getElementById(formId) as HTMLFormElement;
    if (!formElement) return
    // Debounce function to prevent excessive requests
    const handler = debounce((e: Event) => {
        if (!customEvent && (e.target as HTMLElement).dataset["autosaved"]) {
          // If the event is not from a customEvent with is the element autosaved, we pass.
          return
        }

          // Now we can simply trigger the submit event on the parent form element.
          formElement.requestSubmit()

          // Sometimes different components depend on each other, that is component A needs to be updated if component B
          // has changed. This is made mainly for the customize-class (comp. A) and partial-sortable-adventures (comp. B)
          //  we need A to be autosaved and since B is autosaved (via htmx), a get request on some of B's elemnts would
          // allow us to "update" B when A changes. We'll probably use this approach elsewhere too!
          // Moreover, a similar approach should be taken if we decide to allow syncronization between components in our platform.
          // That is, one component sends/triggers an event on another. 
          if (triggerGetRequest) {
            const element = document.getElementById(triggerGetRequest.elementId) as HTMLElement;
            const eventToTrigger = new Event(triggerGetRequest.trigger);
            element.dispatchEvent(eventToTrigger);
          }
    }, timeout);

  if (customEvent) {
    // A custom event could be fired by an element that's not within the form but still attributes to the 
    // submission. For instance, the CKEditor has its own elements and the listeners that we attach here 
    // don't include those elements.
    handler(customEvent);
  } else {
    // Add event listeners to all form elements
    formElement.addEventListener('input', handler);
    formElement.addEventListener('change', handler);
  }
}

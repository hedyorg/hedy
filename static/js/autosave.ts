
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

export function autoSave(formId: string,
  customEvent: Event | any=null,
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

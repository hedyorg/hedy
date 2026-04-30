
const DEBOUNCE_TIMEOUT = 1000;

const autosaveHandlers = new WeakMap<HTMLFormElement, (e: Event) => void>();

function debounce<F extends (...args: any[]) => any>(func: F, delay: number): (...args: Parameters<F>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
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
  customEvent: Event | any = null,
  timeout: number = DEBOUNCE_TIMEOUT,
) {
  console.log("Autosaving form with id:", formId);

  const formElement = document.getElementById(formId) as HTMLFormElement;
  if (!formElement) return

  let handler = autosaveHandlers.get(formElement);
  if (!handler) {
    // Debounce function to prevent excessive requests
    handler = debounce((e: Event) => {
      if ((e.target as HTMLElement).dataset["autosaved"]) {
      // If the event is not from a customEvent with is the element autosaved, we pass.
      return
      }
      // Now we can simply trigger the submit event on the parent form element.
      formElement.requestSubmit()
    }, timeout);

    formElement.addEventListener('input', handler);
    formElement.addEventListener('change', handler);
    autosaveHandlers.set(formElement, handler);
  }

  if (customEvent) {
    // A custom event could be fired by an element that's not within the form but still attributes to the 
    // submission. For instance, the CKEditor has its own elements and the listeners that we attach here 
    // don't include those elements.
    handler(customEvent);
  }
}

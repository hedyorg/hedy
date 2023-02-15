
import { MessageKey, TRANSLATIONS } from './message-translations';

export let ClientMessages: Record<MessageKey, string> = Object.assign({}, TRANSLATIONS['en']);

/**
 * Switch the values in the 'ErrorMessages' global
 */
export function setClientMessageLanguage(key: string) {
  // Mutate the object in-place, so that all imported references are still valid
  Object.assign(ClientMessages, TRANSLATIONS[key] ?? TRANSLATIONS['en']);
}

/**
 * Link adventure snippets to the place in Weblate where they are translated.
 * 
 * We generate the link based on the key for the snippet in the yaml.
 */

const WEBLATE_COMPONENT_URL = 'https://hosted.weblate.org/translate/hedy/adventures';

/**
 * The Weblate key of a field in the adventures YAML file.
 *
 * Weblate joins the nested YAML keys with '->'.
 */
export function weblateKey(adventure: string, level: string, field: string) {
  return ['adventures', adventure, 'levels', level, field].join('->');
}

export function weblateUrl(lang: string, adventure: string, level: string, field: string) {
  // The query needs to match exactly the string we are sending
  // otherwise we might match story_text and story_text_2
  const query = `key:r"^${weblateKey(adventure, level, field)}$"`;
  return `${WEBLATE_COMPONENT_URL}/${encodeURIComponent(lang)}/?q=${encodeURIComponent(query)}`;
}

// Set when a teacher ticks "don't show this message again" and continues to Weblate
const DISMISS_STORAGE_KEY = 'weblate-modal-dismissed';

function isWeblateModalDismissed() {
  try {
    return window.localStorage.getItem(DISMISS_STORAGE_KEY) === 'true';
  } catch {
    // Storage can be blocked, then we just keep showing the modal
    return false;
  }
}

function dismissWeblateModal() {
  try {
    window.localStorage.setItem(DISMISS_STORAGE_KEY, 'true');
  } catch {
    // Storage can be blocked, then the modal will just show again next time
  }
}

function hideWeblateModal() {
  $('#weblate_modal').addClass('hidden').removeClass('flex');
}

document.addEventListener('click', (e) => {
  const target = e.target as HTMLElement | null;

  if (target?.closest('.weblate-modal-close')) {
    // Only remember the choice when they actually go to Weblate, not when they cancel
    if (target.closest('#weblate_continue') && $('#weblate_modal_dismiss').is(':checked')) {
      dismissWeblateModal();
    }
    hideWeblateModal();
    return;
  }

  const link = target?.closest<HTMLElement>('.weblate-link');
  const weblateModal = document.getElementById('weblate_modal');
  if (!link || !weblateModal) {
    return;
  }

  const adventure = link.dataset['weblateAdventure'];
  const level = link.dataset['weblateLevel'];
  const field = link.dataset['weblateField'];
  const lang = weblateModal.dataset['weblateLang'];
  if (!adventure || !level || !field || !lang) {
    return;
  }

  const url = weblateUrl(lang, adventure, level, field);
  if (isWeblateModalDismissed()) {
    window.open(url, '_blank', 'noopener');
    return;
  }

  $('#weblate_continue').attr('href', url);
  $('#weblate_modal_dismiss').prop('checked', false);
  $(weblateModal).removeClass('hidden').addClass('flex');
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    hideWeblateModal();
  }
});

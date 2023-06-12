export function localSave(key: string, data: any) {
  window.localStorage?.setItem(key, JSON.stringify(data));
}

export function localDelete(key: string) {
  window.localStorage?.removeItem(key);
}

export function localLoad(key: string): any {
  const value = window.localStorage?.getItem(key);
  try {
    return value ? JSON.parse(value) : undefined;
  } catch (e) {
    // Invalid JSON or summin'
    return undefined;
  }
}

/**
 * Load an object, deleting it if found
 */
export function localLoadOnce(key: string): any {
  const ret = localLoad(key);
  if (ret !== undefined) {
    localDelete(key);
  }
  return ret;
}

export function isLoggedIn() {
    if (document.body.dataset["loggedIn"]) {
        return parseInt(document.body.dataset["loggedIn"])
    }
    return false;
}

// convert an objet in a map
export function convert(o:(object|undefined)) {
    if (typeof o === 'object') {
      let tmp:Map<string, object> = new Map(Object.entries(o));
  
      let ret:Map<string, (undefined|object)> = new Map();
  
      tmp.forEach((value, key) => {
        ret.set(key, convert(value));
      });
  
      return ret;
    } else {
      return o;
    }
  }
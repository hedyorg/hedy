/**
 * Post JSON, return the result on success, throw an exception on failure
 */
export function postJson(url: string, data?: any): Promise<any> {
  // Use the fetch API, if available
  if (window.fetch !== undefined) {
    return postJsonUsingFetch(url, data);
  }

  return new Promise((ok, ko) => {
    $.ajax({
      type: 'POST',
      url,
      ...(data ? { data: JSON.stringify(data) } : {}),
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
    }).done((response: any) => {
      ok(response);
    }).fail((err) => {
      ko(ajaxError(err));
    });
  });
}

/**
 * Use the fetch API
 *
 * Using this API, we can set `keepalive: true`, which will make the API call
 * complete even if the user navigates away from the page. This way, we can do
 * a "just-in-time" save of users programs while the page unloads.
 */
async function postJsonUsingFetch(url: string, data?: any): Promise<any> {
  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      keepalive: true,
      ...(data ? { body: JSON.stringify(data) } : {}),
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
      },
    });
  } catch (err: any) {
    throw Object.assign(new Error(err.message), {
      internetError: true,
    });
  }

  if (response.status !== 200) {
    // The error message is:
    // - response.error, if the response can be parsed as JSON
    // - A generic error message if the response is too big (indicating we're probably getting an HTML page back here)
    // - Otherwise the response text itself
    let errorMessage = await response.text();

    try {
      const parsed = JSON.parse(errorMessage);
      if (parsed.error) {
        errorMessage = parsed.error;
      }
    } catch {
      // Not JSON, so probably either plain text or HTML. Check for a sane length, otherwise put a placeholder text here.
      // (No need to translate, this should be very rare.)
      if (errorMessage.length > 500) {
        errorMessage = `the server responded with an error (${response.status} ${response.statusText})`;
      }
    }

    throw Object.assign(new Error(errorMessage), {
      responseText: errorMessage,
      status: response.status,
    });
  }

  return response.json();
}

export function postNoResponse(url: string, data?: any): Promise<void> {
  return new Promise<void>((ok, ko) => {
    $.ajax ({
      type: 'POST',
      url,
      contentType: 'application/json; charset=utf-8',
      ...(data ? { data: JSON.stringify(data) } : {}),
    }).done (() => {
      ok();
    }).fail((err) => {
      ko(ajaxError(err));
    });
  });
}

function ajaxError(err: any) {
  // Some places expect the error object to have the same attributes as
  // the XHR object, so copy them over.
  const error = new Error(err.responseText);
  return Object.assign(error, {
    responseText: err.responseText,
    status: err.status,
    // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState
    internetError: err.readyState < 4,
  });
}
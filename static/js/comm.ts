/**
 * Post JSON, return the result on success, throw an exception on failure
 */
export function postJson(url: string, data?: any): Promise<any> {
  // FIXME: This should be using the fetch() API with keepalive: true, so
  // that it can submit a final save when the user leaves the page.
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
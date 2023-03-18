/**
 * Post JSON, return the result on success, throw an exception on failure
 */
export function postJson(url: string, data: any): Promise<any> {
  // FIXME: This should be using the fetch() API with keepalive: true, so
  // that it can submit a final save when the user leaves the page.
  return new Promise((ok, ko) => {
    $.ajax({
      type: 'POST',
      url,
      data: JSON.stringify(data),
      contentType: 'application/json',
      dataType: 'json',
    }).done(function (response: any) {
      ok(response);
    }).fail(function (err) {
      ko(ajaxError(err));
    });
  });
}

export function postUrl(url: string): Promise<any> {
  return new Promise((ok, ko) => {
    $.ajax ({
      type: 'POST',
      url,
    }).done (function (response: any) {
      ok(response);
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
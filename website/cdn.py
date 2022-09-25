import utils


class Cdn:
    """Set up CDN configuration.

    Add a global to the template (called `static()`) to return references to
    static resources. All static resources should be referenced using this
    function.

    If CDN is not enabled:

        static('hello.jpg') -> '/hello.jpg' (fetch from the current server)

    If enabled (when a CDN prefix is given), add an additional
    route with a unique name containing the server commit to return
    static resources.

    If CDN is enabled:

        static('hello.jpg') -> 'https://1235.cdn.com/s-830s8a2fa/hello.jpg' (fetch from CDN)

    Because the commit number is in the URL, it can be extremely aggressively
    cached by the CDN.
    """

    def __init__(self, app, cdn_prefix, commit):
        self.cdn_prefix = cdn_prefix or ""
        self.commit = commit
        self.static_prefix = "/"
        self.app = app

        if self.cdn_prefix:
            # If we are using a CDN, also host static resources under a URL that includes
            # the version number (so the CDN can aggressively cache the static assets and we
            # still can invalidate them whenever necessary).
            #
            # The function {{static('/js/bla.js')}} can be used to retrieve the URL of static
            # assets, either from the CDN if configured or just the normal URL we would use
            # without a CDN.
            #
            # We still keep on hosting static assets in the "old" location as well for images in
            # emails and content we forgot to replace or are unable to replace (like in Markdowns).
            self.static_prefix = "/static-" + commit
            app.add_url_rule(
                self.static_prefix + "/<path:filename>", endpoint="cdn_static", view_func=self._send_static_file
            )

        app.add_template_global(self.static, name="static")

    def static(self, url):
        """Return cacheable links to static resources."""
        return utils.slash_join(self.cdn_prefix, self.static_prefix, url)

    def _send_static_file(self, filename):
        """
        Call app.send_static_file, add headers appropriate for the CDN.

        1. A CORS header. If we don't do this, JavaScript errors won't be
        reported properly ( the errors will be reported as "Script Error") due
        to browser security settings, since they seem to be originating from the
        CDN instead of from us.

        2. Set caching to indefinite.
        """
        response = self.app.send_static_file(filename)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.cache_control.max_age = 24 * 3600  # A day
        return response

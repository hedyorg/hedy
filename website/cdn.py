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
        self.cdn_prefix = cdn_prefix or ''
        self.commit = commit
        self.static_prefix = '/'

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
            # emails and content we forgot to replace or are unable to replace (like in MarkDowns).
            self.static_prefix = '/static-' + commit
            app.add_url_rule(self.static_prefix + '/<path:filename>',
                    endpoint="static",
                    view_func=app.send_static_file)

        app.add_template_global(self.static, name='static')

    def static(self, url):
        """Return cacheable links to static resources."""
        return utils.slash_join(self.cdn_prefix, self.static_prefix, url)



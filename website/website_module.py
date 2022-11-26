import collections

import flask


class WebsiteModule(flask.Blueprint):
    """A website module is a class with its own routes that can be mounted into an app.

    It's based on Flask Blueprints[1], but instead of defining an object and
    then registering routes on it, we put everything together in a class so that
    the routes can also share private variables that are injected from 'app.py', for example the database.
    The alternative (using a global g.db) would be untyped and
    then the IDE lacks information about the type causing less autocomplete support.

    Heavily inspired by [2].

    [1] https://flask.palletsprojects.com/en/2.2.x/blueprints/
    [2] https://gist.github.com/dplepage/2024199
    """

    def __init__(self, name: str, import_name: str, url_prefix=None):
        """Initialize the Blueprint.

        Call as follows:

            super().__init__('mymodule', __name__, url_prefix='/...')

        'url_prefix' can be left out.
        """
        super().__init__(name, import_name, url_prefix=url_prefix)

        for name in dir(self):
            fn = getattr(self, name)
            for rd in getattr(fn, "_routing_data", []):
                self.route(*rd.args, **rd.kwargs)(fn)


RoutingData = collections.namedtuple("RoutingData", ["args", "kwargs"])


def route(*args, **kwargs):
    def wrap(fn):
        route = getattr(fn, "_routing_data", [])
        route.append(RoutingData(args, kwargs))
        setattr(fn, "_routing_data", route)
        return fn

    return wrap

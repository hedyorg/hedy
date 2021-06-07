import flask
from website import querylog

@querylog.timed
def render_template(filename, **kwargs):
    """A copy of Flask's render_template that is timed."""
    return flask.render_template(filename, **kwargs)

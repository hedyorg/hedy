"""General helpers for Flask that ARE Hedy-specific."""

from flask import current_app
from website.database import Database


def g_db() -> Database:
    """An alias for g.db, but typed so that we can get autocomplete in the IDE."""
    return current_app.config['hedy_globals']['DATABASE']

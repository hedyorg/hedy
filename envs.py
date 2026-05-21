"""
Hedy runtime environment behavior.

There are various environments/modes in which Hedy can run.

- Local: a developer runs Hedy on their own machine, using Werkzeug development
         server. We show dev-friendly errors, use unoptimized Tailwind CSS and do not
         connect to real third party services.
- Offline: a special build of Hedy that teachers can download and run on their
           own computers. Uses Werkzeug, but real Tailwind, no 3rd party services,
           and a special offline data directory.
- CI: the automated tests that run on GitHub Actions. Much the same
      as the local environment.
- Docker (local): to validate the Docker build, but on a developer machine.
                  Dev-friendly errors, no 3rd party services, but real Tailwind.
- Heroku: the production environment, where we serve real customer traffic.

Feature          | Local | Docker (local) | CI    | Offline | Heroku
-----------------|-------|----------------|-------|---------|--------------
Server           | Werkz | Gunicorn       | Werkz | Werkz   | Gunicorn

Hot reload .py   | yes   | (n/a)          | no    | no      | (n/a)
Tailwind         | full  | min            | min   | min     | min

Access Log       | print | print          | print | -       | print
Errors           | dev   | dev            | dev   | hidden  | hidden
Allow X-Testing  | yes   | yes            | yes   | -       | -

Statics caching  | -     | yes            | yes   | yes     | yes
Query/Parse Logs | print | print          | print | -       | S3
Cloud            | -     | -              | -     | -       | yes

Secure Cookies   | -     | -              | -     | -       | yes
Require Secret   | -     | -              | -     | -       | yes
"""
import dataclasses
import os
import sys

@dataclasses.dataclass
class EnvironmentSettings:
    hot_reload_py: bool
    errors_pages: bool
    min_tailwind: bool
    statics_caching: bool
    cloud_services: bool
    access_log: bool
    event_logs: bool
    secure_cookies: bool
    require_secret: bool
    allow_x_testing: bool


def is_production():
    """Whether we are serving production traffic."""
    return os.getenv('IS_PRODUCTION', '') != ''


def is_heroku():
    """Whether we are running on Heroku.

    Only use this flag if you are making a decision that really has to do with
    Heroku-based hosting or not.

    If you are trying to make a decision whether something needs to be done
    "for real" or not, prefer using:

    - `is_production()` to see if we're serving customer traffic and trying to
      optimize for safety and speed.
    - `is_debug_mode()` to see if we're on a developer machine and we're trying
      to optimize for developer productivity.

    """
    return os.getenv('DYNO', '') != ''


def is_offline_mode():
    """Return whether or not we're in offline mode.

    Offline mode is a special build of Hedy that teachers can download and run
    on their own computers.
    """
    return getattr(sys, 'frozen', False) and offline_data_dir() is not None


def offline_data_dir():
    """Return the data directory in offline mode."""
    return getattr(sys, '_MEIPASS')


def is_ci():
    """Whether we're running in CI (GitHub Actions)."""
    return os.getenv('CI', '') != ''


def is_dev():
    return not is_production() and not is_offline_mode() and not os.getenv('NO_DEBUG_MODE')


def is_local_dev():
    return is_dev() and not is_ci()


CACHED_ENV_BEHAVIOR = None

def current_env():
    """Return the EnvironmentSettings for the current environment."""
    global CACHED_ENV_BEHAVIOR
    if CACHED_ENV_BEHAVIOR is None:
         CACHED_ENV_BEHAVIOR = _compute_env_behavior()
    return CACHED_ENV_BEHAVIOR

def _compute_env_behavior():
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")

    quick_iteration = is_local_dev() and not is_gunicorn

    return EnvironmentSettings(
        hot_reload_py=quick_iteration,
        # Unfortunately, the error page logic is intertwined with the hot reload
        # logic due to how Werkzeug works. 'errors_pages' doesn't do anything for now.
        errors_pages=is_dev(),
        min_tailwind=not quick_iteration,
        statics_caching=not quick_iteration,
        cloud_services=is_production(),
        access_log=is_dev(),
        event_logs=not is_offline_mode(),
        secure_cookies=is_production(),
        require_secret=is_production(),
        allow_x_testing=is_dev()
    )
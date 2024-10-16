from flask_babel import gettext
from website.flask_helpers import gettext_with_fallback


# Explicitly substitute the flask_babel function gettext with our own implementation that
# adds a fallback language. Note that we need to monkey-patch instead of use the gettext_with_fallback
# directly because the Babel extract function works if we use gettext with literal strings.
gettext = gettext_with_fallback  # noqa

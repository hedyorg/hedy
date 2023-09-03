import os


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(filename)s %(funcName)s %(lineno)d <%(levelname)s>: "
            "%(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG" if not os.getenv("NO_DEBUG_MODE") else "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG" if not os.getenv("NO_DEBUG_MODE") else "INFO",
            "propagate": False,
        },
    },
}

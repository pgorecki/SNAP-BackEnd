import logging.config
from django.utils.log import DEFAULT_LOGGING


def setup_logging(log_level: str, logs_filename: str):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    # exact format is not important, this is the minimum information
                    "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                },
                "colored": {
                    "()": "colorlog.ColoredFormatter",
                    "format": "%(log_color)s%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                },
                "colored_db": {
                    "()": "colorlog.ColoredFormatter",
                    "format": "%(log_color)s%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                    "log_colors": {
                        "DEBUG": "purple",
                        "INFO": "green",
                        "WARNING": "yellow",
                        "ERROR": "red",
                        "CRITICAL": "red,bold",
                    },
                },
                "json_formatter": {
                    "()": "core.ElkJsonFormatter.ElkJsonFormatter",
                },
                "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
            },
            "handlers": {
                # console logs to stderr
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "json_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json_formatter",
                },
                "colored_console": {
                    "class": "colorlog.StreamHandler",
                    "formatter": "colored",
                },
                "colored_console_db": {
                    "class": "colorlog.StreamHandler",
                    "formatter": "colored_db",
                },
                "file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": logs_filename,
                    "formatter": "json_formatter",
                },
                # Add Handler for Sentry for `warning` and above
                # 'sentry': {
                #     'level': 'WARNING',
                #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                # },
                "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
            },
            "loggers": {
                # default for all undefined Python modules
                "": {
                    "level": "WARNING",
                    "handlers": ["colored_console"],  # 'sentry'],
                },
                # Prevent noisy modules from logging to Sentry
                "noisy_module": {
                    "level": "ERROR",
                    "handlers": ["console"],
                    "propagate": False,
                },
                "django": {
                    "level": "INFO",
                    "handlers": ["json_console", "file_handler"],
                },
                # Our application code
                "django.app": {
                    "level": log_level.upper(),
                    "handlers": [
                        "json_console" or "colored_console",
                        "file_handler",
                    ],  # , 'sentry'],
                    # Avoid double logging because of root logger
                    "propagate": False,
                },
                # Default runserver request logging
                "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
                # Toggle SQL query logging
                "django.db.backends": {
                    "level": "INFO",
                    "handlers": ["json_console" or "colored_console_db"],
                    "propagate": False,
                },
            },
        }
    )

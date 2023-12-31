"""
Django settings for match4everyone project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from os import path

from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# or better:
# add paths here and import: from django.col import settings and use settings.XXX_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN_DIR = os.path.join(BASE_DIR, "run")
LOG_DIR = os.path.join(RUN_DIR, "log")

# Application definition

INSTALLED_APPS = [
    "djangocms_admin_style",  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "widget_tweaks",
    "crispy_forms",
    "django_tables2",
    "rest_framework",
    "apps.matching.apps.MatchingConfig",
    "apps.use_statistics.apps.UseStatisticsConfig",
    "webpack_loader",
    "django.contrib.sites",
    "cms",  # django CMS itself
    "treebeard",  # utilities for implementing a tree using materialised paths
    "menus",  # helper for model independent hierarchical website navigation
    "sekizai",  # for javascript and css management
    "filer",
    "easy_thumbnails",
    "mptt",
    "djangocms_text_ckeditor",
    "djangocms_link",
    "djangocms_file",
    "djangocms_picture",
    "djangocms_video",
    "djangocms_snippet",
    "djangocms_style",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'cms.middleware.utils.ApphookReloadMiddleware' TODO: Not working right now "ModuleNotFoundError: No module named 'cms.middleware.utils.ApphookReloadMiddlewaredjango'; 'cms.middleware.utils' is not a package"
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

ROOT_URLCONF = "match4everyone.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

LOGIN_REDIRECT_URL = "/matching/login_redirect"
LOGIN_URL = "/matching/login"

CRISPY_TEMPLATE_PACK = "bootstrap4"

WSGI_APPLICATION = "match4everyone.wsgi.application"

MAX_EMAILS_PER_HOSPITAL_PER_DAY = 200
NEWSLETTER_REQUIRED_APPROVERS = 2
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# django-cms settings
SITE_ID = 1
X_FRAME_OPTIONS = "SAMEORIGIN"
CMS_TEMPLATES = [
    ("home.html", "Home page template"),
]

# django-filler config
THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

TIME_ZONE = "UTC"

USE_I18N = True

AUTH_USER_MODEL = "matching.User"

USE_L10N = True

USE_TZ = False  # Until we have proper timezone support, this does not make sense and only generates warnings

# Translations
# Provide a lists of languages which your site supports.
LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
)
# Set the default language for your site.
LANGUAGE_CODE = "de"
# Tell Django where the project's translation files should be.
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

RUN_DIR = os.path.join(BASE_DIR, "run")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

MEDIA_ROOT = os.path.join(RUN_DIR, "media")
MEDIA_URL = "/media/"
# TODO: Serve media files properly (http://docs.django-cms.org/en/latest/how_to/install.html#media-and-static-file-handling)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(RUN_DIR, "static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.normpath(os.path.join(os.path.join(os.path.dirname(BASE_DIR), "frontend"), "dist")),
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LEAFLET_TILESERVER = os.getenv(
    "LEAFLET_TILESERVER"
)  # 'mapbox', 'open_street_map' or 'custom_tileserver'
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
TILE_SERVER_URL = os.getenv(
    "TILE_SERVER_URL"
)  # needs to include coordinates in the form "{x}","{y}","{z}"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

REST_FRAMEWORK = {"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination"}


# Configure Logging for all environments
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse",},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue",},
    },
    "formatters": {
        "json": {  # Made for Django Requests and General logging, will create parseable error logs
            "class": "match4everyone.logging.formatters.DjangoRequestJSONFormatter"
        },
        "text": {
            "class": "match4everyone.logging.formatters.DefaultExceptionFormatter",
            "format": "%(asctime)s: %(name)-12s %(levelname)-8s |%(message)s|",
        },
    },
    "handlers": {
        "mail_admin": {
            "class": "logging.NullHandler"  # Make sure to disable Djangos default e-Mail Logger
        },
        "null": {"class": "logging.NullHandler",},  # Disable Django Default Server Logger
        "console": {"class": "logging.StreamHandler", "formatter": "text",},
        "errorlogfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "level": "ERROR",
            "filename": path.join(LOG_DIR, "match4everyone.json.error.log"),
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
        },
        "auditlogfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "level": "INFO",
            "filename": path.join(LOG_DIR, "match4everyone.json.audit.log"),
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
        },
        "slack": {
            "level": "ERROR",
            "()": "match4everyone.logging.loggers.SlackMessageHandlerFactory",
            "webhook_url": os.environ.get("SLACK_LOG_WEBHOOK", ""),
        },
    },
    # Now put it all together
    "loggers": {
        "": {  # Root Logger Configuration, should catch all remaining Warnings and Errors, that were not specifically handled below
            "level": "WARNING",
            "handlers": ["errorlogfile", "console", "slack"],
        },
        "apps": {  # Logging Configuration for all Django apps, i.e. our software, matches any loggers under apps subdirectory using __name__
            "level": "INFO",
            "handlers": ["auditlogfile"],
            "propagate": False,
        },
        "django.request": {  # Main error logger and last line of defense for #500 Errors, will log all errors
            "level": "WARNING",
            "handlers": ["errorlogfile", "console", "slack"],
            "propagate": False,
        },
        "django.server": {  # Only for development server, all of these are mirrored on django.request anyway
            "level": "ERROR",
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": True,
        "BUNDLE_DIR_NAME": "/",  # must end with slash
        "STATS_FILE": os.path.normpath(
            os.path.join(
                os.path.join(os.path.join(os.path.dirname(BASE_DIR), "frontend"), "dist"),
                "webpack-stats.json",
            )
        ),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        # 'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}

# ========== determine wether this is a forked version of m4h ==========#

IS_TRAVIS = "TRAVIS" in os.environ and bool(os.environ["TRAVIS"])

IS_CI = "CI" in os.environ and bool(os.environ["CI"])

IS_FORK = False

if IS_TRAVIS and os.environ["TRAVIS_PULL_REQUEST_SLUG"] not in ["match4everyone/match4everything"]:
    IS_FORK = True

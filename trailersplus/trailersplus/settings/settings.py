# Environ set up
import logging
import os
import re

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

env_file = environ.Path(__file__) - 1 + ".env"
root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False), SECURE_SSL_REDIRECT=(bool, True))
environ.Env.read_env(env_file=env_file())

ROOT = root
BASE_DIR = root()

#############################
#    DEPLOY AND SECURITY    #
#############################

DEBUG = env("DEBUG")
# PAYMENT_PASS = env("PAYMENT_PASS")
# PAYMENT_USER = env("PAYMENT_USER")
# PAYMENT_MERCHANTNO = env("PAYMENT_MERCHANTNO")
# PAYMENT_ENDPOINT = env("PAYMENT_ENDPOINT")
# PAYMENT_POST = env("PAYMENT_POST")

if DEBUG:
    AUTHORIZE_LOGIN_ID = env.str("AUTHORIZE_DEBUG_LOGIN_ID")
    AUTHORIZE_TRANSACTION_KEY = env.str("AUTHORIZE_DEBUG_TRANSACTION_KEY")
    AUTHORIZE_CLIENT_KEY = env.str("AUTHORIZE_DEBUG_CLIENT_KEY")
    AUTHORIZE_JS_URL = env.str("AUTHORIZE_DEBUG_JS_URL")
else:
    AUTHORIZE_LOGIN_ID = env.str("AUTHORIZE_PROD_LOGIN_ID")
    AUTHORIZE_TRANSACTION_KEY = env.str("AUTHORIZE_PROD_TRANSACTION_KEY")
    AUTHORIZE_CLIENT_KEY = env.str("AUTHORIZE_PROD_CLIENT_KEY")
    AUTHORIZE_JS_URL = env.str("AUTHORIZE_PROD_JS_URL")

INTERNAL_IPS = ['127.0.0.1', '157.245.248.171', 'trailersplus.viewdemo.co']

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS


WSGI_APPLICATION = "trailersplus.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = "trailersplus.urls"

FIXTURE_DIRS = [str(BASE_DIR + 'fixtures')]

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE")
CSRF_TRUSTED_ORIGINS = [".trailersplus.com"]
SECURE_REFERRER_POLICY = env("SECURE_REFERRER_POLICY")
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS")
SESSION_COOKIE_HTTPONLY = False
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

#############################
#        COMPONENTS         #
#############################
INSTALLED_APPS = [
    "wagtail_modeltranslation",
    "wagtail_modeltranslation.makemigrations",
    "wagtail_modeltranslation.migrate",
    "streams",
    "home",
    "search",
    "menus",
    "store",
    "flatpage",
    "site_settings",
    "blog",
    "product",
    "checkout",
    "my_store",
    "wagtailcache",
    "storages",
    "wagtail.contrib.modeladmin",
    "wagtailmenus",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail_meta_preview",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.sitemaps",
    "wagtailuiplus",
    "wagtailmedia",
    "rest_framework",
    "corsheaders",
    "api.apps.ApiConfig",
    # "django_celery_results",
    # "django_celery_beat",
    "debug_toolbar",
]


MIDDLEWARE = [
    "wagtailcache.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "home.middleware.BrokenLinkMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "trailersplus.middleware.UserLocationMiddleware",
    "trailersplus.middleware.RequestSiteName",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "trailersplus.middleware.LocationTagMiddleware",
    "trailersplus.middleware.CacheRemovalMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "wagtailcache.cache.FetchFromCacheMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: env.bool("SHOW_TOOLBAR_CALLBACK", default=False),
}

ALLOW_AUTHORIZENET = env.bool('ALLOW_AUTHORIZENET', default=True)

CORS_ORIGIN_ALLOW_ALL = True

#############################
#           DATA            #
#############################

CACHES = {
    "default": env.cache(),
    "renditions": env.cache(),
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
DATABASES = {
    "default": env.db(),
    # "products": env.db("PRODUCTS_DB")
}

# DATABASE_ROUTERS = ['trailersplus.routers.DbRouter']

EMAIL_CONFIG = env.email_url("EMAIL_URL")

vars().update(EMAIL_CONFIG)

SITE_NAME = env.str("SITE_NAME")

#############################
# TRANSLATION AND LOCATION  #
#############################

LANGUAGE_CODE = "en"


LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "es")

LOCALE_PATH = str(root.path("locale"))

GEOIP_PATH = str(root + "trailersplus" + "locations")
GEOIP_KEY = env("GEOIP_KEY")

#############################
# WAGTAIL STREAM FORMS  #
#############################

WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
    ("streamforms/form_block.html", "Default Form Template"),  # default
    ("streamforms/fleet_sales_form.html", "Fleet Sales Template"),
    ("streamforms/custom_trailer_form.html", "Custom Trailer Template"),
)

TIME_ZONE = "America/Chicago"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################
# STATICFILES AND TEMPLATES #
#############################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(root + "trailersplus" + "templates"), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
                "trailersplus.context_processors.request_language",
                "trailersplus.context_processors.version_number",
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = ["django.template.context_processors.request"]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = str(root + "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    str(root + "trailersplus" + "static"),
]

MEDIA_ROOT = str(root + "media")
MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = env("DJANGO_STORAGE")
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"

# WAGTAILIMAGES_JPEG_QUALITY = 100
# WAGTAILIMAGES_WEBP_QUALITY = 100

#############################
#      BOTO3 SETTINGS       #
#############################
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
#############################
#     WAGTAIL SETTINGS      #
#############################
WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    "bmp": "jpeg",
    "webp": "webp",
}

WAGTAIL_SITE_NAME = "trailersplus"

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.HalloRichTextArea'
    }
}

BASE_URL = "http://example.com"

#############################
#   Django Rest Settings    #
#############################

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffSetPagination',
#     'PAGE_SIZE': 100,
# }

#############################
#      Celery Settings      #
#############################

CELERY_BROKER_URL = env.str("CELERY_CACHE")
CELERY_RESULT_BACKEND = env.str("RESULTS_CACHE")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# CELERY_TASK_ALWAYS_EAGER = True

TRUSTPILOT_API_KEY = env.str('TRUSTPILOT_API_KEY')
TRUSTPILOT_BUSINESS_UNIT = env.str('TRUSTPILOT_BUSINESS_UNIT')

#############################
#      OG-Facebook Settings      #
#############################

META_PREVIEW_FACEBOOK_TITLE_FIELDS = "og_title,seo_title,title"
META_PREVIEW_FACEBOOK_DESCRIPTION_FIELDS = "og_description,search_description"
META_PREVIEW_FACEBOOK_IMAGE_FIELDS = "og_image"

IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        '404_log': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/404.log'),
            'formatter': 'verbose'
        },
        'checkout': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/checkout.log'),
            'formatter': 'verbose'
        },
        'images': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/images.log'),
            'formatter': 'verbose'
        },
        'cache_invalidation': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/cache_invalidation.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'home.middleware': {
            'level': 'WARNING',
            'handlers': ['404_log'],
            'propagate': False,
        },
        'api.views': {
            'level': 'WARNING',
            'handlers': ['checkout'],
            'propagate': False,
        },
        'checkout.views': {
            'level': 'WARNING',
            'handlers': ['checkout'],
            'propagate': False,
        },
        'checkout.services': {
            'level': 'WARNING',
            'handlers': ['checkout'],
            'propagate': False,
        },
        'blog.signals': {
            'level': 'WARNING',
            'handlers': ['images'],
            'propagate': False,
        },
        'home.tasks': {
            'level': 'WARNING',
            'handlers': ['cache_invalidation'],
            'propagate': False,
        },
        'my_store.wagtail_hooks': {
            'level': 'WARNING',
            'handlers': ['cache_invalidation'],
            'propagate': False,
        },
        # Errors logged by the SDK itself
        'sentry_sdk': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# # Sentry Configuration
SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_LOG_LEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send no events from log messages
)
sentry_sdk.init(
    SENTRY_DSN,
    integrations=[sentry_logging, DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.01,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

REDIS_MESSAGE = env.str("REDIS_MESSAGE")

SERVER_X = env.str("SERVER_X", default=None)
CERT_X = env.str("CERT_X", default=None)

SERVER_Y = env.str("SERVER_Y", default=None)
CERT_Y = env.str("CERT_Y", default=None)
DEFAULT_INVOICE = env.str('DEFAULT_INVOICE', default=None)
ACH_ENABLED = env.str('ACH_ENABLED', default=False)

# UTA Credentials
UTA_USER = env.str("UTA_USER")
UTA_PASSWORD = env.str("UTA_PASSWORD")
UTA_MERCHANTNO = env.str("UTA_MERCHANTNO")

# Delete after development
LOCAL_ENV = env.str("LOCAL_ENV", default=False)
GDAL_LIBRARY_PATH = env("GDAL_LIBRARY_PATH", default=None)
GEOS_LIBRARY_PATH = env("GEOS_LIBRARY_PATH", default=None)

# STATIC FILES VERSION
VERSION_NUMBER = '?-v2.0.5'

# Formula for Interest Rate Calculation
INTEREST_RATE = env("INTEREST_RATE", default=12.49)
MONTHS_FINANCING = env("MONTHS_FINANCING", default=60)
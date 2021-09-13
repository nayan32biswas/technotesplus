import warnings

from .settings import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_SECURE = True

EMAIL_HOST_USER = "demo@example.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST = "console.gmail.com"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


SPECTACULAR_SETTINGS = {
    "SERVE_PUBLIC": False,
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.IsAuthenticated",
        "account.permissions.IsAdministrator",
    ],
}

try:
    __import__("debug_toolbar")
except ImportError as exc:
    warnings.warn(f"{exc} -- Install the missing dependencies ")
else:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = type(str("c"), (), {"__contains__": lambda *a: True})()

try:
    from .local import *
except ImportError:
    pass

import sys
from pprint import pprint
import builtins

from .base import *


# I'm probably setting a bad example for others here. Don't do this in prod.
builtins.pprint = pprint

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1e-bt$3shki&)(e#l2$fj0rqjp9k-bf0+&23j$o@mgi%$2$q6p"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:9000",
    "https://127.0.0.1:9000",
    "http://0.0.0.0:9000",
    "https://0.0.0.0:9000",
    "http://localhost:9000",
    "https://localhost:9000",
]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

CACHES["default"]["LOCATION"] = "redis://localhost:6379/1"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

if "test" in sys.argv:
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

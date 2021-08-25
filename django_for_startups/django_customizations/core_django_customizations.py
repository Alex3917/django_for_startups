# Standard Library imports
import unicodedata

# Core Django imports
from django.contrib.auth.backends import ModelBackend

# Third-party imports

# App imports
from app.models import EmailAddress


class CaseInsensitiveUserAuth(ModelBackend):
    def authenticate(self, *args, **kwargs):
        if "nfkc_username" in kwargs:
            username = kwargs.pop("nfkc_username", None)
        elif "username" in kwargs:
            username = kwargs.pop("username", None)

        if username and "@" in username:
            try:
                nfkc_email_address = unicodedata.normalize("NFKC", username).casefold()
                user_model = (
                    EmailAddress.objects.select_related("user_model")
                    .get(nfkc_email_address=nfkc_email_address)
                    .user_model
                )
                username = user_model.nfkc_username
            except EmailAddress.DoesNotExist:
                pass

        if username:
            nfkc_username = unicodedata.normalize("NFKC", username).casefold()
            return super().authenticate(
                *args, username=nfkc_username.casefold(), **kwargs
            )
        else:
            return None

    def get_user(self, *args, **kwargs):
        return super().get_user(*args, **kwargs)


class CustomSecurityHeaders(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith(("/admin", "/static")):
            response["content-type"] = "text/html"
            response["X-Robots-Tag"] = "noindex"
        else:
            response["Content-Security-Policy"] = "default-src 'none'"
            response["X-Content-Security-Policy"] = "default-src 'none'"

        return response

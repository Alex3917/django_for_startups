# Standard Library imports
from datetime import timedelta

# Core Django imports
from django.utils.dateformat import format
from django.utils import timezone

# Third-party imports
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from rest_framework_jwt.utils import jwt_create_payload

# App imports


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    """Expire token on password change and force user to re-authenticate."""

    def authenticate_credentials(self, payload):
        user_model = super().authenticate_credentials(payload)

        orig_iat = int(payload["orig_iat"])
        password_last_changed = int(format(user_model.password_last_changed, "U"))
        last_hour = timezone.now() - timedelta(hours=1)

        if orig_iat < password_last_changed:
            msg = "Users must re-authenticate after changing password."
            raise exceptions.AuthenticationFailed(msg)

        if user_model.last_activity < last_hour:
            user_model.last_activity = timezone.now()
            user_model.save()

        return user_model


def jwt_custom_payload_handler(user_model):
    payload = jwt_create_payload(user_model)
    payload.pop("user_id", None)
    payload.pop("email", None)
    return payload

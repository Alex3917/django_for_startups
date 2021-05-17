# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework_jwt.settings import api_settings

# App imports


def manually_generate_auth_token(user_model):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user_model)
    return jwt_encode_handler(payload)

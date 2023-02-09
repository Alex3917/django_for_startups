# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework_simplejwt.tokens import RefreshToken

# App imports


def manually_generate_auth_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
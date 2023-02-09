# Standard Library imports
from datetime import timedelta

# Core Django imports
from django.utils.dateformat import format
from django.utils import timezone

# Third-party imports
from rest_framework import permissions, authentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication

# App imports


class CustomJSONWebTokenAuthentication(JWTAuthentication):
    """ Expire token on password change and force user to re-authenticate. """

    def authenticate(self, *args, **kwargs):
        data = super().authenticate(*args, **kwargs)
        if not data:
            return data

        user_model = data[0]
        validated_token = data[1]

        iat = int(validated_token['iat'])
        password_last_changed = int(format(user_model.password_last_changed, 'U'))
        last_hour = timezone.now() - timedelta(hours=1)

        if iat < password_last_changed:
            msg = 'Users must re-authenticate after changing password.'
            raise exceptions.AuthenticationFailed(msg)

        if user_model.last_activity < last_hour:
            user_model.last_activity = timezone.now()
            user_model.save()

        return user_model, validated_token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims here
        return token

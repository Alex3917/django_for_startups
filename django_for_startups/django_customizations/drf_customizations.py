# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# App imports


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


class HighAnonThrottle(AnonRateThrottle):
    rate = '5000000/day'


class AccountCreation(permissions.BasePermission):
    """   A user should be able to create an account without being authenticated, but only the
          owner of an account should be able to access that account's data in a GET method.
    """

    def has_permission(self, request, view):
        if (request.method == "POST") or request.user.is_authenticated:
            return True
        return False

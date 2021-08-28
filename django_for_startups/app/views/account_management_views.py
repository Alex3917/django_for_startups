# Standard Library imports

# Core Django imports
from rest_framework.response import Response

# Third-party imports
from rest_framework.views import APIView
import marshmallow

# App imports
from utils import sanitization_utils
from utils.error_utils import (
    get_validation_error_response,
    get_business_requirement_error_response,
)
from app.services import account_management_service
from errors import custom_errors
from django_customizations.drf_customizations import AccountCreation


class User(APIView):
    permission_classes = (AccountCreation,)

    # Create account
    def post(self, request):
        unsafe_username = request.data.get("username", "")
        unsafe_email_address = request.data.get("email_address", "")
        unsafe_terms_of_service_accepted = request.data.get(
            "terms_of_service_accepted", None
        )
        unsafe_password = request.data.get("password", "")

        sanitized_username = sanitization_utils.strip_xss(unsafe_username)
        sanitized_email_address = sanitization_utils.strip_xss(unsafe_email_address)
        sanitized_terms_of_service_accepted = sanitization_utils.string_to_boolean(
            unsafe_terms_of_service_accepted
        )

        try:
            user_model, auth_token = account_management_service.create_account(
                sanitized_username,
                sanitized_email_address,
                unsafe_password,
                sanitized_terms_of_service_accepted,
            )
        except marshmallow.exceptions.ValidationError as e:
            return get_validation_error_response(
                validation_error=e, http_status_code=422
            )
        except custom_errors.UsernameAlreadyExistsError as e:
            return get_business_requirement_error_response(
                business_logic_error=e, http_status_code=409
            )
        except custom_errors.EmailAddressAlreadyExistsError as e:
            return get_business_requirement_error_response(
                business_logic_error=e, http_status_code=409
            )
        except custom_errors.TermsNotAcceptedError as e:
            return get_business_requirement_error_response(
                business_logic_error=e, http_status_code=429
            )

        resp = {"data": {"auth_token": auth_token}}
        return Response(data=resp, status=201)

    # Get account settings
    def get(self, request):
        user_profile_dict = account_management_service.get_user_profile_from_user_model(
            request.user
        )

        resp = {"data": {"user_profile": user_profile_dict}}
        return Response(data=resp, status=200)

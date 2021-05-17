# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework.response import Response

# App imports


def get_validation_error_response(validation_error, http_status_code, display_error=""):
    resp = {
        "errors": {
            "display_error": display_error,
            "field_errors": validation_error.normalized_messages(),
        }
    }

    return Response(data=resp, status=http_status_code)


def get_business_requirement_error_response(business_logic_error, http_status_code):
    resp = {
        "errors": {
            "display_error": business_logic_error.message,
            "internal_error_code": business_logic_error.internal_error_code,
        }
    }

    return Response(data=resp, status=http_status_code)

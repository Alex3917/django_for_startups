# Standard Library imports
import unicodedata

# Core Django imports
from django.db import transaction
from django.forms.models import model_to_dict

# Third-party imports
import marshmallow

# App imports
from app.validators import AccountCreationValidator
from app.models import User, EmailAddress
from utils import token_utils
from app.services import communication_service
from errors import custom_errors


def get_user_profile_from_user_model(user_model):
    user_model_dict = model_to_dict(user_model)

    user_model_dict["date_joined"] = user_model_dict["date_joined"].isoformat()

    allowlisted_keys = [
        "nfc_name",
        "nfkc_name",
        "nfc_username",
        "nfkc_username",
        "nfkc_primary_email_address",
        "date_joined",
    ]

    for key in list(user_model_dict.keys()):
        if not key in allowlisted_keys:
            user_model_dict.pop(key)

    return user_model_dict


def update_or_create_email_address(
    user_model, nfc_email_address, nfkc_email_address, is_primary, is_verified
):
    with transaction.atomic():
        # The `user_model` and `nfc_email_address` params are only set if a new object is created, so
        # we must still set them for updates
        email_address_model, _ = EmailAddress.objects.select_for_update().get_or_create(
            nfkc_email_address=nfkc_email_address,
            defaults={"user_model": user_model, "nfc_email_address": nfc_email_address},
        )

        """ Return an error if the email address already exists and is verified for a different
        user. This is to prevent other accounts from being left without a primary email. """
        if email_address_model.is_verified and (
            email_address_model.user_model.id != user_model.id
        ):
            raise custom_errors.EmailAddressAlreadyExistsError()

        email_address_model.user_model = user_model
        email_address_model.nfc_email_address = nfc_email_address
        email_address_model.is_verified = is_verified
        email_address_model.is_primary = is_primary
        email_address_model.save()

        # Set `is_verified` on the user_model if the email address being created or updated is
        # the user's primary email address.
        if user_model.nfkc_primary_email_address == nfkc_email_address:
            user_model.is_verified = is_verified
            user_model.save()

        # If a user successfully adds a linked email address, delete other users who have it as an unverified primary email.
        User.objects.filter(nfkc_primary_email_address=nfkc_email_address).exclude(
            id=user_model.id
        ).delete()


def create_account(
    sanitized_username,
    sanitized_email_address,
    unsafe_password,
    sanitized_terms_of_service_accepted,
):
    fields_to_validate_dict = {
        "username": sanitized_username,
        "email_address": sanitized_email_address,
        "password": unsafe_password,
        "terms_of_service": sanitized_terms_of_service_accepted,
    }

    AccountCreationValidator().load(fields_to_validate_dict)

    nfc_username = unicodedata.normalize("NFC", sanitized_username)
    nfkc_username = unicodedata.normalize("NFKC", sanitized_username).casefold()

    nfc_email_address = unicodedata.normalize("NFC", sanitized_email_address)
    nfkc_email_address = unicodedata.normalize(
        "NFKC", sanitized_email_address
    ).casefold()

    if User.objects.filter(nfkc_username=nfkc_username).exists():
        raise custom_errors.UsernameAlreadyExistsError()

    if EmailAddress.objects.filter(
        nfkc_email_address=nfkc_email_address, is_verified=True
    ).exists():
        raise custom_errors.EmailAddressAlreadyExistsError()

    if not sanitized_terms_of_service_accepted:
        raise custom_errors.TermsNotAcceptedError()

    with transaction.atomic():
        user_model = User.objects.create_user(
            nfkc_username=nfkc_username,
            nfc_username=nfc_username,
            nfkc_primary_email_address=nfkc_email_address,
            password=unsafe_password,
        )
        user_model.full_clean()
        user_model.save()

        update_or_create_email_address(
            user_model,
            nfc_email_address,
            nfkc_email_address,
            is_primary=True,
            is_verified=False,
        )

    communication_service.send_user_account_activation_email(user_model=user_model)

    # Return an auth token so that the front end doesn't need to do another round trip to log in the user.
    auth_token = token_utils.manually_generate_auth_token(user_model)

    return (
        user_model,
        auth_token,
    )

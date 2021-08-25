# Standard Library imports

# Core Django imports

# Third-party imports
from factory.django import DjangoModelFactory
from app.services import account_management_service
from app.models import *

# App imports


class UserFactory(DjangoModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        username = kwargs.pop("username")
        email_address = kwargs.pop("email_address")
        password = kwargs.pop("password", "1234567a")
        terms_of_service_accepted = kwargs.pop("terms_of_service_accepted", True)

        user_model, _ = account_management_service.create_account(
            username, email_address, password, terms_of_service_accepted
        )

        if kwargs:
            for kwarg, value in kwargs.items():
                setattr(user_model, kwarg, value)

            user_model.save()

        return user_model

    class Meta:
        model = User


class EmailAddressFactory(DjangoModelFactory):
    class Meta:
        model = EmailAddress

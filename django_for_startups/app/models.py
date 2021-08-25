# Standard Library imports

# Core Django imports
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.conf import settings
from django.utils import timezone
from django.db import transaction

# Third-party imports

# App imports


class UserManager(BaseUserManager):
    def create_user(
        self, nfkc_username, nfc_username, nfkc_primary_email_address, password=None
    ):
        """If you don't verify your primary email address, your account will get deleted
        if another user attempts to create an account with that email address."""
        existing_user_with_email = User.objects.select_for_update().filter(
            nfkc_primary_email_address=nfkc_primary_email_address
        )
        is_verified_email = EmailAddress.objects.filter(
            nfkc_email_address=nfkc_primary_email_address, is_verified=True
        ).exists()

        if existing_user_with_email and not is_verified_email:
            existing_user_with_email.delete()

        user_model = self.model(
            nfc_username=nfc_username,
            nfkc_username=nfkc_username,
            nfkc_primary_email_address=nfkc_primary_email_address,
        )
        user_model.set_password(password)

        return user_model

    def create_superuser(
        self, nfkc_username, nfkc_primary_email_address, password=None
    ):
        with transaction.atomic():
            nfc_username = nfkc_username
            user_model = self.create_user(
                nfkc_username, nfc_username, nfkc_primary_email_address, password
            )
            user_model.is_admin = True
            user_model.is_staff = True
            user_model.save()
        return user_model


class User(AbstractBaseUser, PermissionsMixin):
    """Stored casefolded, to prevent multiple users from having the same name username with different capitalization."""

    nfkc_username = models.CharField(max_length=15, unique=True)
    nfc_username = models.CharField(max_length=15)

    """ Also stored in the EmailAddress table; `AbstractBaseUser` requires custom users to implement an email field.
    Don't send emails to this address unless it's been verified. """
    nfkc_primary_email_address = models.EmailField(unique=True)
    # Don't allow a user to perform certain actions until they verify their primary email address
    is_verified = models.BooleanField(default=False)

    nfkc_name = models.CharField(max_length=20, db_index=True, blank=True)
    nfc_name = models.CharField(max_length=20, blank=True)

    last_activity = models.DateTimeField(default=timezone.now)
    password_last_changed = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    # These three fields are required by `AbstractBaseUser`
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "nfkc_username"
    EMAIL_FIELD = "nfkc_primary_email_address"
    REQUIRED_FIELDS = ["nfkc_primary_email_address"]

    def __str__(self):
        return self.nfc_username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, fwdeveryone):
        return True


class EmailAddress(models.Model):
    user_model = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nfc_email_address = models.EmailField()
    nfkc_email_address = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nfc_email_address)

    class Meta:
        unique_together = (("user_model", "is_primary"),)

from marshmallow import Schema, fields, validate

from django.conf import settings


class AccountCreationValidator(Schema):
    username = fields.Str(required=True, load_only=True, validate=[
            validate.Length(1, 15, error="Usernames must be less than or equal to 15 characters."),
            validate.Regexp("^[a-zA-Z][a-zA-Z0-9_]*$", error="Username must start with a letter, and "
                            "contain only letters, numbers, and underscores.",),
        ],
    )
    email_address = fields.Email(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True, validate=[validate.Length(settings.MIN_PASSWORD_LENGTH, None)],)
    terms_of_service = fields.Boolean(required=True, load_only=True)
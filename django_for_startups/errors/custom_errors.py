# Standard Library imports

# Core Django imports

# Third-party imports

# App imports


class Error(Exception):
    def __init__(self, value=""):
        if not hasattr(self, "value"):
            self.value = value

    def __str__(self):
        return repr(self.value)


###############
# User Errors #
###############
class UsernameAlreadyExistsError(Error):
    message = "An account with this username already exists!"
    internal_error_code = 40901


class EmailAddressAlreadyExistsError(Error):
    message = "There is already an account associated with this email address!"
    internal_error_code = 40902


class TermsNotAcceptedError(Error):
    message = "You must accept the terms of service in order to use example.com!"
    internal_error_code = 42901

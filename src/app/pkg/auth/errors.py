from enum import Enum

from app.pkg.errors import ErrorObj


class AuthErrorTypes(str, Enum):
    EMAIL_OCCUPIED = 'email_occupied'
    INVALID_CREDENTIALS = 'invalid_credentials'


class AuthError:
    @staticmethod
    def get_email_occupied_error() -> ErrorObj:
        return ErrorObj(
            type=AuthErrorTypes.EMAIL_OCCUPIED,
            message='This email is already occupied',
        )

    @staticmethod
    def get_invalid_credentials_error() -> ErrorObj:
        return ErrorObj(
            type=AuthErrorTypes.INVALID_CREDENTIALS,
            message='Invalid email or password',
        )

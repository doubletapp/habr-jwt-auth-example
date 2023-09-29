from enum import Enum

from app.pkg.errors import ErrorObj


class AccessErrorTypes(str, Enum):
    TOKEN_IS_NOT_SPECIFIED = 'token_is_not_specified'
    INCORRECT_AUTH_HEADER_FORM = 'incorrect_auth_header_form'
    INCORRECT_TOKEN_TYPE = 'incorrect_token_type'
    INVALID_TOKEN = 'invalid_token'
    TOKEN_REVOKED = 'token_revoked'
    TOKEN_ALREADY_REVOKED = 'token_already_revoked'
    TOKEN_OWNER_NOT_FOUND = 'token_owner_not_found'


class AccessError:
    @staticmethod
    def get_token_is_not_specified_error() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.TOKEN_IS_NOT_SPECIFIED,
            message='Access-token header is not set',
        )

    @staticmethod
    def get_incorrect_auth_header_form_error() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.INCORRECT_AUTH_HEADER_FORM,
            message='Access-token must have the form "Bearer <TOKEN>"',
        )

    @staticmethod
    def get_incorrect_token_type_error() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.INCORRECT_TOKEN_TYPE,
            message='The passed token does not match the required type',
        )

    @staticmethod
    def get_invalid_token_error() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.INVALID_TOKEN,
            message='The transferred token is invalid',
        )

    @staticmethod
    def get_token_revoked_error() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.TOKEN_REVOKED,
            message='This token has revoked',
        )

    @staticmethod
    def get_token_already_revoked_error() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.TOKEN_ALREADY_REVOKED,
            message='This token has already been revoked',
        )

    @staticmethod
    def get_token_owner_not_found() -> ErrorObj:
        return ErrorObj(
            type=AccessErrorTypes.TOKEN_OWNER_NOT_FOUND,
            message='The owner of this access token has not been found',
        )

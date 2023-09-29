from enum import Enum, unique


@unique
class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'

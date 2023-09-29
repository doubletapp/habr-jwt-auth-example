from pydantic import BaseModel


class UserCredentialsDTO(BaseModel):
    email: str
    password: str


class TokensDTO(BaseModel):
    access_token: str
    refresh_token: str

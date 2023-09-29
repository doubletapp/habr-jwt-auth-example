from pydantic import BaseModel, Field


class UserCredentialsIn(BaseModel):
    email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1)

    class Config:
        anystr_strip_whitespace = True


class UpdateTokensIn(BaseModel):
    refresh_token: str

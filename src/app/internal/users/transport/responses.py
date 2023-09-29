from uuid import UUID
from pydantic import BaseModel


class UserProfileOut(BaseModel):
    id: UUID
    email: str

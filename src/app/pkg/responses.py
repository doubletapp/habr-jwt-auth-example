from pydantic import BaseModel


class SuccessOut(BaseModel):
    success: bool = True


class ErrorOut(BaseModel):
    type: str
    message: str

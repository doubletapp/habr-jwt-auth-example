import uuid

from tortoise import Model, fields


class APIUser(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)

    email = fields.CharField(max_length=254, unique=True)
    password_hash = fields.CharField(max_length=64)

    def __str__(self) -> str:
        return self.email

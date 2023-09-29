from tortoise.models import Model
from tortoise import fields


class IssuedJWTToken(Model):
    jti = fields.CharField(max_length=36, pk=True)

    subject = fields.ForeignKeyField(
        model_name='models.APIUser',
        on_delete='CASCADE',
        related_name='tokens',
    )

    device_id = fields.CharField(max_length=36)
    revoked = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.subject}: {self.jti}'

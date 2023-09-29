from fastapi import APIRouter, Request, Security, Depends

from app.internal.users.service import MeService
from app.internal.users.transport.responses import UserProfileOut
from app.pkg.auth.middlewares.jwt.service import check_access_token


me_router = APIRouter(prefix='/me', tags=['me'], dependencies=[Security(check_access_token)])


def get_me_service() -> MeService:
    return MeService()


@me_router.get(path='', responses={200: {'model': UserProfileOut}})
async def get_me(request: Request, me_service: MeService = Depends(get_me_service)) -> None:
    return me_service.get_me(user=request.state.user)

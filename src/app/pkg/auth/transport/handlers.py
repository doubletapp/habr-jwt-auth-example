from fastapi import APIRouter, Depends, Request, Security
from fastapi.responses import JSONResponse

from app.pkg.auth.middlewares.jwt.service import check_access_token
from app.pkg.auth.service import AuthService
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.auth.transport.requests import UpdateTokensIn, UserCredentialsIn
from app.pkg.auth.transport.responses import TokensOut
from app.pkg.errors import get_bad_request_error_response
from app.pkg.responses import ErrorOut, SuccessOut
from config.settings import jwt_config


auth_router = APIRouter(prefix='/auth', tags=['auth'])


def get_auth_service() -> AuthService:
    return AuthService(jwt_auth=JWTAuth(config=jwt_config))


@auth_router.post(
    path='/register',
    responses={
        200: {'model': TokensOut},
        400: {'model': ErrorOut},
    },
)
async def register(
    request: Request,
    body: UserCredentialsIn,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut | JSONResponse:
    data, error = await auth_service.register(body=body)

    if error:
        return get_bad_request_error_response(error=error)

    return data


@auth_router.post(
    path='/login',
    responses={
        200: {'model': TokensOut},
        400: {'model': ErrorOut},
    },
)
async def login(
    request: Request,
    body: UserCredentialsIn,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut | JSONResponse:
    data, error = await auth_service.login(body=body)

    if error:
        return get_bad_request_error_response(error=error)

    return data


@auth_router.post(
    path='/logout',
    responses={200: {'model': SuccessOut}},
    dependencies=[Security(check_access_token)],
)
async def logout(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> SuccessOut:
    await auth_service.logout(user=request.state.user, device_id=request.state.device_id)
    return SuccessOut()


@auth_router.post(
    path='/update-tokens',
    responses={
        200: {'model': TokensOut},
        400: {'model': ErrorOut},
    },
    dependencies=[Security(check_access_token)],
)
async def update_tokens(
    request: Request,
    body: UpdateTokensIn,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokensOut | JSONResponse:
    data, error = await auth_service.update_tokens(user=request.state.user, **body.dict())

    if error:
        return get_bad_request_error_response(error=error)

    return data

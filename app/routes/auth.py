from fastapi import APIRouter

from app.schemas.user_schema import RegisterSchema
from app.schemas.auth_schema import (
    LoginSchema,
    RefreshTokenSchema,
    LogoutSchema
)
from app.schemas.email_schema import EmailSchema
from app.schemas.login_otp_schema import (
    LoginOtpVerifySchema
)
from app.services.auth_service import resend_login

from app.services.auth_service import (
    register_user,
    login_user,
    verify_login,
    refresh_access_token,
    logout_current_session,
    logout_all_sessions
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register(data: RegisterSchema):

    return await register_user(data)

@router.post("/login")
async def login(data: LoginSchema):

    return await login_user(data)
@router.post("/verify-login-otp")
async def verify_login_otp(
    data: LoginOtpVerifySchema
):

    return await verify_login(

        email=data.email,

        otp=data.otp,

        device=data.device

    )
@router.post("/resend-login-otp")
async def resend_login_otp_route(
    data: EmailSchema
):

    return await resend_login(

        data.email

    )

@router.post("/refresh-token")
async def refresh_token(data: RefreshTokenSchema):

    return await refresh_access_token(
        data.refresh_token
    )

@router.post("/logout")
async def logout(data: LogoutSchema):

    return await logout_current_session(
        data.refresh_token
    )
@router.post("/logout-all/{user_id}")
async def logout_all(user_id: str):

    return await logout_all_sessions(
        user_id
    )


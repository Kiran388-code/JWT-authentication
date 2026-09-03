from fastapi import APIRouter

from app.schemas.password_schema import (
    ForgotPasswordSchema,
    VerifyOTPSchema,
    ResetPasswordSchema,
    ResendOTPSchema
)

from app.services.auth_service import (
    forgot_password,
    verify_password_otp,
    resend_password_otp,
    reset_password
)

router = APIRouter(
    prefix="/password",
    tags=["Password"]
)
@router.post("/forgot-password")
async def forgot(data: ForgotPasswordSchema):

    return await forgot_password(
        data.email
    )
@router.post("/verify-otp")
async def verify(data: VerifyOTPSchema):

    return await verify_password_otp(
        data.phone,
        data.otp
    )
@router.post("/resend-otp")
async def resend(data: ResendOTPSchema):

    return await resend_password_otp(
        data.phone
    )
@router.post("/reset-password")
async def reset(data: ResetPasswordSchema):

    return await reset_password(
        data.phone,
        data.new_password
    )
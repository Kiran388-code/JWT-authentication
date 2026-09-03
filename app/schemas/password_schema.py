from pydantic import BaseModel, EmailStr, Field
class ForgotPasswordSchema(BaseModel):

    email: EmailStr
class VerifyOTPSchema(BaseModel):

    phone: str = Field(
        min_length=10,
        max_length=10
    )

    otp: str = Field(
        min_length=4,
        max_length=4
    )
class ResendOTPSchema(BaseModel):

    phone: str = Field(
        min_length=10,
        max_length=10
    )

class ResetPasswordSchema(BaseModel):

    phone: str = Field(
        min_length=10,
        max_length=10
    )

    new_password: str
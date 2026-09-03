from pydantic import BaseModel, EmailStr
from app.database.mongodb import users_collection

class LoginOtpVerifySchema(BaseModel):

    email: EmailStr

    otp: str

    device: str

# ===========================================
# GET VERIFIED LOGIN OTP
# ===========================================

async def get_verified_login_otp(

    email: str

):

    otp = await login_otp_collection().find_one(

        {

            "email": email,

            "is_verified": True

        }

    )

    return otp
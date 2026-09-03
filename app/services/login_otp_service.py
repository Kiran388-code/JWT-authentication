import random

from datetime import datetime, timedelta

from app.database.mongodb import login_otp_collection

from app.core.config import settings
def generate_login_otp():

    otp = ""

    for _ in range(settings.LOGIN_OTP_LENGTH):

        otp += str(random.randint(0, 9))

    return otp
async def create_login_otp(

    email: str

):

    await login_otp_collection().delete_many(

        {

            "email": email

        }

    )

    otp = generate_login_otp()

    otp_document = {

        "email": email,

        "otp": otp,

        "is_verified": False,

        "created_at": datetime.utcnow(),

        "expires_at": datetime.utcnow()

        + timedelta(

            minutes=settings.LOGIN_OTP_EXPIRE_MINUTES

        )

    }

    await login_otp_collection().insert_one(

        otp_document

    )

    return otp

async def verify_login_otp(

    email: str,

    otp: str

):

    otp_data = await login_otp_collection().find_one(

        {

            "email": email,

            "otp": otp,

            "is_verified": False

        }

    )

    if otp_data is None:

        return False

    if otp_data["expires_at"] < datetime.utcnow():

        await login_otp_collection().delete_one(

            {

                "_id": otp_data["_id"]

            }

        )

        return False

    await login_otp_collection().update_one(

        {

            "_id": otp_data["_id"]

        },

        {

            "$set": {

                "is_verified": True

            }

        }

    )

    return True

async def delete_login_otp(

    email: str

):

    await login_otp_collection().delete_many(

        {

            "email": email

        }

    )

async def resend_login_otp(email: str):

    await delete_login_otp(

        email

    )

    otp = await create_login_otp(

        email

    )

    return otp
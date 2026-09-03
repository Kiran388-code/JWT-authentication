import random

from datetime import datetime, timedelta

from app.database.mongodb import otp_collection
from app.core.config import settings

def generate_otp():

    otp = ""

    for _ in range(settings.OTP_LENGTH):

        otp += str(random.randint(0, 9))

    return otp



async def create_otp(
    phone: str
):

    await otp_collection().delete_many(

        {
            "phone": phone
        }

    )

    otp = generate_otp()

    otp_document = {

        "phone": phone,

        "otp": otp,

        "is_verified": False,

        "created_at": datetime.utcnow(),

        "expires_at": datetime.utcnow()

        + timedelta(

            minutes=settings.OTP_EXPIRE_MINUTES

        )

    }

    await otp_collection().insert_one(

        otp_document

    )

    return otp



async def verify_otp(

    phone: str,

    otp: str

):

    otp_data = await otp_collection().find_one(

        {

            "phone": phone,

            "otp": otp,

            "is_verified": False

        }

    )

    if otp_data is None:

        return False


    if otp_data["expires_at"] < datetime.utcnow():

        await otp_collection().delete_one(

            {

                "_id": otp_data["_id"]

            }

        )

        return False


    await otp_collection().update_one(

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



async def resend_otp(
    phone: str
):

    await otp_collection().delete_many(

        {

            "phone": phone

        }

    )

    return await create_otp(
        phone
    )



async def delete_otp(
    phone: str
):

    await otp_collection().delete_many(

        {

            "phone": phone

        }

    )



async def get_otp(
    phone: str
):

    otp = await otp_collection().find_one(

        {

            "phone": phone

        }

    )

    return otp



async def is_otp_verified(
    phone: str
):

    otp = await otp_collection().find_one(

        {

            "phone": phone,

            "is_verified": True

        }

    )

    if otp:

        return True

    return False



async def remove_expired_otps():

    result = await otp_collection().delete_many(

        {

            "expires_at": {

                "$lt": datetime.utcnow()

            }

        }

    )

    return result.deleted_count
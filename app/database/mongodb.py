from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class MongoDB:

    client: AsyncIOMotorClient = None

    database = None


mongodb = MongoDB()


async def connect_database():

    mongodb.client = AsyncIOMotorClient(

        settings.MONGO_URL

    )

    mongodb.database = mongodb.client[

        settings.DATABASE_NAME

    ]

    await mongodb.client.admin.command(

        "ping"

    )

    print("MongoDB Connected Successfully")


async def close_database():

    mongodb.client.close()

    print("MongoDB Connection Closed")


def get_database():

    return mongodb.database


def users_collection():

    return mongodb.database["users"]


def sessions_collection():

    return mongodb.database["sessions"]


def otp_collection():

    return mongodb.database["otp"]


def login_otp_collection():

    return mongodb.database["login_otp"]
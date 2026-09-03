from app.database.mongodb import sessions_collection
from app.models.session_model import create_session_model
from app.core.security import hash_password


async def create_user_session(
    user_id: str,
    refresh_token: str,
    device: str
):

    hashed_refresh_token = hash_password(
        refresh_token
    )

    session = create_session_model(

        user_id=user_id,

        refresh_token=hashed_refresh_token,
        device=device

    )

    await sessions_collection().insert_one(
        session
    )

    return session



async def count_active_sessions(
    user_id: str
):

    count = await sessions_collection().count_documents(

        {

            "user_id": user_id,

            "is_active": True

        }

    )

    return count



async def get_active_sessions(
    user_id: str
):

    sessions = []

    cursor = sessions_collection().find(

        {

            "user_id": user_id,

            "is_active": True

        }

    )

    async for session in cursor:

        session["_id"] = str(
            session["_id"]
        )

        sessions.append(
            session
        )

    return sessions

async def get_session_by_session_id(
    session_id: str
):

    session = await sessions_collection().find_one(

        {

            "session_id": session_id,

            "is_active": True

        }

    )

    return session



async def deactivate_session(
    session_id: str
):

    result = await sessions_collection().update_one(

        {

            "session_id": session_id

        },

        {

            "$set": {

                "is_active": False

            }

        }

    )

    return result.modified_count



async def deactivate_all_sessions(
    user_id: str
):

    result = await sessions_collection().update_many(

        {

            "user_id": user_id,

            "is_active": True

        },

        {

            "$set": {

                "is_active": False

            }

        }

    )

    return result.modified_count



async def update_refresh_token(

    session_id: str,

    hashed_refresh_token: str

):

    result = await sessions_collection().update_one(

        {

            "session_id": session_id

        },

        {

            "$set": {

                "refresh_token_hash": hashed_refresh_token

            }

        }

    )

    return result.modified_count
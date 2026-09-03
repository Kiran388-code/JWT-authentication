from datetime import datetime, timedelta
import uuid

from app.core.config import settings


def create_session_model(

    user_id: str,

    refresh_token: str,

    device: str

):

    session_id = str(

        uuid.uuid4()

    )

    return {

        "session_id": session_id,

        "user_id": user_id,

        "device": device,

        "refresh_token_hash": refresh_token,

        "is_active": True,

        "created_at": datetime.utcnow(),

        "expires_at": datetime.utcnow()

        + timedelta(

            days=settings.REFRESH_TOKEN_EXPIRE_DAYS

        )

    }
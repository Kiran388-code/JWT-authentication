from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException

from app.database.mongodb import users_collection
from app.core.jwt_handler import verify_access_token

router = APIRouter(

    prefix="/users",

    tags=["Users"]

)


@router.get("/profile")

async def profile(

    authorization: str = Header(...)

):

    if not authorization.startswith(

        "Bearer "

    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid Token"

        )

    token = authorization.split(

        " "

    )[1]

    payload = verify_access_token(

        token
    )
    if payload is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid Access Token"
        )

    user = await users_collection().find_one(

        {

            "_id": payload["user_id"]

        }

    )
    if user is None:

        raise HTTPException(

            status_code=404,

            detail="User Not Found"

        )

    return {

        "success": True,

        "user": {

            "id": str(user["_id"]),

            "name": user["name"],

            "email": user["email"],

            "phone": user["phone"]

        }

    }
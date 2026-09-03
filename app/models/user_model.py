from datetime import datetime


def create_user_model(
    name: str,
    email: str,
    phone: str,
    password: str
):

    return {

        "name": name,

        "email": email,

        "phone": phone,

        "password": password,

        "is_verified": False,

        "is_active": True,

        "created_at": datetime.utcnow(),

        "updated_at": datetime.utcnow()

    }
def user_response(user):

    return {

        "id": str(user["_id"]),

        "name": user["name"],

        "email": user["email"],

        "phone": user["phone"],

        "is_verified": user["is_verified"],

        "is_active": user["is_active"],

        "created_at": user["created_at"],

        "updated_at": user["updated_at"]

    }
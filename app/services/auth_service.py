from app.database.mongodb import users_collection

from app.core.security import (
    hash_password,
    verify_password
)

from app.core.password_checker import (
    check_password_strength
)

from app.core.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)

from app.models.user_model import (
    create_user_model
)

from app.services.login_otp_service import (
    create_login_otp,
    verify_login_otp,
    delete_login_otp,
    resend_login_otp
)

from app.services.otp_service import (
    create_otp,
    verify_otp,
    resend_otp,
    delete_otp,
    is_otp_verified
)

from app.services.session_service import (
    create_user_session,
    count_active_sessions,
    update_refresh_token,
    deactivate_session,
    deactivate_all_sessions,
    get_session_by_session_id
)

from app.email.email_service import (
    send_login_otp
)

from app.core.config import settings

async def register_user(data):

    existing_email = await users_collection().find_one(
        {
            "email": data.email
        }
    )
    if existing_email:

        return {

            "success": False,

            "message": "Email already registered."

        }
    existing_phone = await users_collection().find_one(

        {

            "phone": data.phone

        }

    )

    if existing_phone:

        return {

            "success": False,

            "message": "Phone number already registered."

        }


    password_status = check_password_strength(

        data.password

    )


    if password_status["success"] is False:

        return password_status


    hashed_password = hash_password(

        data.password

    )


    user = create_user_model(

        name=data.name,

        email=data.email,

        phone=data.phone,

        password=hashed_password

    )


    result = await users_collection().insert_one(

        user

    )


    return {

        "success": True,

        "message": "Registration Successful",

        "user_id": str(

            result.inserted_id

        )

    }

async def login_user(data):

    user = await users_collection().find_one(
        {
            "email": data.email
        }
    )

    if user is None:

        return {
            "success": False,
            "message": "Invalid Email"
        }

    if not verify_password(
        data.password,
        user["password"]
    ):

        return {
            "success": False,
            "message": "Invalid Password"
        }

    total_sessions = await count_active_sessions(
        str(user["_id"])
    )

    if total_sessions >= settings.MAX_ACTIVE_SESSIONS:

        return {
            "success": False,
            "message": "Maximum 3 active sessions allowed."
        }

    # ===========================================
    # Generate Login OTP
    # ===========================================

    otp = await create_login_otp(
    user["email"]
)

# Email sending disabled for development

    return {
    "success": True,
    "message": "OTP Generated Successfully",
    "email": user["email"],
    "otp": otp
}

async def verify_login(email: str, otp: str, device: str):

    status = await verify_login_otp(

        email,

        otp

    )

    if status is False:

        return {

            "success": False,

            "message": "Invalid OTP"

        }

    user = await users_collection().find_one(

        {

            "email": email

        }

    )

    session = await create_user_session(

        user_id=str(user["_id"]),

        refresh_token="TEMP",

        device=device

    )

    session_id = session["session_id"]

    access_token = create_access_token(

        user_id=str(user["_id"]),

        session_id=session_id

    )

    refresh_token = create_refresh_token(

        user_id=str(user["_id"]),

        session_id=session_id

    )

    hashed_refresh_token = hash_password(

        refresh_token

    )

    await update_refresh_token(

        session_id=session_id,

        hashed_refresh_token=hashed_refresh_token

    )

    await delete_login_otp(

        email

    )

    return {

        "success": True,

        "message": "Login Successful",

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "Bearer",

        "session_id": session_id

    }
# ==========================================================
# RESEND LOGIN OTP
# ==========================================================

async def resend_login(email: str):

    user = await users_collection().find_one(
        {
            "email": email
        }
    )

    if user is None:

        return {
            "success": False,
            "message": "Email Not Registered"
        }

    otp = await resend_login_otp(
        email
    )

    # Email sending disabled during development

    return {
        "success": True,
        "message": "OTP Resent Successfully",
        "email": user["email"],
        "otp": otp
    }

# ==========================================================
# REFRESH ACCESS TOKEN
# ==========================================================

async def refresh_access_token(refresh_token: str):

    payload = verify_refresh_token(refresh_token)

    if payload is None:

        return {

            "success": False,

            "message": "Invalid Refresh Token"

        }

    session = await get_session_by_session_id(

        payload["session_id"]

    )

    if session is None:

        return {

            "success": False,

            "message": "Session Not Found"

        }

    if not verify_password(

        refresh_token,

        session["refresh_token_hash"]

    ):

        return {

            "success": False,

            "message": "Invalid Refresh Token"

        }

    access_token = create_access_token(

        user_id=payload["user_id"],

        session_id=payload["session_id"]

    )

    return {

        "success": True,

        "access_token": access_token,

        "token_type": "Bearer"

    }
# ==========================================================
# LOGOUT CURRENT SESSION
# ==========================================================

async def logout_current_session(refresh_token: str):

    payload = verify_refresh_token(refresh_token)

    if payload is None:

        return {

            "success": False,

            "message": "Invalid Refresh Token"

        }

    await deactivate_session(

        payload["session_id"]

    )

    return {

        "success": True,

        "message": "Logout Successful"

    }
# ==========================================================
# LOGOUT ALL SESSIONS
# ==========================================================

async def logout_all_sessions(user_id: str):

    await deactivate_all_sessions(

        user_id

    )

    return {

        "success": True,

        "message": "All Sessions Logged Out"

    }
# ==========================================================
# FORGOT PASSWORD
# ==========================================================

async def forgot_password(email: str):

    user = await users_collection().find_one(

        {

            "email": email

        }

    )

    if user is None:

        return {

            "success": False,

            "message": "Email Not Registered"

        }

    otp = await create_otp(

        user["phone"]

    )

    return {

        "success": True,

        "message": "OTP Generated Successfully",

        "otp": otp

    }
# ==========================================================
# VERIFY PASSWORD OTP
# ==========================================================

async def verify_password_otp(

    phone: str,

    otp: str

):

    status = await verify_otp(

        phone,

        otp

    )

    if status is False:

        return {

            "success": False,

            "message": "Invalid OTP"

        }

    return {

        "success": True,

        "message": "OTP Verified"

    }
# ==========================================================
# RESEND PASSWORD OTP
# ==========================================================

async def resend_password_otp(
    phone: str
):

    otp = await resend_otp(
        phone
    )

    return {

        "success": True,

        "message": "OTP Resent Successfully",

        "otp": otp

    }
# ==========================================================
# RESET PASSWORD
# ==========================================================

async def reset_password(
    phone: str,
    new_password: str
):

    password_status = check_password_strength(
        new_password
    )

    if password_status["success"] is False:

        return password_status

    hashed_password = hash_password(
        new_password
    )

    result = await users_collection().update_one(

        {
            "phone": phone
        },

        {
            "$set": {
                "password": hashed_password
            }
        }

    )

    if result.modified_count == 0:

        return {

            "success": False,

            "message": "Password Reset Failed"

        }

    return {

        "success": True,

        "message": "Password Reset Successful"

    }


import re
def check_password_strength(
    password: str
):

    errors = []
    if len(password) < 8:

        errors.append(
            "Password must contain at least 8 characters."
        )
    if len(password) > 72:

        errors.append(
            "Password cannot exceed 72 characters."
        )

    if not re.search(
        r"[A-Z]",
        password
    ):

        errors.append(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(
        r"[a-z]",
        password
    ):

        errors.append(
            "Password must contain at least one lowercase letter."
        )
    if not re.search(
        r"\d",
        password
    ):
        errors.append(
            "Password must contain at least one number."
        )
    if not re.search(
        r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",
        password
    ):

        errors.append(
            "Password must contain at least one special character."
        )

    if errors:

        return {

            "success": False,

            "errors": errors

        }


    return {

        "success": True,

        "message": "Strong Password"

    }
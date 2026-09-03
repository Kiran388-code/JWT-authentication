from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import MessageType

from app.email.smtp import conf
from app.email.templates import login_otp_template


async def send_login_otp(

    email: str,

    name: str,

    otp: str

):

    html = login_otp_template(

        name,

        otp

    )

    message = MessageSchema(

        subject="Login Verification OTP",

        recipients=[email],

        body=html,

        subtype=MessageType.html

    )

    fm = FastMail(

        conf

    )

    await fm.send_message(

        message

    )
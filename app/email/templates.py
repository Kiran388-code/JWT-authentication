def login_otp_template(

    name: str,

    otp: str

):

    return f"""
    <html>

        <body>

            <h2>Login Verification</h2>

            <p>Hello <b>{name}</b>,</p>

            <p>Your Login OTP is:</p>

            <h1 style="color:#2563eb;">{otp}</h1>

            <p>This OTP is valid for 5 minutes.</p>

            <p>If you didn't request this login, ignore this email.</p>

        </body>

    </html>
    """
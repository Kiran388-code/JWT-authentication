from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):

    email: EmailStr

    password: str

    device: str

    


class RefreshTokenSchema(BaseModel):

    refresh_token: str


class LogoutSchema(BaseModel):

    refresh_token: str
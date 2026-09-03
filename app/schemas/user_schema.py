from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):

    name: str = Field(

        min_length=3,

        max_length=100

    )

    email: EmailStr

    phone: str = Field(

        min_length=10,

        max_length=10

    )

    password: str


class UserResponseSchema(BaseModel):

    id: str

    name: str

    email: EmailStr

    phone: str

    is_verified: bool

    is_active: bool
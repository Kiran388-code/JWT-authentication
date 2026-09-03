from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)


class TestEmailSchema(BaseModel):
    email: EmailStr


@router.post("/test")
async def test_email(data: TestEmailSchema):

    return {
        "success": True,
        "message": "Email service is disabled in development mode.",
        "email": data.email,
        "otp": "123456"
    }
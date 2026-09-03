from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes import email

from app.database.mongodb import (
    connect_database,
    close_database
)

from app.routes import auth
from app.routes import users
from app.routes import password


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect_database()

    yield

    await close_database()


app = FastAPI(

    title="JWT Authentication API",

    version="1.0.0",

    lifespan=lifespan

)

app.include_router(auth.router)
app.include_router(email.router)
app.include_router(users.router)

app.include_router(password.router)

@app.get("/")
async def home():

    return {

        "message": "JWT Authentication API Running"

    }

@app.get("/health")
async def health():

    return {

        "status": "OK"

    }
import datetime
from pydantic import BaseModel, EmailStr
import os


class UserDisplay(BaseModel):
    name: str
    email: str
    bio: str = None

    class Config:
        orm_mode = True


class UserDisplayWithId(UserDisplay):
    id: int


class SignUpRequestModel(UserDisplay):
    password: str
    time_created: datetime.datetime


class UserUpdateRequestModel(BaseModel):
    name: str
    password: str
    bio: str
    time_updated: datetime.datetime

    class Config:
        orm_mode = True


class User(UserDisplayWithId):
    time_updated: str


class SignInRequestModel(BaseModel):
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'email': 'this_is@your.email',
                'password': 'password_which_you_forgot'
            }
        }


class HTTPExceptionSchema(BaseModel):
    status_code: str
    detail: str

    class Config:
        schema_extra = {"detail": "HTTPException raised."}


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ["SECRET_KEY"]


class Token(BaseModel):
    access_token: str

import datetime

from pydantic import BaseModel


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


class UserUpdateRequestModel(UserDisplay):
    time_updated: datetime.datetime


class User(UserUpdateRequestModel):
    id: int


class SignInRequestModel(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class HTTPExceptionSchema(BaseModel):
    status_code: str
    detail: str

    class Config:
        schema_extra = {"detail": "HTTPException raised."}

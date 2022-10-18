import datetime

from pydantic import BaseModel
from typing import List


class UserDisplay(BaseModel):
    name: str
    email: str
    bio: str = None

    class Config:
        orm_mode = True


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

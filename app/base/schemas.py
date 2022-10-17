import datetime

from pydantic import BaseModel
from typing import List


class SignUpRequestModel(BaseModel):
    name: str
    email: str
    password: str
    bio: str
    time_created: datetime.datetime

    class Config:
        orm_mode = True


class UserUpdateRequestModel(SignUpRequestModel):
    time_updated: datetime.datetime

    # class Config:
    #     orm_mode = True


class User(UserUpdateRequestModel):
    id: int

    # class Config:
    #     orm_mode = True


class SignInRequestModel(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UsersListResponse(BaseModel):
    users: List[User] = []

    class Config:
        orm_mode = True

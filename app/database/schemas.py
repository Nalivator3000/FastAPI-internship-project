from typing import List

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str


class UserListResponse(BaseModel):
    users: List[User] = []

    class Config():
        orm_mode = True

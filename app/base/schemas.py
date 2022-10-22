import datetime
from fastapi_jwt_auth import AuthJWT
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
        schema_extra = {
            'example': {
                'email': 'this_is@your.email',
                'password': 'password_which_you_forgot'
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'eae62a7482658cb6d8af3bd1a70cc0689f1d1b81e28c78074c1c0c04fcd61100'


@AuthJWT.load_config
def get_config():
    return Settings()

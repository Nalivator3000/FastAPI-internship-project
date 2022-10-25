import datetime

from jose import jwt
from pydantic import EmailStr
from fastapi import Response, Depends, HTTPException, status
from base.base import database
from base.hash import Hash
from base.models import users
from services.user_services import UserCRUD
from auth.token_auth0 import VerifyToken, token_auth_scheme
from base.schemas import Token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() +
                             datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


class AuthCRUD:

    def __init__(self):
        self.database = database

    async def auth_test(response: Response, token: str = Depends(token_auth_scheme)) -> EmailStr:
        response.status_code = status.HTTP_202_ACCEPTED
        result = VerifyToken(token.credentials).verify()
        user_email = result.get("email")
        user = await database.fetch_one(users.select().where(users.c.email == user_email))
        if user is None:
            raise await UserCRUD.sign_up_user_by_email(user_email)
        if result.get('status'):
            status_code = response.status_code = status.HTTP_400_BAD_REQUEST
            raise status_code
        return user_email

    async def login(email: EmailStr, password: str, response: Response) -> Token:
        user = await database.fetch_one(users.select().where(users.c.email == email))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with email {email} not found')
        elif not Hash.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password is not correct')
        else:
            response.status_code = status.HTTP_202_ACCEPTED

            return Token(
                access_token=create_access_token({"sub": user.email}),
                token_type="Bearer"
            )

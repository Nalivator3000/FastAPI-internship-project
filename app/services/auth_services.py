import datetime
from fastapi.security import HTTPBearer
import jwt
from pydantic import EmailStr
from fastapi import Response, Depends, HTTPException, status
from base.base import database
from base.hash import Hash
from base.models import users
from auth.token_auth0 import VerifyToken, token_auth_scheme
from base.schemas import Token, UserDisplayWithId
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

from services.user_services import UserCRUD


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() +
                             datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def verify_password(password: str, hashed_password: str) -> bool:
    return Hash.verify(password, hashed_password)


def decode_token(token: str):
    return jwt.decode(token.credentials, SECRET_KEY, ALGORITHM)


async def get_current_user(token=Depends(HTTPBearer())) -> UserDisplayWithId:
    try:
        email = await AuthCRUD().auth0_test(response=Response, token=token)
        user = await database.fetch_one(users.select().where(users.c.email == email))
    except:
        try:
            decoded_token = decode_token(token=token)
            user = await database.fetch_one(users.select().where(users.c.email == decoded_token['sub']))
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')
    return user


class AuthCRUD:
    def __init__(self):
        self.database = database

    async def auth0_test(self, response: Response, token: str = Depends(token_auth_scheme)) -> EmailStr:
        try:
            response.status_code = status.HTTP_202_ACCEPTED
            result = VerifyToken(token.credentials).verify()
            user_email = result.get("email")
            user = await self.database.fetch_one(users.select().where(users.c.email == user_email))
            if user is None:
                return await UserCRUD().sign_up_user_by_email(user_email)
        except:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user_email

    async def get_token(self, email: EmailStr, password: str, response: Response) -> Token:
        user = await self.database.fetch_one(users.select().where(users.c.email == email))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        elif not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login or password is not correct')
        else:
            response.status_code = status.HTTP_202_ACCEPTED

        return Token(
            access_token=create_access_token({"sub": user.email}),
            token_type="Bearer"
        )

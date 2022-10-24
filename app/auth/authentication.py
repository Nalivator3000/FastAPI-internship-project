from fastapi import APIRouter, status, Depends, Response, HTTPException
from fastapi.security import HTTPBearer
from pydantic import EmailStr
from base.hash import Hash
from base.models import users
from .token import VerifyToken
from services.user_services import UserCRUD
from base.base import database

router = APIRouter(
    tags=['authentication']
)

token_auth_scheme = HTTPBearer()


@router.post('/auth-test', response_model=EmailStr)
async def auth_test(response: Response, token: str = Depends(token_auth_scheme)) -> EmailStr:
    result = VerifyToken(token.credentials).verify()
    user_email = result.get("email")

    user = await database.fetch_one(users.select().where(users.c.email == user_email))

    if user is None:
        raise await UserCRUD.sign_up_user_by_email(user_email)

    if result.get('status'):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return user_email


@router.post('/login', response_model=EmailStr)
async def login(email: EmailStr, password: str, response: Response, token: str = Depends(token_auth_scheme))\
        -> EmailStr:
    user = await database.fetch_one(users.select().where(users.c.email == email))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with email {email} not found')
    elif not Hash.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password is not correct')
    else:
        response.status_code = status.HTTP_202_ACCEPTED
        return VerifyToken(token.credentials).verify().get('email')

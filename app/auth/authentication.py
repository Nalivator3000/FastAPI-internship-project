from fastapi import APIRouter, status, Depends, Response
from fastapi.security import HTTPBearer
from base.models import users
from .token import VerifyToken
from services.user_services import UserCRUD

from base.base import database

router = APIRouter(
    tags=['authentication']
)

token_auth_scheme = HTTPBearer()


@router.post('/auth-test')
async def auth_test(response: Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()
    user_email = result.get("email")

    user = await database.fetch_one(users.select().where(users.c.email == user_email))
    print(f'User: {user}')

    if user is None:
        raise await UserCRUD.sign_up_user_by_email(user_email)

    if result.get('status'):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return user_email

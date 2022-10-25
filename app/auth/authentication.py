from fastapi import APIRouter
from .token import token_auth_scheme
from services.auth_services import *


router = APIRouter(
    tags=['authentication']
)


@router.post('/auth-test', response_model=EmailStr, status_code=status.HTTP_201_CREATED)
async def auth_test(response: Response, token: str = Depends(token_auth_scheme)) -> EmailStr:
    return await AuthCRUD.auth_test(response, token)


@router.post('/login', response_model=EmailStr, status_code=status.HTTP_201_CREATED)
async def login(email: EmailStr, password: str, response: Response, token: str = Depends(token_auth_scheme))\
        -> EmailStr:
        return await AuthCRUD.login(email, password, response, token)

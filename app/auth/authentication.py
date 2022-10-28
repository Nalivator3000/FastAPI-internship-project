from fastapi import APIRouter
from services.auth_services import *
from .token_auth0 import token_auth_scheme
from base.schemas import *

router = APIRouter(
    tags=['authentication']
)


@router.post('/auth-test', response_model=EmailStr, status_code=status.HTTP_201_CREATED)
async def auth_test(response: Response, token: str = Depends(token_auth_scheme)) -> EmailStr:
    return await AuthCRUD().auth0_test(response, token)


@router.post('/get-token', response_model=Token, status_code=status.HTTP_201_CREATED)
async def login(email: EmailStr, password: str, response: Response) -> Token:
    return await AuthCRUD().get_token(email, password, response)


@router.post('/get-current-user', response_model=UserDisplayWithId, status_code=status.HTTP_200_OK)
async def get_current_user(token: str) -> UserDisplayWithId:
    return await AuthCRUD().get_current_user_service(token)

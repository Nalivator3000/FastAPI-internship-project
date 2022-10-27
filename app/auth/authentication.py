from fastapi import APIRouter
from services.auth_services import *
from base.schemas import Token

router = APIRouter(
    tags=['authentication']
)


@router.post('/auth-test', response_model=EmailStr, status_code=status.HTTP_201_CREATED)
async def auth_test(response: Response, token: str = Depends(token_auth_scheme)) -> EmailStr:
    return await AuthCRUD().auth0_test(response, token)


@router.post('/login', response_model=Token, status_code=status.HTTP_201_CREATED)
async def login(email: EmailStr, password: str, response: Response) -> Token:
        return await AuthCRUD().login(email, password, response)


@router.post('/test-jwt', status_code=status.HTTP_202_ACCEPTED)
async def test_decode_jwt(response: Response, token: str) -> dict:
    return await AuthCRUD().test_decode_jwt(response, token)

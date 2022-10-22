from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from base.models import DbUser
from .token import VerifyToken

from base.base import database as db
from base.hash import Hash

router = APIRouter(
    tags=['authentication']
)

token_auth_scheme = HTTPBearer()


@router.post('/auth-test')
def auth_test(response: Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()

    if result.get('status'):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return result

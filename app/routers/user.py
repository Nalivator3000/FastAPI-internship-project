from fastapi import APIRouter, status, Response, Depends, HTTPException
from base.schemas import *
from typing import List
from auth.token_auth0 import token_auth_scheme
from base.schemas import SignUpRequestModel, UserDisplayWithId, HTTPExceptionSchema
from services import user_services

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/signup', response_model=SignUpRequestModel, status_code=status.HTTP_201_CREATED)
async def sign_up_user(u: SignUpRequestModel) -> SignUpRequestModel:
    return await user_services.UserCRUD().sign_up_user(u)


@router.get('/{id}', response_model=UserDisplayWithId)
async def get_user_by_id(id: int, response: Response, token: str = Depends(token_auth_scheme)) -> UserDisplayWithId:
    return await user_services.UserCRUD().get_user_by_id(id, response)


@router.get('/', response_model=List[UserDisplayWithId], status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(token_auth_scheme)) -> List[UserDisplayWithId]:
    return await user_services.UserCRUD().get_all_users()


@router.put('/{id}', response_model=UserUpdateRequestModel)
async def update_user(id: int, u: UserUpdateRequestModel, response: Response, token: str = Depends(token_auth_scheme))\
        -> UserUpdateRequestModel:
    return await user_services.UserCRUD().update_user(id, u, response)


@router.delete("/{id}", response_model=HTTPExceptionSchema)
async def delete_user(id: int, token: str = Depends(token_auth_scheme)) -> HTTPExceptionSchema:
    return await user_services.UserCRUD().delete_user(id)

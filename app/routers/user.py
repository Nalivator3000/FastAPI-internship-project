from fastapi import APIRouter, status, Response, Depends, HTTPException

from auth.authentication import get_current_user
from base.schemas import *
from typing import List
from base.schemas import SignUpRequestModel, UserDisplayWithId, HTTPExceptionSchema
from services import user_services

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/signup', response_model=SignUpRequestModel, status_code=status.HTTP_201_CREATED)
async def sign_up_user(u: SignUpRequestModel, current_user=Depends(get_current_user)) -> SignUpRequestModel:
    return await user_services.UserCRUD().sign_up_user(u=u)


@router.get('/{id}', response_model=UserDisplayWithId)
async def get_user_by_id(id: int, response: Response, current_user=Depends(get_current_user)) -> UserDisplayWithId:
    return await user_services.UserCRUD().get_user_by_id(id=id, response=response)


@router.get('/', response_model=List[UserDisplayWithId], status_code=status.HTTP_200_OK)
async def get_all_users(current_user=Depends(get_current_user)) -> List[UserDisplayWithId]:
    return await user_services.UserCRUD().get_all_users()


@router.put('/{id}', response_model=UserUpdateRequestModel)
async def update_user(id: int, u: UserUpdateRequestModel, response: Response, current_user=Depends(get_current_user))\
        -> UserUpdateRequestModel:
    return await user_services.UserCRUD().update_user(id=id, u=u, response=response)


@router.delete("/{id}", response_model=HTTPExceptionSchema)
async def delete_user(id: int, current_user=Depends(get_current_user)) -> HTTPExceptionSchema:
    return await user_services.UserCRUD().delete_user(id=id)

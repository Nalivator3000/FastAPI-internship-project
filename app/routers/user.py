from fastapi import APIRouter, status, Response, Depends
from base.schemas import *
from typing import List

from base.schemas import SignUpRequestModel, UserDisplayWithId
from services import user_services

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/signup', response_model=SignUpRequestModel, status_code=status.HTTP_201_CREATED)
async def sign_up_user(u: SignUpRequestModel) -> SignUpRequestModel:
    return await user_services.UserCRUD.sign_up_user(u)


@router.get('/{id}', response_model=UserDisplayWithId)
async def get_user_by_id(id: int, response: Response) -> UserDisplayWithId:
    return await user_services.UserCRUD.get_user_by_id(id, response)


@router.get('/', response_model=List[UserDisplayWithId], status_code=status.HTTP_200_OK)
async def get_all_users() -> List[UserDisplayWithId]:
    return await user_services.UserCRUD.get_all_users()


@router.put('/{id}', response_model=UserUpdateRequestModel)
async def update_user(id: int, u: UserUpdateRequestModel, response: Response) -> UserUpdateRequestModel:
    return await user_services.UserCRUD.update_user(id, u, response)


@router.delete("/{id}", response_model=HTTPExceptionSchema)
async def delete_user(id: int) -> HTTPExceptionSchema:
    return await user_services.UserCRUD.delete_user(id)

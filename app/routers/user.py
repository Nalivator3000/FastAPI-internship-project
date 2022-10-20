from fastapi import APIRouter, status, Response
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
    return await user_services.sign_up_user(u)


@router.get('/{id}')
async def get_user_by_id(id: int, response: Response) -> UserDisplayWithId:
    return await user_services.get_user_by_id(id, response)


@router.get('/', response_model=List[UserDisplayWithId], status_code=status.HTTP_200_OK)
async def get_all_users() -> List[UserDisplayWithId]:
    return await user_services.get_all_users()


@router.put('/{id}')
async def update_user(id: int, u: UserUpdateRequestModel, response: Response) -> UserUpdateRequestModel:
    return await user_services.update_user(id, u, response)


@router.delete("/{id}")
async def delete_user(id: int, response: Response):
    return await user_services.delete_user(id, response)

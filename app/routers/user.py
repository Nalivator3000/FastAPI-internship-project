from fastapi import APIRouter, status, Response
from base.schemas import *
from typing import List
import services

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/signup', response_model=SignUpRequestModel, status_code=status.HTTP_201_CREATED)
async def sign_up_user(u: SignUpRequestModel):
    return services.sign_up_user(u)


@router.get('/{id}', response_model=UserDisplayWithId, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, response: Response):
    return services.get_user_by_id(id, response)


@router.get('/', response_model=List[UserDisplayWithId], status_code=status.HTTP_200_OK)
async def get_all_users():
    return services.get_all_users()


@router.put('/{id}', response_model=UserUpdateRequestModel, status_code=status.HTTP_200_OK)
async def update_user(id: int, u: UserUpdateRequestModel, response: Response):
    return services.update_user(id, u, response)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, response: Response):
    return services.delete_user(id, response)

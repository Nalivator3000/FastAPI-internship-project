from fastapi import APIRouter, status, Response
from base.schemas import *
from base.models import users
from base.base import database
from typing import List
from base.hash import Hash

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/signup', response_model=SignUpRequestModel, status_code=status.HTTP_201_CREATED)
async def sign_up_user(u: SignUpRequestModel):
    query = users.insert().values(
        name=u.name,
        email=u.email,
        password=Hash.bcrypt(u.password),
        bio=u.bio
    )
    record_id = await database.execute(query)
    query = users.select().where(users.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@router.get('/{id}', response_model=UserDisplayWithId, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, response: Response):
    query = users.select().where(users.c.id == id)
    user = await database.fetch_one(query)
    if user is not None:
        response.status_code = status.HTTP_200_OK
        return {**user}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}


@router.get('/', response_model=List[UserDisplayWithId], status_code=status.HTTP_200_OK)
async def get_all_users():
    query = users.select()
    all_get = await database.fetch_all(query)
    return all_get


@router.put('/{id}', response_model=UserUpdateRequestModel, status_code=status.HTTP_200_OK)
async def update_user(id: int, u: UserUpdateRequestModel, response: Response):
    query = users.update().where(users.c.id == id).values(
        name=u.name,
        email=u.email,
        bio=u.bio,
    )
    user = await database.fetch_one(query)
    if user is not None:
        response.status_code = status.HTTP_200_OK
        record_id = await database.execute(query)
        query = users.select().where(users.c.id == record_id)
        row = await database.fetch_one(query)
        return {**row}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, response: Response):
    query = users.delete().where(users.c.id == id)
    user = await database.fetch_one(query)
    if user is not None:
        await database.execute(query)
        response.status_code = status.HTTP_200_OK
        return {'status': f'User {id} deleted successfully'}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}

from fastapi import APIRouter
from base.schemas import *
from base.models import users
from base.base import database
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/signup', response_model=SignUpRequestModel)
async def sign_up_user(u: SignUpRequestModel):
    query = users.insert().values(
        name=u.name,
        email=u.email,
        password=u.password,
        bio=u.bio
    )
    record_id = await database.execute(query)
    query = users.select().where(users.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@router.get('/{id}', response_model=UserDisplay)
async def get_user_by_id(id: int):
    query = users.select().where(users.c.id == id)
    user = await database.fetch_one(query)
    return {**user}


@router.get('/', response_model=List[UserDisplay])
async def get_all_users():
    query = users.select()
    all_get = await database.fetch_all(query)
    return all_get


@router.put('/{id}', response_model=UserUpdateRequestModel)
async def update_user(id: int, u: UserUpdateRequestModel):
    query = users.update().where(users.c.id == id).values(
        name=u.name,
        email=u.email,
        bio=u.bio
    )
    record_id = await database.execute(query)
    query = users.select().where(users.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@router.delete("/{id}") #response_model=User
async def delete(id: int):
    query = users.delete().where(users.c.id == id)
    await database.execute(query)
    return {'status': f'User {id} deleted successfully'}


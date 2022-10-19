from base.base import database
from base.hash import Hash
from base.models import users
from base.schemas import *
from fastapi import status, Response


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


async def get_user_by_id(id: int, response: Response):
    query = users.select().where(users.c.id == id)
    user = await database.fetch_one(query)
    if user is not None:
        response.status_code = status.HTTP_200_OK
        return {**user}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}


async def get_all_users():
    query = users.select()
    all_get = await database.fetch_all(query)
    return all_get


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


async def delete_user(id: int, response: Response):
    query = users.delete().where(users.c.id == id)
    user = await database.fetch_one(query)
    if user is not None:
        await database.execute(query)
        response.status_code = status.HTTP_200_OK
        return {'status': f'User {id} deleted successfully'}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}
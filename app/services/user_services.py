from base.base import database
from base.hash import Hash
from base.models import users
from base.schemas import *
from fastapi import status, Response
from typing import List


async def sign_up_user(u) -> SignUpRequestModel:
    query = users.insert().values(
        name=u.name,
        email=u.email,
        password=Hash.bcrypt(u.password),
        bio=u.bio
    )

    record_id = await database.execute(query)
    query = users.select().where(users.c.id == record_id)
    row = await database.fetch_one(query)

    return SignUpRequestModel(**row)


async def get_user_by_id(id: int, response: Response) -> UserDisplayWithId or dict[str, str]:
    user = await database.fetch_one(users.select().where(users.c.id == id))
    if user is not None:
        response.status_code = status.HTTP_200_OK
        user = await database.fetch_one(users.select().where(users.c.id == id))
        return UserDisplayWithId(**user)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}


async def get_all_users() -> List[UserDisplayWithId]:
    user_list = await database.fetch_all(query=users.select())
    return user_list


async def update_user(id: int, u: UserUpdateRequestModel, response: Response)\
        -> UserUpdateRequestModel or dict[str:str]:
    user = await database.fetch_one(users.select().where(users.c.id == id))
    if user is not None:
        query = users.update().where(users.c.id == id).values(
            name=u.name,
            email=u.email,
            bio=u.bio,
        )
        response.status_code = status.HTTP_200_OK
        record_id = await database.execute(query)
        query = users.select().where(users.c.id == id)
        row = await database.fetch_one(query)
        print('-\n-\n-\n-\n-\n', {**row}, '-\n-\n-\n-\n-\n')
        return UserUpdateRequestModel(**row)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}


async def delete_user(id: int, response: Response):
    user = await database.fetch_one(users.select().where(users.c.id == id))
    if user is not None:
        response.status_code = status.HTTP_200_OK
        query = users.delete().where(users.c.id == id)
        await database.execute(query)
        return {'status': f'User {id} deleted successfully'}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'User with id {id} not found'}
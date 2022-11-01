from base.base import database
from base.hash import Hash
from base.models import users
from base.schemas import *
from fastapi import status, Response, HTTPException
from typing import List

from services.validation import *


class UserCRUD:
    def __init__(self):
        self.database = database

    async def sign_up_user(self, u: SignUpRequestModel) -> SignUpRequestModel:
        query = users.insert().values(
            name=u.name,
            email=u.email,
            password=Hash.bcrypt(u.password),
            bio=u.bio
        )

        record_id = await self.database.execute(query)
        query = users.select().where(users.c.id == record_id)
        row = await self.database.fetch_one(query)

        return SignUpRequestModel(**row)

    async def get_user_by_id(self, id: int, response: Response) -> UserDisplayWithId:
        user = await self.database.fetch_one(users.select().where(users.c.id == id))
        if user is not None:
            response.status_code = status.HTTP_200_OK
            user = await self.database.fetch_one(users.select().where(users.c.id == id))
            return UserDisplayWithId(**user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')

    async def get_all_users(self) -> List[UserDisplayWithId]:
        user_list = await self.database.fetch_all(query=users.select())
        return user_list

    async def update_user(self, id: int, u: UserUpdateRequestModel, response: Response, current_user: UserDisplayWithId)\
            -> UserUpdateRequestModel:
        user = await self.database.fetch_one(users.select().where(users.c.id == id))
        user_update_validation(current_user=current_user, user_id=user.id)
        if user is not None:
            response.status_code = status.HTTP_200_OK
            query = users.update().where(users.c.id == id).values(
                name=u.name,
                password=Hash.bcrypt(u.password),
                bio=u.bio
            )

            await self.database.execute(query)
            query = users.select().where(users.c.id == user.id)
            row = await self.database.fetch_one(query)

            return UserUpdateRequestModel(**row)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')

    async def delete_user(self, id: int, current_user: UserDisplayWithId) -> HTTPExceptionSchema:
        user = await self.database.fetch_one(users.select().where(users.c.id == id))
        user_update_validation(current_user=current_user, user_id=user.id)
        if user is not None:
            query = users.delete().where(users.c.id == id)
            await self.database.execute(query)
            raise HTTPException(status_code=status.HTTP_200_OK, detail=f'User {id} deleted successfully')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')

    async def sign_up_user_by_email(self, user_email: EmailStr) -> SignUpRequestModel:
        query = users.insert().values(
            name=str(user_email).split('@')[0],
            email=user_email,
            password=Hash.bcrypt(user_email),
            bio='Default bio'
        )

        record_id = await self.database.execute(query)
        query = users.select().where(users.c.id == record_id)
        row = await self.database.fetch_one(query)

        return SignUpRequestModel(**row)

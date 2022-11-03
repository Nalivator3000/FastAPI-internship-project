from typing import List

from fastapi import Response, status, HTTPException

from base.base import database
from base.models import companies, users, companies_users, companies_administrators
from base.schemas import Company, UserDisplayWithId, CompanyUpdate, HTTPExceptionSchema, UserDisplay
from services.validation import user_update_validation, company_update_validation, company_delete_validation


class CompanyCRUD:
    def __init__(self):
        self.database = database

    async def create_company(self, company: Company, response: Response, current_user: UserDisplayWithId):
        response.status_code = status.HTTP_201_CREATED
        query = companies.insert().values(
            name=company.name,
            description=company.description,
            is_hide=company.is_hide,
            owner=current_user.email
        )

        record_id = await self.database.execute(query)
        query = companies.select().where(companies.c.id == record_id)
        row = await self.database.fetch_one(query)

        return Company(**row)

    async def get_company_by_id(self, id: int, response: Response) -> Company:
        company = await self.database.fetch_one(companies.select().where(companies.c.id == id))
        if company is not None:
            if company.is_hide:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Company with id {id} is hided')
            else:
                response.status_code = status.HTTP_200_OK
                company = await self.database.fetch_one(companies.select().where(companies.c.id == id))
                return Company(**company)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company with id {id} not found')

    async def get_all_companies(self) -> List[UserDisplayWithId]:
        companies_list = await self.database.fetch_all(companies.select().where(companies.c.is_hide == False))
        return companies_list

    async def update_company(
            self, id: int, company: CompanyUpdate, response: Response, current_user: UserDisplay) \
            -> CompanyUpdate:
        comp = await self.database.fetch_one(companies.select().where(companies.c.id == id))
        company_update_validation(current_user=current_user, user_email=comp.owner)
        if comp is not None:
            response.status_code = status.HTTP_200_OK
            query = companies.update().where(companies.c.id == id).values(
                name=company.name,
                description=company.description,
                is_hide=company.is_hide,
                id=id
            )

            await self.database.execute(query)
            query = companies.select().where(companies.c.id == company.id)
            row = await self.database.fetch_one(query)

            return CompanyUpdate(**row)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company with id {id} not found')

    async def delete_company(self, id: int, current_user: UserDisplayWithId) -> HTTPExceptionSchema:
        company = await self.database.fetch_one(companies.select().where(companies.c.id == id))
        company_delete_validation(current_user=current_user, user_email=company.owner)
        if company is not None:
            query = companies.delete().where(companies.c.id == id)
            await self.database.execute(query)
            raise HTTPException(status_code=status.HTTP_200_OK, detail=f'User {id} deleted successfully')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')

    async def add_user_to_company(self, company_id: int, user_id: int, current_user: UserDisplayWithId):
        user = await self.database.fetch_one(users.select().where(users.c.id == user_id))
        company = await self.database.fetch_one(companies.select().where(companies.c.id == company_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
        elif company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company with id {company_id} not found')
        else:
            await self.database.execute(companies_users.insert().values(
                user_id=user.id,
                company_id=company.id,
                is_active_owner=True,
                is_active_user=False
            ))
            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail=f'User {user_id} successfully added to company {company_id}')

    async def delete_user_from_company(self, cid: int, uid: int, current_user: UserDisplayWithId):
        user_company = await self.database.fetch_one(companies_users.select().where(companies_users.c.user_id == uid).
                                                     where(companies_users.c.company_id == cid))
        if user_company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No matches found')
        else:
            await self.database.execute(companies_users.delete().where(companies_users.c.user_id == uid).
                                        where(companies_users.c.company_id == cid))
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'User {uid} deleted from company {cid} successfully')

    async def accept_invitation(self, answer: bool, cid: int, current_user: UserDisplayWithId):
        if answer:
            query = companies.update().where(current_user.id == companies_users.c.user_id). \
                where(cid == companies_users.c.company_id).values(
                is_active_user=True
            )
            await self.database.execute(query)
        else:
            await self.database.execute(companies_users.delete().where(companies_users.c.user_id == current_user.id).
                                        where(companies_users.c.company_id == cid))
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail='You declined an invitation to the company')

    async def join_group(self, cid: int, current_user: UserDisplayWithId):
        company = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        if company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company with id {cid} not found')
        else:
            await self.database.execute(companies_users.insert().values(
                user_id=current_user.id,
                company_id=company.id,
                is_active_owner=False,
                is_active_user=True
            ))
            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail=f'You have applied to join company {company.name}')

    async def approve_application(self, answer: bool, uid: int, cid: int, current_user: UserDisplayWithId):
        company = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        company_update_validation(current_user=current_user, user_email=company.owner)
        if answer:
            query = companies.update().where(uid == companies_users.c.user_id). \
                where(cid == companies_users.c.company_id).values(
                is_active_owner=True
            )
            await self.database.execute(query)
        else:
            await self.database.execute(companies_users.delete().where(companies_users.c.user_id == current_user.id).
                                        where(companies_users.c.company_id == cid))
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail='You declined request to join the company')

    async def add_admin_to_company(self, cid: int, uid: int, current_user: UserDisplayWithId):
        user = await self.database.fetch_one(users.select().where(users.c.id == uid))
        company = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        company_user = await self.database.fetch_one(companies_users.select().where(companies_users.c.user_id == uid).
                                                     where(companies_users.c.company_id == cid))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {uid} not found')
        elif company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company with id {cid} not found')
        elif company_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'User {uid} is not a member of company {cid}')
        else:
            await self.database.execute(companies_administrators.insert().values(
                user_id=user.id,
                company_id=company.id
            ))
            raise HTTPException(status_code=status.HTTP_201_CREATED,
                                detail=f'User {uid} successfully added to company {cid} as administrator')

    async def delete_admin_from_company(self, uid: int, cid: int, current_user: UserDisplayWithId):
        admin_company = await self.database.fetch_one(companies_administrators.select().
                                                      where(companies_administrators.c.user_id == uid).
                                                      where(companies_administrators.c.company_id == cid))
        if admin_company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No matches found')
        else:
            await self.database.execute(companies_administrators.delete().where(companies_administrators.c.user_id == uid).
                                        where(companies_administrators.c.company_id == cid))
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'User {uid} deleted from company {cid} successfully')

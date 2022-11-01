from typing import List

from fastapi import Response, status, HTTPException

from base.base import database
from base.models import companies, users
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
        if not company.is_hide:
            if company is not None:
                response.status_code = status.HTTP_200_OK
                company = await self.database.fetch_one(companies.select().where(companies.c.id == id))
                return Company(**company)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company with id {id} not found')
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Company with id {id} is hided')

    async def get_all_companies(self) -> List[UserDisplayWithId]:
        companies_list = await self.database.fetch_all(query=companies.select())
        return companies_list

    async def update_company(
            self, id: int, company: CompanyUpdate, response: Response, current_user: UserDisplay)\
            -> CompanyUpdate:
        comp = await self.database.fetch_one(companies.select().where(companies.c.id == id))
        user = await self.database.fetch_one(users.select().where(users.c.id == id))
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

    async def hide_company(self):
        pass

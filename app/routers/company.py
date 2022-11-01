from typing import List

from fastapi import APIRouter, status, Depends, Response

from base.schemas import Company, CompanyUpdate, HTTPExceptionSchema
from services import company_services
from services.auth_services import get_current_user

router = APIRouter(
    prefix='/company',
    tags=['company']
)


@router.post('/create', response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_company(company: Company, response: Response, current_user=Depends(get_current_user)) -> Company:
    return await company_services.CompanyCRUD().create_company(
        company=company, response=response, current_user=current_user)


@router.get('/{id}', response_model=Company, status_code=status.HTTP_200_OK)
async def get_company_by_id(id: int, response: Response, current_user=Depends(get_current_user)) -> Company:
    return await company_services.CompanyCRUD().get_company_by_id(id=id, response=response)


@router.get('/', response_model=List[Company], status_code=status.HTTP_200_OK)
async def get_all_companies(current_user=Depends(get_current_user)) -> List[Company]:
    return await company_services.CompanyCRUD().get_all_companies()


@router.put('/{id}', response_model=CompanyUpdate)
async def update_company(id: int, company: CompanyUpdate, response: Response, current_user=Depends(get_current_user))\
        -> CompanyUpdate:
    return await company_services.CompanyCRUD().update_company(
        id=id, company=company, response=response, current_user=current_user)


@router.delete("/{id}", response_model=HTTPExceptionSchema)
async def delete_company(id: int, current_user=Depends(get_current_user)) -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().delete_company(id=id, current_user=current_user)

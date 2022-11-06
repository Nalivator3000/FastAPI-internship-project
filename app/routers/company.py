from typing import List

from fastapi import APIRouter, status, Depends, Response

from base.schemas import Company, CompanyUpdate, HTTPExceptionSchema, UserDisplayWithId, AllInvitesSchema
from services import company_services
from services.auth_services import get_current_user

router = APIRouter(
    prefix='/company',
    tags=['company']
)


@router.post('/create/', response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_company(company: Company, response: Response, current_user=Depends(get_current_user)) -> Company:
    return await company_services.CompanyCRUD().create_company(
        company=company, response=response, current_user=current_user)


@router.get('/{id}/', response_model=Company, status_code=status.HTTP_200_OK)
async def get_company_by_id(id: int, response: Response, current_user=Depends(get_current_user)) -> Company:
    return await company_services.CompanyCRUD().get_company_by_id(id=id, response=response)


@router.get('/', response_model=List[Company], status_code=status.HTTP_200_OK)
async def get_all_companies(response: Response, current_user=Depends(get_current_user)) -> list[Company]:
    return await company_services.CompanyCRUD().get_all_companies()


@router.put('/{id}/', response_model=CompanyUpdate)
async def update_company(id: int, company: CompanyUpdate, response: Response, current_user=Depends(get_current_user)) \
        -> CompanyUpdate:
    return await company_services.CompanyCRUD().update_company(
        id=id, company=company, response=response, current_user=current_user)


@router.delete("/{id}/", response_model=HTTPExceptionSchema)
async def delete_company(id: int, current_user=Depends(get_current_user)) -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().delete_company(id=id, current_user=current_user)


@router.post('/{user_id}/{company_id}/', response_model=HTTPExceptionSchema)
async def invite_user_to_company(company_id: int, user_id: int, current_user=Depends(get_current_user))\
        -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().invite_user_to_company(
        company_id=company_id, user_id=user_id, current_user=current_user
    )


@router.delete('/{user_id}/{company_id}/', response_model=HTTPExceptionSchema)
async def delete_user_from_company(company_id: int, user_id: int, current_user=Depends(get_current_user))\
        -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().delete_user_from_company(
        cid=company_id, uid=user_id, current_user=current_user
    )


@router.post('/me/invites/{company_id}/', response_model=HTTPExceptionSchema)
async def accept_invitation(answer: bool, company_id: int, current_user=Depends(get_current_user))\
        -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().accept_invitation(
        answer=answer, cid=company_id, current_user=current_user
    )


@router.put('/join/{company_id}/', response_model=HTTPExceptionSchema)
async def join_company(company_id: int, current_user=Depends(get_current_user)) -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().join_company(cid=company_id, current_user=current_user)


@router.post('/application/{company_id}/{user_id}/', response_model=HTTPExceptionSchema)
async def approve_application(answer: bool, user_id: int, company_id: int, current_user=Depends(get_current_user))\
        -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().approve_application(
        answer=answer, uid=user_id, cid=company_id, current_user=current_user
    )


@router.post('/admin/{company_id}/{user_id}/', response_model=HTTPExceptionSchema)
async def add_admin_to_company(company_id: int, user_id: int, current_user=Depends(get_current_user))\
        -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().add_admin_to_company(
        cid=company_id, uid=user_id, current_user=current_user
    )


@router.delete('/admin/{company_id}/{user_id}/', response_model=HTTPExceptionSchema)
async def delete_admin_from_company(user_id: int, company_id: int, current_user=Depends(get_current_user))\
        -> HTTPExceptionSchema:
    return await company_services.CompanyCRUD().delete_admin_from_company(
        uid=user_id, cid=company_id, current_user=current_user
    )


@router.get('/me/invites/', response_model=list[AllInvitesSchema])
async def get_all_invites(response: Response, current_user=Depends(get_current_user)) -> list[AllInvitesSchema]:
    return await company_services.CompanyCRUD().get_all_invites(current_user=current_user)


@router.get('/me/applications/', response_model=list[AllInvitesSchema])
async def get_all_applications(company_id: int, response: Response, current_user=Depends(get_current_user))\
        -> List[AllInvitesSchema]:
    return await company_services.CompanyCRUD().get_all_applications(cid=company_id, current_user=current_user)

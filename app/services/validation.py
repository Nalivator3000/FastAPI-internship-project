from pydantic import EmailStr

from base.schemas import UserUpdateRequestModel, Company, UserDisplay
from fastapi import HTTPException, status


def user_update_validation(current_user: UserUpdateRequestModel, user_id: str):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can edit only yours account')


def user_delete_validation(current_user: UserUpdateRequestModel, user_id: str):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can delete only yours account')


def company_update_validation(current_user: UserUpdateRequestModel, user_email: EmailStr):
    if current_user.email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can edit only yours companies')


def company_delete_validation(current_user: UserUpdateRequestModel, user_email: EmailStr):
    if current_user.email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can delete only yours companies')


def company_applications_validation(company: Company, current_user: UserDisplay):
    if company.owner != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You can see only applications to your companies')


def add_admin_validation(company: Company, current_user: UserDisplay):
    if company.owner != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You can add administrators only in your companies')


def delete_admin_validation(company: Company, current_user: UserDisplay):
    if company.owner != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You can delete administrators only from your companies')

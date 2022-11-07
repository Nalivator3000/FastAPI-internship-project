from pydantic import EmailStr

from base.base import database
from base.models import companies_administrators
from base.schemas import UserUpdateRequestModel, Company, UserDisplay, UserDisplayWithId, Quiz, DisplayQuestion, \
    DisplayQuiz
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


async def owner_or_admin_validation(company: Company, quiz: Quiz, current_user: UserDisplayWithId):
    try:
        is_admin = await database.fetch_one(companies_administrators.select().
                                            where(companies_administrators.c.user_id == current_user.id).
                                            where(companies_administrators.c.company_id == quiz.company_id)
                                            )
    finally:
        if company.owner != current_user.email and is_admin is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Only company owners or administrators can create quizzes')

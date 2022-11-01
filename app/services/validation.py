from base.schemas import UserUpdateRequestModel
from fastapi import HTTPException, status


def user_update_validation(current_user: UserUpdateRequestModel, user_id: str):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can edit only yours account')


def user_delete_validation(current_user: UserUpdateRequestModel, user_id: str):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can delete only yours account')

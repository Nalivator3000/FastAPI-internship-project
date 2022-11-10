from fastapi import APIRouter, status, Depends

from services import result_services
from services.auth_services import get_current_user

router = APIRouter(
    prefix='/result',
    tags=['result']
)


@router.get('/me/', status_code=status.HTTP_200_OK)
async def get_my_quizzes(current_user=Depends(get_current_user)):
    return await result_services.ResultCRUD().get_my_quizzes(current_user=current_user)


async def get_average():
    pass


async def get_average_by_quiz():
    pass


async def get_company_users():
    pass


async def get_my_average():
    pass


async def get_me_average_by_quiz():
    pass


async def my_quizzes():
    pass
from fastapi import APIRouter, status, Depends

from services import result_services
from services.auth_services import get_current_user

router = APIRouter(
    prefix='/result',
    tags=['result']
)


@router.get('/me/')
async def get_my_results(current_user=Depends(get_current_user)) -> list:
    return await result_services.ResultCRUD().get_my_results(current_user=current_user)


@router.get('/by_user/{user_d}')
async def get_user_results(user_id: int, current_user=Depends(get_current_user)) -> list:
    return await result_services.ResultCRUD().get_user_results(uid=user_id, current_user=current_user)


@router.get('/average/{quiz_id}')
async def get_average_by_quiz(quiz_id: int, current_user=Depends(get_current_user)) -> dict:
    return await result_services.ResultCRUD().get_average_by_quiz(quiz_id=quiz_id)


@router.get('/users/{company_id}')
async def get_company_users(company_id: int, current_user=Depends(get_current_user)) -> list:
    return await result_services.ResultCRUD().get_company_users(cid=company_id, current_user=current_user)


@router.get('/all-quizzes/')
async def get_average_by_all_quizzes(current_user=Depends(get_current_user)) -> list:
    return await result_services.ResultCRUD().get_average_by_all_quizzes()


@router.get('/all/average', status_code=status.HTTP_200_OK)
async def get_average(current_user=Depends(get_current_user)) -> str:
    return await result_services.ResultCRUD().get_average()


@router.get('/me/all', status_code=status.HTTP_200_OK)
async def get_my_average(current_user=Depends(get_current_user)) -> dict:
    return await result_services.ResultCRUD().get_my_average(current_user=current_user)


@router.get('/me/quizzes/', status_code=status.HTTP_200_OK)
async def get_my_quizzes(current_user=Depends(get_current_user)) -> list:
    return await result_services.ResultCRUD().get_my_quizzes(current_user=current_user)

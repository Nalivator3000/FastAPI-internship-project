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
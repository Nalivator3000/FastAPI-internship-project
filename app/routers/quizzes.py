from typing import List

from fastapi import APIRouter, status, Depends, Response

from base.schemas import Quiz, HTTPExceptionSchema, DisplayQuiz
from services import quiz_services
from services.auth_services import get_current_user
from services.validation import take_quiz_validation

router = APIRouter(
    prefix='/quiz',
    tags=['quiz']
)


@router.post('/create/', response_model=Quiz, status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: Quiz, response: Response, current_user=Depends(get_current_user)) -> Quiz:
    return await quiz_services.QuizCRUD().create_quiz(
        quiz=quiz, response=response, current_user=current_user)


@router.put('/{id}/', response_model=Quiz)
async def update_quiz(id: int, quiz: Quiz, response: Response, current_user=Depends(get_current_user)) \
        -> Quiz:
    return await quiz_services.QuizCRUD().update_quiz(
        id=id, quiz=quiz, response=response, current_user=current_user)


@router.delete("/{id}/", response_model=HTTPExceptionSchema)
async def delete_quiz(id: int, current_user=Depends(get_current_user)) -> HTTPExceptionSchema:
    return await quiz_services.QuizCRUD().delete_quiz(id=id, current_user=current_user)


@router.get('/{company_id}/', response_model=List[DisplayQuiz], status_code=status.HTTP_200_OK)
async def get_company_quizzes(company_id: int, current_user=Depends(get_current_user)) -> List[DisplayQuiz]:
    return await quiz_services.QuizCRUD().get_company_quizzes(cid=company_id)


@router.get('/take/{quiz_id}', status_code=status.HTTP_200_OK)
async def take_quiz(quiz_id: int, current_user=Depends(get_current_user)):
    return await quiz_services.QuizCRUD().take_quiz(quiz_id=quiz_id, current_user=current_user)

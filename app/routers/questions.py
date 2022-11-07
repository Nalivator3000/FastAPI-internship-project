from typing import List

from fastapi import APIRouter, status, Response, Depends

from base.schemas import Question, HTTPExceptionSchema, DisplayQuestion, DisplayQuestionWithId
from services import question_services
from services.auth_services import get_current_user

router = APIRouter(
    prefix='/question',
    tags=['question']
)


@router.post('/create/', response_model=Question, status_code=status.HTTP_201_CREATED)
async def create_quiz(question: Question, response: Response, current_user=Depends(get_current_user)) -> Question:
    return await question_services.QuestionCRUD().create_question(
        question=question, response=response, current_user=current_user)


@router.delete('/delete/{id}', response_model=HTTPExceptionSchema, status_code=status.HTTP_200_OK)
async def delete_question(id: int, current_user=Depends(get_current_user)) \
        -> HTTPExceptionSchema:
    return await question_services.QuestionCRUD().delete_question(id=id, current_user=current_user)


@router.get('/all/', response_model=List[DisplayQuestion], status_code=status.HTTP_200_OK)
async def get_all_questions(current_user=Depends(get_current_user)) -> List[DisplayQuestion]:
    return await question_services.QuestionCRUD().get_all_questions()


@router.get('/{id}/', response_model=DisplayQuestion, status_code=status.HTTP_200_OK)
async def get_question_by_id(id: int, current_user=Depends(get_current_user)) -> DisplayQuestion:
    return await question_services.QuestionCRUD().get_question_by_id(id=id)


@router.get('/quiz/{quiz_id}', status_code=status.HTTP_200_OK, response_model=List[DisplayQuestionWithId])
async def get_quiz_questions(quiz_id: int, current_user=Depends(get_current_user)) -> List[DisplayQuestionWithId]:
    return await question_services.QuestionCRUD().get_quiz_questions(quiz_id=quiz_id)

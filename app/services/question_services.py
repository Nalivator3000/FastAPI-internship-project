from typing import List

from base.base import database
from fastapi import Response, HTTPException, status

from base.models import quizzes, questions, companies
from base.schemas import Question, UserDisplayWithId, HTTPExceptionSchema, DisplayQuestion, DisplayQuestionWithId
from services.validation import owner_or_admin_validation


class QuestionCRUD:
    def __init__(self):
        self.database = database

    async def create_question(
            self, question: Question, response: Response, current_user: UserDisplayWithId
    ) -> Question:
        is_quiz_exist = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == question.quiz_id))
        if not is_quiz_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz #{question.quiz_id} not found')
        company = await self.database.fetch_one(companies.select().where(companies.c.id == is_quiz_exist.company_id))
        await owner_or_admin_validation(company=company, current_user=current_user, quiz=is_quiz_exist)
        response.status_code = status.HTTP_201_CREATED
        query = questions.insert().values(
            question=question.question,
            options=question.options,
            answer=question.answer,
            quiz_id=question.quiz_id
        )

        if len(question.options) < 2:
            raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                                detail='Question must have more than one option')

        if question.answer not in question.options:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='At least one of options must be right')

        record_id = await self.database.execute(query)
        row = await self.database.fetch_one(questions.select().where(questions.c.id == record_id))

        return Question(**row)

    async def delete_question(self, id: int, current_user: UserDisplayWithId)\
        -> HTTPExceptionSchema:
        question = await self.database.fetch_one(questions.select().where(questions.c.id == id))
        quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == question.quiz_id))
        company = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
        await owner_or_admin_validation(company=company, current_user=current_user, quiz=quiz)
        if question is not None:
            await self.database.execute(questions.delete().where(questions.c.id == id))
            raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Question #{id} deleted successfully')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Question with id #{id} not found')

    async def get_all_questions(self) -> List[DisplayQuestion]:
        all_questions = await self.database.fetch_all(questions.select())
        return all_questions

    async def get_question_by_id(self, id: int) -> DisplayQuestion:
        question = await self.database.fetch_one(questions.select().where(questions.c.id == id))
        return question

    async def get_quiz_questions(self, quiz_id: int) -> List[DisplayQuestionWithId]:
        quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == quiz_id))
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz #{quiz_id} not found')
        quest = await self.database.fetch_all(questions.select().where(questions.c.quiz_id == quiz_id))
        return quest

    # async def add_question_to_quiz(self, quiz_id: int, question_id: int, current_user: UserDisplayWithId)\
    #         -> QuestionQuiz:
    #     question = await self.database.fetch_one(questions.select().where(questions.c.id == question_id))
    #     if not question:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Question #{question_id} not found')
    #     quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == quiz_id))
    #     if not quiz:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz #{quiz_id} not found')
    #     company = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
    #     await owner_or_admin_validation(company=company, current_user=current_user, quiz=quiz)
    #     await self.database.execute(question_quiz.insert().values(quiz_id=quiz_id, question_id=question_id))
    #     row = self.database.fetch_one(question_quiz.select().
    #                                   where(question_quiz.c.quiz_id == quiz_id).
    #                                   where(question_quiz.c.question_id == question_id)
    #                                   )
    #     return QuestionQuiz(**row)


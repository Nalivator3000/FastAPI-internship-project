import datetime
import random
from typing import List

from base.base import database
from fastapi import Response, status, HTTPException

from base.models import quizzes, companies, questions, results
from base.redis import set_redis
from base.schemas import Quiz, UserDisplayWithId, HTTPExceptionSchema, DisplayQuiz, Result
from services.validation import owner_or_admin_validation, take_quiz_validation


class QuizCRUD:
    def __init__(self):
        self.database = database

    async def create_quiz(self, quiz: Quiz, response: Response, current_user: UserDisplayWithId) -> Quiz:
        is_company_exist = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
        if not is_company_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company #{quiz.company_id} not found')
        await owner_or_admin_validation(company=is_company_exist, current_user=current_user, quiz=quiz)
        response.status_code = status.HTTP_201_CREATED
        query = quizzes.insert().values(
            name=quiz.name,
            description=quiz.description,
            frequency=quiz.frequency,
            company_id=quiz.company_id
        )

        record_id = await self.database.execute(query)
        row = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == record_id))

        return Quiz(**row)

    async def update_quiz(
            self, id: int, quiz: Quiz, response: Response, current_user: UserDisplayWithId) \
            -> Quiz:
        current_quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == id))
        company = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
        await owner_or_admin_validation(company=company, current_user=current_user, quiz=quiz)
        if current_quiz is not None:
            response.status_code = status.HTTP_200_OK
            query = quizzes.update().where(quizzes.c.id == id).values(
                name=quiz.name,
                description=quiz.description,
                frequency=quiz.frequency,
                id=id
            )

            await self.database.execute(query)
            query = quizzes.select().where(quizzes.c.id == current_quiz.id)
            row = await self.database.fetch_one(query)

            return DisplayQuiz(**row)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz with id #{id} not found')

    async def delete_quiz(self, id: int, current_user: UserDisplayWithId) -> HTTPExceptionSchema:
        quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == id))
        company = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
        await owner_or_admin_validation(company=company, current_user=current_user, quiz=quiz)
        if quiz is not None:
            await self.database.execute(quizzes.delete().where(quizzes.c.id == id))
            raise HTTPException(status_code=status.HTTP_200_OK, detail=f'Quiz {id} deleted successfully')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Quiz with id {id} not found')

    async def get_company_quizzes(self, cid: int) -> List[DisplayQuiz]:
        company = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company #{cid} not found')
        return await self.database.fetch_all(quizzes.select().where(quizzes.c.company_id == cid))

    async def take_quiz(self, quiz_id: int, current_user: UserDisplayWithId):
        await take_quiz_validation(quiz_id=quiz_id, current_user=current_user)
        all_questions = await self.database.fetch_all(questions.select().where(questions.c.quiz_id == quiz_id))
        # answers = {}
        result = 0
        for i in range(len(all_questions)):
            option_id = random.randint(0, len(all_questions[i].options)-1)
            if all_questions[i].options[int(option_id)] == all_questions[i].answer:
                result += 1
            question = await self.database.fetch_one(questions.select().
                                                     where(questions.c.question == all_questions[i].question))
            # answers[f'{all_questions[i].question}'] = f'{all_questions[i].options[option_id]}'
            # print(answers)
            set_redis(key=f'{quiz_id},{question.id},{current_user.id},{datetime.date.today()}',
                      val=all_questions[i].options[int(option_id)])

        quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == quiz_id))
        query = results.insert().values(
            user_id=current_user.id,
            company_id=quiz.company_id,
            quiz_id=quiz.id,
            questions=len(all_questions),
            right_answers=result
        )

        record_id = await self.database.execute(query)
        row = await self.database.fetch_one(results.select().where(results.c.id == record_id))

        return Result(**row)


import csv
import datetime
import random
from typing import List

from base.base import database
from fastapi import Response, status, HTTPException
from fastapi.responses import FileResponse

from base.models import quizzes, companies, questions, results
from base.redis import set_redis, find_records
from base.schemas import Quiz, UserDisplayWithId, HTTPExceptionSchema, DisplayQuiz, QuizAnswers
from services.validation import owner_or_admin_validation, take_quiz_validation


class QuizCRUD:
    def __init__(self):
        self.database = database

    async def create_quiz(self, quiz: Quiz, response: Response, current_user: UserDisplayWithId) -> Quiz:
        is_company_exist = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
        if not is_company_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Company #{quiz.company_id} not found')
        await owner_or_admin_validation(current_user=current_user, company=is_company_exist, quiz=quiz)
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
        await owner_or_admin_validation(current_user=current_user, company=company, quiz=quiz)
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
        await owner_or_admin_validation(current_user=current_user, company=company, quiz=quiz)
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

    async def take_quiz(self, answer_dict: dict, current_user: UserDisplayWithId) -> QuizAnswers:
        quiz_id = answer_dict.get('quiz_id')
        await take_quiz_validation(quiz_id=quiz_id, current_user=current_user)
        all_questions = await self.database.fetch_all(questions.select().where(questions.c.quiz_id == quiz_id))
        result = 0
        for i in range(len(all_questions)):
            if answer_dict.get('answers').get(f'{i}') == all_questions[i].answer:
                result += 1
            question = await self.database.fetch_one(questions.select().
                                                     where(questions.c.question == all_questions[i].question))
            set_redis(key=f'{quiz_id}--{current_user.id}--{question.id}--{datetime.date.today()}',
                      val=str(answer_dict.get('answers').get(f'{i}')))

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

        return QuizAnswers(**row)

    async def get_answers_by_quiz_id(self, quiz_id: int, current_user: UserDisplayWithId) -> str:
        records = find_records(quiz_id=quiz_id, user_id=int(current_user.id))
        my_dict = {}
        for i in range(len(records)):
            record = records[i].split('--')
            question = await self.database.fetch_one(questions.select().where(questions.c.id == int(record[2])))
            my_dict.update({f'{record[-2]}-{question.question}': record[-1]})
        with open(f'User{current_user.id}_Quiz{quiz_id}_report.csv', 'w') as f:
            w = csv.DictWriter(f, my_dict.keys())
            w.writeheader()
            w.writerow(my_dict)
        return FileResponse(f'User{current_user.id}_Quiz{quiz_id}_report.csv',
                            status_code=status.HTTP_200_OK,
                            media_type="text/csv")

    async def get_answers_by_company(self, cid: int, current_user: UserDisplayWithId, uid: int = None):
        company = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        await owner_or_admin_validation(current_user=current_user, company=company)
        quiz_list = await self.get_company_quizzes(cid=cid)
        quiz_id_list = []
        for i in range(len(quiz_list)):
            quiz_id_list.append(quiz_list[i].id)
        my_dict = {}
        for i in range(len(quiz_id_list)):
            records = find_records(quiz_id=quiz_id_list[i], user_id=uid)
            for j in range(len(records)):
                record = records[j].split('--')
                question = await self.database.fetch_one(questions.select().where(questions.c.id == int(record[2])))
                my_dict.update({f'{record[-2]}-{question.question}': record[-1]})
        with open(f'User{uid}_Company{cid}_report.csv', 'w') as f:
            w = csv.DictWriter(f, my_dict.keys())
            w.writeheader()
            w.writerow(my_dict)
        return FileResponse(f'User{uid}Company{cid}_report.csv',
                            status_code=status.HTTP_200_OK,
                            media_type="text/csv")

    async def get_quiz_answers(self, user_id: int, quiz_id: int, current_user: UserDisplayWithId) -> str:
        quiz = await self.database.fetch_one(quizzes.select().where(quizzes.c.id == quiz_id))
        company = await self.database.fetch_one(companies.select().where(companies.c.id == quiz.company_id))
        await owner_or_admin_validation(current_user=current_user, company=company, quiz=quiz)
        records = find_records(quiz_id=quiz_id, user_id=user_id)
        my_dict = {}
        for i in range(len(records)):
            record = records[i].split('--')
            question = await self.database.fetch_one(questions.select().where(questions.c.id == int(record[2])))
            my_dict.update({f'{record[-2]}-{question.question}': record[-1]})
        with open(f'User{current_user.id}_Quiz{quiz_id}_report.csv', 'w') as f:
            w = csv.DictWriter(f, my_dict.keys())
            w.writeheader()
            w.writerow(my_dict)
        return FileResponse(f'User{user_id}_Quiz{quiz_id}_report.csv',
                            status_code=status.HTTP_200_OK,
                            media_type="text/csv")

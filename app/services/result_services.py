from fastapi import HTTPException, status

from base.base import database
from base.schemas import UserDisplayWithId
from base.models import results, companies, companies_administrators, quizzes, companies_users, users, questions
from services.validation import owner_or_admin_validation


class ResultCRUD:
    def __init__(self):
        self.database = database

    async def get_my_results(self, current_user: UserDisplayWithId) -> list:
        all_companies = await self.get_my_companies(current_user=current_user)
        quiz_list = []
        for i in range(0, len(all_companies)):
            company_quizzes = await self.database.fetch_all(quizzes.select().
                                                            where(quizzes.c.company_id == all_companies[i].id))
            if company_quizzes is not None:
                for j in range(0, len(company_quizzes)):
                    quiz_list.append(company_quizzes[j])
        result_list = []
        for i in range(0, len(quiz_list)):
            quiz_results = await self.database.fetch_all(results.select().where(results.c.quiz_id == quiz_list[i].id))
            for j in range(0, len(quiz_results)):
                result_list.append(quiz_results[j])
        return result_list

    async def get_my_companies(self, current_user: UserDisplayWithId) -> list:
        owner_list = await self.database.fetch_all(companies.select().where(companies.c.owner == current_user.email))
        admin_companies = await self.database.fetch_all(companies_administrators.select().
                                                        where(companies_administrators.c.user_id == current_user.id))
        admin_list = []
        for i in range(0, len(admin_companies)):
            admin = await self.database.fetch_one(companies.select().
                                                  where(companies.c.id == admin_companies[i].company_id))
            admin_list.append(admin)
        all_companies = owner_list + admin_list
        return all_companies

    async def get_user_results(self, uid: int, current_user: UserDisplayWithId) -> list:
        result_list = await self.get_my_results(current_user=current_user)
        user_results = []
        for i in range(0, len(result_list)):
            if result_list[i].user_id == uid:
                user_results.append(result_list[i])
        return user_results

    async def get_company_users(self, cid: int, current_user: UserDisplayWithId) -> list:
        is_exist = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        if is_exist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
        company = await self.database.fetch_one(companies.select().where(companies.c.id == cid))
        await owner_or_admin_validation(current_user=current_user, company=company)
        company_users = await self.database.fetch_all(companies_users.select().
                                                      where(companies_users.c.company_id == cid))
        users_list = []
        for i in range(0, len(company_users)):
            user = await self.database.fetch_one(users.select().where(users.c.id == company_users[i].user_id))
            if user is not None:
                users_list.append(user)
        last_results = []
        for i in range(0, len(users_list)):
            user_results = await self.get_my_results(current_user=users_list[i])
            if not user_results:
                never_passed = {"user_id": users_list[i].id,
                                "company_id": cid,
                                "quiz_id": 9999,
                                "questions": 9999,
                                "right_answers": 9999,
                                "time": "User never passed this company quizzes"}
                last_results.append(never_passed)
                continue
            time_list = []
            for j in range(0, len(user_results)):
                time_list.append(user_results[j].time)
            last_time = max(time_list)
            last_result = await self.database.fetch_one(results.select().
                                                        where(results.c.user_id == user_results[j].user_id).
                                                        where(results.c.time == last_time)
                                                        )
            res = {"user_id": last_result.user_id,
                   "company_id": last_result.company_id,
                   "quiz_id": last_result.quiz_id,
                   "questions": last_result.questions,
                   "right_answers": last_result.right_answers,
                   "time": last_result.time}
            last_results.append(res)
        return last_results

    async def get_average_by_quiz(self, quiz_id: int) -> dict:
        result_list = await self.database.fetch_all(results.select().where(results.c.quiz_id == quiz_id))
        if result_list:
            count_questions = result_list[0].questions
            right_answers = []
            for i in range(0, len(result_list)):
                right_answers.append(result_list[i].right_answers)
            average = sum(right_answers) / len(right_answers) / count_questions
            return {'quiz_id': quiz_id, 'average': average, 'number_or_question': count_questions}

    async def get_average_by_all_quizzes(self) -> list:
        all_quizzes = await self.database.fetch_all(quizzes.select())
        average_list = []
        for i in range(0, len(all_quizzes)):
            average = await self.get_average_by_quiz(quiz_id=all_quizzes[i].id)
            if average is not None:
                average_list.append(average)
        return average_list

    async def get_average(self) -> str:
        average_list = await self.get_average_by_all_quizzes()
        average_ints = []
        average_number_of_question =[]
        for i in range(0, len(average_list)):
            average_ints.append(float(average_list[i].get('average')))
            average_number_of_question.append(float(average_list[i].get('number_or_question')))
        return f'Average of all users on all quizzes: ' \
               f'{sum(average_ints) / len(average_ints) / sum(average_number_of_question) * 100:.2f}%'

    async def get_my_average(self, current_user: UserDisplayWithId) -> dict:
        return await self.get_average_by_user(uid=current_user.id)

    async def get_average_by_user(self, uid: int) -> dict:
        result_list = await self.database.fetch_all(results.select().where(results.c.user_id == uid))
        if not result_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Results not found')
        count_questions = result_list[0].questions
        right_answers = []
        for i in range(0, len(result_list)):
            right_answers.append(result_list[i].right_answers)
        average = sum(right_answers) / len(right_answers) / count_questions
        return {'user_id': uid, 'average': f'{average} from {count_questions}'}

    async def get_my_quizzes(self, current_user: UserDisplayWithId) -> list:
        my_companies_users = await self.database.fetch_all(companies_users.select().
                                                           where(companies_users.c.user_id == current_user.id))
        quizzes_list = []
        for i in range(0, len(my_companies_users)):
            quiz = await self.database.fetch_all(quizzes.select().
                                                 where(quizzes.c.company_id == int(my_companies_users[i].company_id)))
            for j in range(0, len(quiz)):
                quizzes_list.append(quiz[j])
        average_with_last_time = []
        for k in range(0, len(quizzes_list)):
            quizz_questions = await self.database.fetch_all(questions.select().
                                                            where(questions.c.quiz_id == quizzes_list[k].id))
            number_of_question = len(quizz_questions)
            if number_of_question == 0:
                record = {
                    'Quiz id': quizzes_list[k].id,
                    'Average score': None,
                    'Last pass': None
                }
                average_with_last_time.append(record)
                continue
            quiz_results = await self.database.fetch_all(results.select().
                                                         where(results.c.quiz_id == quizzes_list[k].id).
                                                         where(results.c.user_id == current_user.id)
                                                         )
            right_answers_list = []
            for n in range(0, len(quiz_results)):
                right_answers_list.append(quiz_results[n].right_answers)
            average_by_quiz = sum(right_answers_list) / (int(number_of_question) * len(quiz_results))
            average_score = f'{average_by_quiz} from {number_of_question}'
            time_list = []
            for m in range(0, len(quiz_results)):
                time_list.append(quiz_results[m].time)
            last_time = max(time_list)
            last_result = await self.database.fetch_one(results.select().
                                                        where(results.c.user_id == quiz_results[k].user_id).
                                                        where(results.c.time == last_time)
                                                        )
            record = {
                'Quiz id': quizzes_list[k].id,
                'Average score': average_score,
                'Last pass': last_result.time
            }
            average_with_last_time.append(record)

        return average_with_last_time

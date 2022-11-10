from base.base import database
from base.schemas import UserDisplayWithId
from base.models import results


class ResultCRUD:
    def __init__(self):
        self.database = database

    async def get_my_quizzes(self, current_user: UserDisplayWithId):
        result = await self.database.fetch_all(results.select().where(results.c.user_id == current_user.id))
        return result

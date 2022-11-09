import datetime
from typing import List

from pydantic import BaseModel, EmailStr
import os


class UserDisplay(BaseModel):
    name: str
    email: str
    bio: str = None

    class Config:
        orm_mode = True


class UserDisplayWithId(UserDisplay):
    id: int


class SignUpRequestModel(UserDisplay):
    password: str
    time_created: datetime.datetime


class UserUpdateRequestModel(BaseModel):
    name: str
    password: str
    bio: str
    time_updated: datetime.datetime

    class Config:
        orm_mode = True


class User(UserDisplayWithId):
    time_updated: str


class SignInRequestModel(BaseModel):
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'email': 'this_is@your.email',
                'password': 'password_which_you_forgot'
            }
        }


class HTTPExceptionSchema(BaseModel):
    status_code: str
    detail: str

    class Config:
        schema_extra = {"detail": "HTTPException raised."}


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ["SECRET_KEY"]


class Token(BaseModel):
    access_token: str


class CompanyUpdate(BaseModel):
    name: str
    description: str
    is_hide: bool
    id: int

    class Config:
        orm_mode = True


class Company(CompanyUpdate):
    owner: EmailStr


class AllInvitesSchema(BaseModel):
    user_id: int
    company_id: int


class Quiz(BaseModel):
    name: str
    description: str
    frequency: int
    company_id: int

    class Config:
        orm_mode = True


class DisplayQuiz(Quiz):
    id: int


class Question(BaseModel):
    question: str
    options: List[str]
    answer: str
    quiz_id: int

    class Config:
        orm_mode = True


class DisplayQuestion(Question):
    id: int


class DisplayQuestionWithId(BaseModel):
    id: int
    options: List[str]
    answer: str
    quiz_id: int

    class Config:
        orm_mode = True


class QuestionQuiz(BaseModel):
    quiz_id: int
    question_id: int


class Result(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    questions: int
    right_answers: int
    time: datetime.datetime

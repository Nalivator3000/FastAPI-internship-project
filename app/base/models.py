from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Table, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

companies_users = Table(
    'companies_users',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('company_id', ForeignKey('companies.id'))
)

companies_administrators = Table(
    'companies_administrators',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('company_id', ForeignKey('companies.id'))
)

invites = Table(
    'invites',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('company_id', ForeignKey('companies.id'))
)

applications = Table(
    'applications',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('company_id', ForeignKey('companies.id'))
)

# question_quiz = Table(
#     'question_quiz',
#     Base.metadata,
#     Column('quiz_id', ForeignKey('quizzes.id')),
#     Column('question_id', ForeignKey('questions.id'))
# )


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    bio = Column(String, default=None, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    users_companies = relationship(
        'DbCompany', secondary=companies_users, backref='companies_users'
    )
    company_administrators = relationship(
        'DbCompany', secondary=companies_administrators, backref='companies_administrators'
    )


users = DbUser.__table__


class DbCompany(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_hide = Column(Boolean, nullable=False)
    owner = Column(String, ForeignKey('users.email'))
    quizzes = relationship('DbQuestion')


companies = DbCompany.__table__


class DbQuiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    frequency = Column(Integer, nullable=False)
    questions = relationship('DbQuestion', back_populates='question_quiz')
    company_id = Column(Integer, ForeignKey('companies.id'))


quizzes = DbQuiz.__table__


class DbQuestion(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    options = Column(ARRAY(String), nullable=False)
    answer = Column(String, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    question_quiz = relationship('DbQuiz', back_populates='questions')


questions = DbQuestion.__table__


class DbResult(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    questions = Column(Integer, nullable=False)
    right_answers = Column(Integer, nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())


results = DbResult.__table__

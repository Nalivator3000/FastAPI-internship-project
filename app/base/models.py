from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Table
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


companies = DbCompany.__table__

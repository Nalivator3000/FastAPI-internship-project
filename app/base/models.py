from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


companies_users = Table(
    'companies_users',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('company_id', ForeignKey('companies.id')),
    Column('is_active_owner', Boolean),
    Column('is_active_user', Boolean)
)


# class CompaniesUsers(Base):
#     __tablename__ = 'companies_users'
#     user_id = Column(ForeignKey('users.id'), primary_key=True)
#     company_id = Column(ForeignKey('companies.id'), primary_key=True)
#     user = relationship('DbUser', back_populates='companies')
#     company = relationship('DbCompany', back_populates='users')


# companies_users = CompaniesUsers.__table__


companies_administrators = Table(
    'companies_administrators',
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
    company_administrators = relationship('DbCompany', secondary=companies_administrators)


users = DbUser.__table__


class DbCompany(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_hide = Column(Boolean, nullable=False)
    owner = Column(String, ForeignKey('users.email'))
    # companies_users = relationship(
    #     'CompaniesUsers', secondary=companies_users, back_populates='users_companies'
    # )


companies = DbCompany.__table__

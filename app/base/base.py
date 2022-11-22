from databases import Database
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import os

load_dotenv()

metadata = MetaData()

database = Database(os.getenv('ASYNC_DB_URL'))

engine = create_engine(os.getenv('ASYNC_DB_URL'), connect_args={"check_same_thread": False}, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

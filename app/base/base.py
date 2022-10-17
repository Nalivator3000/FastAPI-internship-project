from databases import Database
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
import os

load_dotenv()

db = Database(os.getenv('DATABASE_URL'))
engine = create_engine(os.getenv('DATABASE_URL'), connect_args={"check_same_thread": False})

metadata = MetaData()

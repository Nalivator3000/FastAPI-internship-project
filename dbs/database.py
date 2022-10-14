from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

db = Database(os.getenv('DATABASE_URL'))

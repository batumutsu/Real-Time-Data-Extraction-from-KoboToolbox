from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv
import os

load_dotenv()

#DATABASE_URL = "postgresql://quick_start:quick_start@localhost/inkomoko"
DATABASE_URL = "mysql+pymysql://batumutsu:inkomoko@batumutsu.mysql.pythonanywhere-services.com/batumutsu$inkomoko"

# DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
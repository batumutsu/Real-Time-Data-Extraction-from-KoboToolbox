from sqlalchemy import Column, String, Date, DateTime, Integer, func, BINARY
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

def generate_uuid():
    return uuid.uuid4().bytes

class KoboRecord(Base):
    __tablename__ = "kobo_records"
    
    id = Column(BINARY(16), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    kobo_id = Column(Integer, unique=True, index=True)
    survey_date = Column(Date)
    unique_id = Column(String)
    country = Column(String)
    region = Column(String)
    bda_name = Column(String)
    cohort = Column(String)
    program = Column(String)
    client_name = Column(String)
    client_id = Column(String)
    location = Column(String)
    phone = Column(String)
    gender = Column(String)
    age = Column(Integer)
    nationality = Column(String)
    education = Column(String)
    business_status = Column(String)
    submission_time = Column(DateTime)
    inserted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

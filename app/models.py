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
    unique_id = Column(String(255))
    country = Column(String(255))
    region = Column(String(255))
    bda_name = Column(String(255))
    cohort = Column(String(255))
    program = Column(String(255))
    client_name = Column(String(255))
    client_id = Column(String(255))
    location = Column(String(255))
    phone = Column(String(255))
    gender = Column(String(255))
    age = Column(Integer)
    nationality = Column(String(255))
    education = Column(String(255))
    business_status = Column(String(255))
    submission_time = Column(DateTime)
    inserted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

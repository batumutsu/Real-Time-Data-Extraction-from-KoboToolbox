from sqlalchemy import Column, String, Date, DateTime, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import CHAR
import uuid

Base = declarative_base()

class KoboRecord(Base):
    __tablename__ = "kobo_records"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
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
    inserted_at = Column(DateTime(timezone=True), insert_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
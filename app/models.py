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
    unique_id = Column(String(255))  # Set length to 255, or whatever is appropriate
    country = Column(String(255))
    region = Column(String(255))
    bda_name = Column(String(255))
    cohort = Column(String(255))
    program = Column(String(255))
    client_name = Column(String(255))
    client_id = Column(String(255))
    location = Column(String(255))
    phone = Column(String(20))  # Adjust length according to the format you expect
    gender = Column(String(10))  # Adjust length according to the values you expect (e.g., "Male", "Female")
    age = Column(Integer)
    nationality = Column(String(255))
    education = Column(String(255))
    business_status = Column(String(255))
    submission_time = Column(DateTime)
    inserted_at = Column(DateTime(timezone=True), insert_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

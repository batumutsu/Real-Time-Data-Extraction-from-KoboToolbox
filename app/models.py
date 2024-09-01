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
    unique_id = Column(String(255), nullable=False, index=True)
    country = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    bda_name = Column(String(255), nullable=False)
    cohort = Column(String(255), nullable=False)
    program = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    client_id = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    alt_phone = Column(String(255), nullable=True)
    phone_smart_feature = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    nationality = Column(String(255), nullable=False)
    strata = Column(String(255), nullable=False)
    disability = Column(String(255), default="No")
    education = Column(String(255), nullable=False)
    client_status = Column(String(255), nullable=False)
    sole_income_earner = Column(String(255), default="Yes")
    responsible_people = Column(Integer, nullable=False)
    business_status = Column(String(255), nullable=False)
    business_operating = Column(String(255), nullable=True)
    submission_time = Column(DateTime, nullable=False)
    inserted_at = Column(DateTime(timezone=True), insert_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

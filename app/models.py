from sqlalchemy import Column, String, Date, DateTime, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import VARCHAR  # Import VARCHAR for MySQL string type

Base = declarative_base()

class KoboRecord(Base):
    __tablename__ = "kobo_records"  # Use double underscores for table name
    id = Column(String(length=36), primary_key=True, unique=True, nullable=False)
    kobo_id = Column(Integer, unique=True, index=True)
    survey_date = Column(Date)
    unique_id = Column(VARCHAR(length=255))  # Use VARCHAR for potentially long strings
    country = Column(VARCHAR(length=255))
    region = Column(VARCHAR(length=255))
    bda_name = Column(VARCHAR(length=255))
    cohort = Column(VARCHAR(length=255))
    program = Column(VARCHAR(length=255))
    client_name = Column(VARCHAR(length=255))
    client_id = Column(VARCHAR(length=255))
    location = Column(VARCHAR(length=255))
    phone = Column(VARCHAR(length=255))
    gender = Column(VARCHAR(length=255))
    age = Column(Integer)
    nationality = Column(VARCHAR(length=255))
    education = Column(VARCHAR(length=255))
    business_status = Column(VARCHAR(length=255))
    submission_time = Column(DateTime)
    inserted_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
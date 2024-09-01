from .kobo_api import fetch_and_save_data
from .webhook import register_webhook
from .database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_extracted_records():
    try:
        db: Session = next(get_db())
        fetch_and_save_data(db)
        logger.info("Records saved successfully")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred while saving records: {str(e)}")
    finally:
        db.close()
        
    webhookResponse = register_webhook()
    logger.info("Webhook registered successfully with response: " + webhookResponse.text)

if __name__ == "__main__":
    save_extracted_records()
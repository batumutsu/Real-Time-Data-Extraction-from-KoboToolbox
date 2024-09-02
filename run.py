from app.main import save_extracted_records
from app.webhook import app
from app.database import init_db, engine
from app.models import Base

if __name__ == "__main__":
    # Base.metadata.drop_all(bind=engine)  # This drops all tables better to use it once only.
    init_db()  # This creates all tables
    save_extracted_records()
    app.run(host='0.0.0.0', port=4000)
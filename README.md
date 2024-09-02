# Real Time Data Extraction from KoboToolbox

This project extracts data from KoboToolbox and saves it to a database, handling real-time updates for new records and edits.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
6. Get mySQL running: `docker-compose up -d`(This will require docker to be installed)
7. Create test database: `docker-compose exec -T mysql mysql -u root -p quick_start -e "CREATE DATABASE test_db;"`
8. Create test user: `docker-compose exec -T mysql mysql -u root -p quick_start -e "CREATE USER 'test_user'@'%' IDENTIFIED BY 'test_user';"`
9. Grant permissions to test user: `docker-compose exec -T mysql mysql -u root -p quick_start -e "GRANT ALL PRIVILEGES ON *.* TO 'test_user'@'%' WITH GRANT OPTION;"`
10. Reload permissions: `docker-compose exec -T mysql mysql -u root -p quick_start -e "FLUSH PRIVILEGES;"`
11. Create .env file and add these variables:
    1. `DATABASE_URL` : "mysql+pymysql://username:password@localhost/databasename"
    2. `DATABASE_TEST_URL` : "mysql+pymysql://test_user:test_user@localhost/test_db"
    3. `INKOMOKO_REGISTER_WEBHOOK_URL` : "http://dev.inkomoko.com:1055/register_webhook"
    4. `REAL_TIME_POST_ENDPOINT_URL` : "https://batumutsu.pythonanywhere.com/api/real-time-updates"
    5. `KOBO_TOKEN` : "f24b97a52f76779e97b0c10f80406af5e9590eaf"
    6. `KOBO_ASSET_ID` : "aW9w8jHjn4Cj8SSQ5VcojK"
12. Run the initial data extraction, register the webhook server and start the webhook server: `python run.py`
13. Run tests: `python -m pytest`

## Usage

- The initial data extraction is performed by running `app/main.py`
- Real-time updates are handled by the webhook endpoint at `/api/real-time-updates`
- The webhook will be registered using the URL variable in .env file called `REAL_TIME_POST_ENDPOINT_URL`

## Database Schema

The database uses a single table `kobo_records` with the following schema:

- `id`: BINARY(16), primary key, unique identifier generated using UUID, not nullable
- `kobo_id`: Integer, unique identifier from KoboToolbox, indexed
- `survey_date`: Date, records the date of the survey
- `unique_id`: String(255), a unique identifier for the record, indexed, not nullable
- `country`: String(255), the country associated with the record, not nullable
- `region`: String(255), the region associated with the record, not nullable
- `bda_name`: String(255), name of the BDA, not nullable
- `cohort`: String(255), cohort information, not nullable
- `program`: String(255), program associated with the record, not nullable
- `client_name`: String(255), name of the client, not nullable
- `client_id`: String(255), identifier for the client, not nullable
- `location`: String(255), location information, not nullable
- `phone`: String(255), primary phone number, not nullable
- `alt_phone`: String(255), alternative phone number, nullable
- `phone_smart_feature`: String(255), specifies if the phone is smart or feature, not nullable
- `gender`: String(255), gender of the client, not nullable
- `age`: Integer, age of the client, not nullable
- `nationality`: String(255), nationality of the client, not nullable
- `strata`: String(255), strata information, not nullable
- `disability`: String(255), indicates if the client has a disability, defaults to "No"
- `education`: String(255), educational background of the client, not nullable
- `client_status`: String(255), status of the client, not nullable
- `sole_income_earner`: String(255), indicates if the client is the sole income earner, defaults to "Yes"
- `responsible_people`: Integer, number of people the client is responsible for, not nullable
- `business_status`: String(255), status of the client's business, not nullable
- `business_operating`: String(255), indicates if the business is operating, nullable
- `submission_time`: DateTime, timestamp of when the record was submitted, not nullable
- `inserted_at`: DateTime, timestamp of when the record was inserted into the database, defaults to the current time, not nullable
- `updated_at`: DateTime, timestamp of when the record was last updated, defaults to the current time and updates automatically on modification, not nullable

## Assumptions

- KoboToolbox API: This project assumes that the KoboToolbox API is available and accessible with the provided token and endpoint.
- Pagination: The KoboToolbox API endpoint uses pagination, and can take limit and offset parameters.
- Database: A MySQL database is set up and properly configured with the necessary schemas and permissions. If using a different database, adjust the engine settings in `database.py`.
- Webhook Accessibility: The webhook endpoint is publicly accessible to receive real-time updates.
- Database: This project assumes that a database is set up and configured correctly, with the necessary schemas and permissions.
- Environment Variables: The required environment variables (DATABASE_URL, DATABASE_TEST_URL, INKOMOKO_REGISTER_WEBHOOK_URL, REAL_TIME_POST_ENDPOINT_URL, KOBO_TOKEN, KOBO_ASSET_ID) are correctly set.
- Data Structure: The data received from the KoboToolbox API is in the expected format and structure.
- User Permissions: The user running this project has the necessary permissions to access the database and KoboToolbox API.
- Network Connectivity: The system running this project has a stable internet connection to access the KoboToolbox API.
- Compatibility: The user has created a python virtual environment and has Docker installed to run this project.

## Testing

- Run the tests using: `python -m pytest`
- Five unit tests cases are run by default and all tests should pass.
- Covered unit tests are:
  - test_extract_data_from_kobo_success
  - test_extract_data_from_kobo_failure
  - test_extract_data_from_kobo
  - test_process_kobo_data_empty
  - test_process_kobo_data_single_record
  - mock_test_save_records_to_db
  - real_data_test_save_records_to_db

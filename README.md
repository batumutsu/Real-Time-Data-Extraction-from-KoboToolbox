# Real Time Data Extraction from KoboToolbox

This project extracts data from KoboToolbox and saves it to a database, handling real-time updates for new records and edits.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up a PostgreSQL database and update the `DATABASE_URL` in `app/database.py`
4. Run the initial data extraction: `python -m app.main`
5. Start the webhook server: `python -m app.webhook`

## Usage

- The initial data extraction is performed by running `app/main.py`
- Real-time updates are handled by the webhook endpoint at `/api`
- Register the webhook using the provided code snippet, replacing the URL with your deployed endpoint

## Database Schema

The database uses a single table `kobo_records` with the following schema:

- `id`: Integer, primary key
- `kobo_id`: String, unique identifier from KoboToolbox
- `data`: JSON, stores the entire record data

## Assumptions

- The KoboToolbox API endpoint and token remain constant
- The database is PostgreSQL (change the engine in `database.py` if using a different database)
- The webhook endpoint is publicly accessible for receiving real-time updates

## Testing

Run the tests using: `python -m unittest discover tests`

import requests
from sqlalchemy.orm import Session
from .models import KoboRecord
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func, update
from dotenv import load_dotenv
import os

load_dotenv()

def extract_data_from_kobo(limit=1000, offset=0):
    KOBO_ASSET_ID = os.getenv('KOBO_ASSET_ID')
    KOBO_TOKEN = os.getenv('KOBO_TOKEN')
    url = f"https://kf.kobotoolbox.org/api/v2/assets/{KOBO_ASSET_ID}/data.json?limit={limit}&offset={offset}"
    headers = {
        'Authorization': f'Token {KOBO_TOKEN}',
        'Cookie': 'django_language=en'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to extract data: {response.status_code}")

def process_kobo_data(data):
    processed_data = []
    for record in data.get('results', []):
        processed_record = {
    'kobo_id': record.get('_id'),
    'survey_date': record.get('cd_survey_date'),
    'unique_id': record.get('sec_a/unique_id'),
    'country': record.get('sec_a/cd_biz_country_name'),
    'region': record.get('sec_a/cd_biz_region_name'),
    'bda_name': record.get('sec_b/bda_name'),
    'cohort': record.get('sec_b/cd_cohort'),
    'program': record.get('sec_b/cd_program'),
    'client_name': record.get('sec_c/cd_client_name'),
    'client_id': record.get('sec_c/cd_client_id_manifest'),
    'location': record.get('sec_c/cd_location'),
    'phone': record.get('sec_c/cd_clients_phone'),
    'alt_phone': record.get('sec_c/cd_phoneno_alt_number'),
    'phone_smart_feature': record.get('sec_c/cd_clients_phone_smart_feature'),
    'gender': record.get('sec_c/cd_gender'),
    'age': record.get('sec_c/cd_age'),
    'nationality': record.get('sec_c/cd_nationality'),
    'strata': record.get('sec_c/cd_strata'),
    'disability': record.get('sec_c/cd_disability'),
    'education': record.get('sec_c/cd_education'),
    'client_status': record.get('sec_c/cd_client_status'),
    'sole_income_earner': record.get('sec_c/cd_sole_income_earner'),
    'responsible_people': record.get('sec_c/cd_howrespble_pple'),
    'business_status': record.get('group_mx5fl16/cd_biz_status'),
    'business_operating': record.get('group_mx5fl16/bd_biz_operating'),
    'submission_time': record.get('_submission_time'),
    'updated_at': func.now()
}

        processed_data.append(processed_record)
    length = len(processed_data)
    print(f"The length of the array processed_data is: {length}")  
    return processed_data

def save_records_to_db(db: Session, records):
    stmt = insert(KoboRecord).values(records)
    stmt = stmt.on_duplicate_key_update(
        **{
            c.key: c for c in stmt.inserted if c.key not in ['id', 'kobo_id', 'inserted_at']
        }
    )
    result = db.execute(stmt)
    db.commit()
    # return result.fetchall()

def fetch_and_save_data(db: Session, batch_size=1000):
    offset = 0
    while True:
        data = extract_data_from_kobo(limit=batch_size, offset=offset)
        processed_data = process_kobo_data(data)
        
        if not processed_data:
            break
        
        save_records_to_db(db, processed_data)
        
        if len(processed_data) < batch_size:
            break
        
        offset += 1